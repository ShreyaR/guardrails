from guardrails.actions.reask import FieldReAsk
from guardrails.classes.validation.validation_result import FailResult

VALIDATOR_PARALLELISM_REASK_1 = FieldReAsk(
    incorrect_value="Hello a you\nand me",
    fail_results=[
        FailResult(
            outcome="fail",
            error_message="must be exactly two words",
            fix_value="Hello a",
        ),
        FailResult(
            outcome="fail",
            error_message="Value Hello a you\nand me is not lower case.",
            fix_value="hello a you\nand me",
        ),
    ],
)
