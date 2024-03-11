from typing import Any, Dict, Optional, Callable
from warnings import warn

from guardrails.logger import logger
from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="valid-url", data_type=["string"])
class ValidURL(Validator):
    """Validates that a value is a valid URL.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `valid-url`                       |
    | Supported data types          | `string`                          |
    | Programmatic fix              | None                              |
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
        logger.debug(f"Validating {value} is a valid URL...")

        from urllib.parse import urlparse

        # Check that the URL is valid
        try:
            result = urlparse(value)
            # Check that the URL has a scheme and network location
            if not result.scheme or not result.netloc:
                return FailResult(
                    error_message=f"URL {value} is not valid.",
                )
        except ValueError:
            return FailResult(
                error_message=f"URL {value} is not valid.",
            )

        return PassResult()
