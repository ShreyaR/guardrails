from guardrails.actions.reask import SkeletonReAsk
from guardrails.classes.validation.validation_result import FailResult

MSG_VALIDATED_OUTPUT_REASK = SkeletonReAsk(
    incorrect_value={"name": "Inception", "director": "Christopher Nolan"},
    fail_results=[
        FailResult(
            outcome="fail",
            metadata=None,
            error_message="""JSON does not match schema:
{
  "$": [
    "'release_year' is a required property"
  ]
}""",
            fix_value=None,
        )
    ],
)
