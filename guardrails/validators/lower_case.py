from typing import Any, Callable, Dict, Optional
from warnings import warn

from guardrails.logger import logger
from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="lower-case", data_type="string")
class LowerCase(Validator):
    """Validates that a value is lower case.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `lower-case`                      |
    | Supported data types          | `string`                          |
    | Programmatic fix              | Convert to lower case.            |
    """

    def __init__(self, on_fail: Optional[Callable] = None):
        warn(
            """
            Using this validator from `guardrails.validators` is deprecated.
            Please install and import this validator from Guardrails Hub instead.
            This validator would be removed from this module in the next major release.
            """,
            FutureWarning,
        )
        super().__init__(on_fail=on_fail)

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        logger.debug(f"Validating {value} is lower case...")

        if value.lower() != value:
            return FailResult(
                error_message=f"Value {value} is not lower case.",
                fix_value=value.lower(),
            )

        return PassResult()
