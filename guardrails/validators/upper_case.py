from typing import Any, Callable, Dict, Optional

from guardrails.logger import logger
from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="upper-case", data_type="string")
class UpperCase(Validator):
    """Validates that a value is upper case.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `upper-case`                      |
    | Supported data types          | `string`                          |
    | Programmatic fix              | Convert to upper case.            |
    """

    def __init__(self, on_fail: Optional[Callable] = None):
        super().__init__(
            on_fail=on_fail,
        )

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        logger.debug(f"Validating {value} is upper case...")

        if value.upper() != value:
            return FailResult(
                error_message=f"Value {value} is not upper case.",
                fix_value=value.upper(),
            )

        return PassResult()
