from typing import (
    Any,
    AsyncIterator,
    Dict,
    List,
    Optional,
    Union,
    cast,
)


from guardrails.actions.reask import SkeletonReAsk
from guardrails.classes import ValidationOutcome
from guardrails.classes.history import Call, Inputs, Iteration, Outputs
from guardrails.classes.output_type import OutputTypes
from guardrails.constants import pass_status
from guardrails.llm_providers import (
    AsyncPromptCallableBase,
    PromptCallableBase,
)
from guardrails.logger import set_scope
from guardrails.run import StreamRunner
from guardrails.run.async_runner import AsyncRunner
from guardrails.telemetry import trace_async_stream_step
from guardrails.hub_telemetry.hub_tracing import async_trace_stream


class AsyncStreamRunner(AsyncRunner, StreamRunner):
    # @async_trace_stream(name="/reasks", origin="AsyncStreamRunner.async_run")
    async def async_run(
        self, call_log: Call, prompt_params: Optional[Dict] = None
    ) -> AsyncIterator[ValidationOutcome]:
        prompt_params = prompt_params or {}

        (
            messages,
            output_schema,
        ) = (
            self.messages,
            self.output_schema,
        )

        result = await self.async_step(
            0,
            output_schema,
            call_log,
            api=self.api,
            messages=messages,
            prompt_params=prompt_params,
            output=self.output,
        )
        # FIXME: Where can this be moved to be less verbose? This is an await call on
        # the async generator.
        async for call in result:
            yield call

    @async_trace_stream(name="/step", origin="AsyncStreamRunner.async_step")
    @trace_async_stream_step
    async def async_step(
        self,
        index: int,
        output_schema: Dict[str, Any],
        call_log: Call,
        *,
        api: Optional[AsyncPromptCallableBase],
        messages: Optional[List[Dict]] = None,
        prompt_params: Optional[Dict] = None,
        output: Optional[str] = None,
    ) -> AsyncIterator[ValidationOutcome]:
        prompt_params = prompt_params or {}
        inputs = Inputs(
            llm_api=api,
            llm_output=output,
            messages=messages,
            prompt_params=prompt_params,
            num_reasks=self.num_reasks,
            metadata=self.metadata,
            full_schema_reask=self.full_schema_reask,
            stream=True,
        )
        outputs = Outputs()
        iteration = Iteration(
            call_id=call_log.id, index=index, inputs=inputs, outputs=outputs
        )
        set_scope(str(id(iteration)))
        call_log.iterations.push(iteration)
        if output is not None:
            messages = None
        else:
            messages = await self.async_prepare(
                call_log,
                messages=messages,
                prompt_params=prompt_params,
                api=api,
                attempt_number=index,
            )

        iteration.inputs.messages = messages

        llm_response = await self.async_call(messages, api, output)
        iteration.outputs.llm_response_info = llm_response
        stream_output = llm_response.async_stream_output
        if not stream_output:
            raise ValueError(
                "No async stream was returned from the API. Please check that "
                "the API is returning an async generator."
            )

        fragment = ""
        parsed_fragment, validated_fragment, valid_op = None, None, None
        verified = set()
        validation_response = ""

        if self.output_type == OutputTypes.STRING:
            async for chunk in stream_output:
                chunk_text = self.get_chunk_text(chunk, api)
                _ = self.is_last_chunk(chunk, api)
                fragment += chunk_text

                parsed_chunk, move_to_next = self.parse(
                    chunk_text, output_schema, verified=verified
                )
                if move_to_next:
                    continue
                validated_fragment = await self.async_validate(
                    iteration,
                    index,
                    parsed_chunk,
                    output_schema,
                    validate_subschema=True,
                    stream=True,
                )
                if isinstance(validated_fragment, SkeletonReAsk):
                    raise ValueError(
                        "Received fragment schema is an invalid sub-schema "
                        "of the expected output JSON schema."
                    )

                reasks, valid_op = self.introspect(validated_fragment)
                if reasks:
                    raise ValueError(
                        "Reasks are not yet supported with streaming. Please "
                        "remove reasks from schema or disable streaming."
                    )
                validation_response += cast(str, validated_fragment)
                passed = call_log.status == pass_status
                yield ValidationOutcome(
                    call_id=call_log.id,  # type: ignore
                    raw_llm_output=chunk_text,
                    validated_output=validated_fragment,
                    validation_passed=passed,
                )
        else:
            async for chunk in stream_output:
                chunk_text = self.get_chunk_text(chunk, api)
                fragment += chunk_text

                parsed_fragment, move_to_next = self.parse(
                    fragment, output_schema, verified=verified
                )
                if move_to_next:
                    continue
                validated_fragment = await self.async_validate(
                    iteration,
                    index,
                    parsed_fragment,
                    output_schema,
                    validate_subschema=True,
                )
                if isinstance(validated_fragment, SkeletonReAsk):
                    raise ValueError(
                        "Received fragment schema is an invalid sub-schema "
                        "of the expected output JSON schema."
                    )

                reasks, valid_op = self.introspect(validated_fragment)
                if reasks:
                    raise ValueError(
                        "Reasks are not yet supported with streaming. Please "
                        "remove reasks from schema or disable streaming."
                    )

                if self.output_type == OutputTypes.LIST:
                    validation_response = cast(list, validated_fragment)
                else:
                    validation_response = cast(dict, validated_fragment)
                yield ValidationOutcome(
                    call_id=call_log.id,  # type: ignore
                    raw_llm_output=fragment,
                    validated_output=chunk_text,
                    validation_passed=validated_fragment is not None,
                )

        iteration.outputs.raw_output = fragment
        # FIXME: Handle case where parsing continuously fails/is a reask
        iteration.outputs.parsed_output = parsed_fragment or fragment  # type: ignore
        iteration.outputs.validation_response = validation_response
        iteration.outputs.guarded_output = valid_op

    def get_chunk_text(self, chunk: Any, api: Union[PromptCallableBase, None]) -> str:
        """Get the text from a chunk."""
        chunk_text = ""
    
        try:
            finished = chunk.choices[0].finish_reason
            content = chunk.choices[0].delta.content
            if not finished and content:
                chunk_text = content
        except Exception:
            try:
                finished = chunk.choices[0].finish_reason
                content = chunk.choices[0].text
                if not finished and content:
                    chunk_text = content
            except Exception:
                try:
                    chunk_text = chunk
                except Exception as e:
                    raise ValueError(
                        f"Error getting chunk from stream: {e}. "
                        "Non-OpenAI API callables expected to return "
                        "a generator of strings."
                    ) from e
        return chunk_text
