
from typing import Any, Dict

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

from guardrails.logger import logger


@register_validator(name="one-line", data_type="string")
class OneLine(Validator):
    """Validates that a value is a single line or sentence.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `one-line`                        |
    | Supported data types          | `string`                          |
    | Programmatic fix              | Pick the first line.              |
    """

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        logger.debug(f"Validating {value} is a single line...")

        if len(value.splitlines()) > 1:
            return FailResult(
                error_message=f"Value {value} is not a single line.",
                fix_value=value.splitlines()[0],
            )

        return PassResult()
