import logging
from typing import Any, Dict

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

logger = logging.getLogger(__name__)


@register_validator(name="ends-with", data_type="list")
class EndsWith(Validator):
    """Validates that a list ends with a given value.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `ends-with`                       |
    | Supported data types          | `list`                            |
    | Programmatic fix              | Append the given value to the list. |

    Parameters: Arguments
        end: The required last element.
    """

    def __init__(self, end: str, on_fail: str = "fix"):
        super().__init__(on_fail=on_fail, end=end)
        self._end = end

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        logger.debug(f"Validating {value} ends with {self._end}...")

        if not value[-1] == self._end:
            return FailResult(
                error_message=f"{value} must end with {self._end}",
                fix_value=value + [self._end],
            )

        return PassResult()