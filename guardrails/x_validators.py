"""Create validators for each data type."""
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Union, Any, Optional, Callable, Dict

from guardrails.x_datatypes import registry as types_registry

validators_registry = {}
types_to_validators = defaultdict(list)


logger = logging.getLogger(__name__)


def register_validator(name: str, data_type: Union[str, List[str]]):
    """Register a validator for a data type."""

    def decorator(cls: type):
        """Register a validator for a data type."""

        nonlocal data_type
        if isinstance(data_type, str):
            if data_type == 'all':
                data_type = list(types_registry.keys())
            else:
                data_type = [data_type]

        # Make sure that the data type string exists in the data types registry.
        for dt in data_type:
            if dt not in types_registry:
                raise ValueError(f"Data type {dt} is not registered.")

            types_to_validators[dt].append(name)

        validators_registry[name] = cls
        return cls

    return decorator


@dataclass
class EventDetail(BaseException):
    """Event detail."""

    key: str
    value: Any
    schema: Dict[str, Any]
    error_message: str
    debug_value: Any


@dataclass
class ReAsk:
    incorrect_value: Any
    error_message: str


class Validator:
    """Base class for validators."""

    def __init__(self, on_fail: Optional[Callable] = None):
        if on_fail is not None:
            if isinstance(on_fail, str):
                if on_fail == 'filter':
                    on_fail = self.filter
                elif on_fail == 'refrain':
                    on_fail = self.refrain
                elif on_fail == 'noop':
                    on_fail = self.noop
                elif on_fail == 'debug':
                    on_fail = self.debug
                else:
                    raise ValueError(f"Unknown on_fail value: {on_fail}.")
            self.on_fail = on_fail
        else:
            self.on_fail = self.debug


    def validate_with_correction(self, key, value, schema) -> Dict:
        try:
            return self.validate(key, value, schema)
        except Exception as e:
            logger.debug(f"Validator {self.__class__.__name__} failed for {key} with error {e}.")
            return self.on_fail(key, value, schema, e)


    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate a value."""

        raise NotImplementedError

    def debug(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Debug the incorrect value."""

        raise NotImplementedError

    def reask(self, key: str, value: Any, schema: Union[Dict, List], error: BaseException) -> Dict:
        """Reask disambiguates the validation failure into a helpful error message."""

        schema[key] = ReAsk(value, error)
        return schema

    def filter(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """If validation fails, filter the offending key from the schema."""

        logger.debug(f"Filtering {key} from schema...")

        if isinstance(schema, dict):
            schema.pop(key)
        elif isinstance(schema, list):
            schema.remove(value)

        return schema

    def refrain(self, key: str, value: Any, schema: Union[Dict, List]) -> Optional[Dict]:
        """If validation fails, refrain from answering."""

        logger.debug(f"Refusing to answer {key}...")
    
        return None

    def noop(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """If validation fails, do nothing."""

        logger.debug(f"Validator {self.__class__.__name__} failed for {key}, but doing nothing...")

        return schema


# @register_validator('required', 'all')
# class Required(Validator):
#     """Validate that a value is not None."""

#     def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> bool:
#         """Validate that a value is not None."""

#         return value is not None


# @register_validator('description', 'all')
# class Description(Validator):
#     """Validate that a value is not None."""

#     def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> bool:
#         """Validate that a value is not None."""

#         return value is not None


@register_validator(name='valid-range', data_type=['integer', 'float', 'percentage'])
class ValidRange(Validator):
    """Validate that a value is within a range."""

    def __init__(self, min: int = None, max: int = None, on_fail: Optional[Callable] = None):
        """Initialize the validator."""
        super().__init__(on_fail=on_fail)

        self._min = min
        self._max = max

    def validate(self, key, str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is within a range."""

        logger.debug(f"Validating {value} is in range {self._min} - {self._max}...")

        if self._min is not None and value < self._min:
            logger.debug(f"Value {value} is less than {self._min}.")
            return self.on_fail(key, value, schema)

        if self._max is not None and value > self._max:
            logger.debug(f"Value {value} is greater than {self._max}.")
            return self.on_fail(key, value, schema)

        return schema

    def debug(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is within a range."""
        # If value is less than min, return min. If value is greater than max, return max.

        logger.debug(f"Validating {value} is in range {self._min} - {self._max}...")
        logger.debug(f"Value {value} is not in range {self._min} - {self._max}.")

        if self._min is not None and value < self._min:
            logger.debug(f"Value {value} is less than {self._min}.")
            schema[key] = self._min

        if self._max is not None and value > self._max:
            logger.debug(f"Value {value} is greater than {self._max}.")
            schema[key] = self._max

        return schema


@register_validator(name='valid-choices', data_type='all')
class ValidChoices(Validator):
    """Validate that a value is within a range."""

    def __init__(self, choices: List[Any], on_fail: Optional[Callable] = None):
        """Initialize the validator."""
        super().__init__(on_fail=on_fail)
        self._choices = choices

    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is within a range."""

        logger.debug(f"Validating {value} is in choices {self._choices}...")

        validation_outcome = value in self._choices

        logger.debug(f"Validation outcome: {validation_outcome}")

        if not validation_outcome:
            return self.on_fail(key, value, schema)

        return schema


@register_validator(name='lower-case', data_type='string')
class LowerCase(Validator):
    """Validate that a value is lower case."""

    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is lower case."""

        logger.debug(f"Validating {value} is lower case...")

        validation_outcome = value.lower() == value

        logger.debug(f"Validation outcome: {validation_outcome}")

        if not validation_outcome:
            return self.on_fail(key, value, schema)

        return schema

    def debug(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is lower case."""
        raise NotImplementedError


@register_validator(name='upper-case', data_type='string')
class UpperCase(Validator):
    """Validate that a value is upper case."""

    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is upper case."""

        logger.debug(f"Validating {value} is upper case...")

        validation_outcome = value.upper() == value

        logger.debug(f"Validation outcome: {validation_outcome}")

        if not validation_outcome:
            return self.on_fail(key, value, schema)

        return schema

    def debug(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is upper case."""
        raise NotImplementedError


@register_validator(name='length', data_type=['string', 'list', 'object'])
class ValidLength(Validator):
    """Validate that the length of value is within the expected range."""

    def __init__(
            self,
            min: int = None,
            max: int = None,
            on_fail: Optional[Callable] = None
    ):
        """Initialize the validator."""
        super().__init__(on_fail=on_fail)
        self._min = int(min)
        self._max = int(max)

    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is within a range."""

        logger.debug(f"Validating {value} is in length range {self._min} - {self._max}...")

        if self._min is not None and len(value) < self._min:
            logger.debug(f"Value {value} is less than {self._min}.")
            return self.on_fail(key, value, schema)

        if self._max is not None and len(value) > self._max:
            logger.debug(f"Value {value} is greater than {self._max}.")
            return self.on_fail(key, value, schema)

        logger.debug(f"Value {value} is in range {self._min} - {self._max}.")
        return schema

    def debug(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is within a range."""
        raise NotImplementedError


@register_validator(name='two-words', data_type='string')
class TwoWords(Validator):
    """Validate that a value is upper case."""

    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is upper case."""
        logger.debug(f"Validating {value} is two words...")

        validation_outcome = len(value.split()) == 2

        logger.debug(f"Validation outcome: {validation_outcome}")


        print(f'\n\n\nValidating {value} is two words...')
        print(f'Validation outcome: {validation_outcome}\n\n\n')


        if not validation_outcome:
            return self.on_fail(key, value, schema)

        return schema

    def debug(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is upper case."""
        raise NotImplementedError


@register_validator(name='one-line', data_type='string')
class OneLine(Validator):
    """Validate that a value is a single line or sentence."""

    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is a single line or sentence."""
        logger.debug(f"Validating {value} is a single line...")

        validation_outcome = len(value.splitlines()) == 1

        logger.debug(f"Validation outcome: {validation_outcome}")

        if not validation_outcome:
            return self.on_fail(key, value, schema)

        return schema

    def debug(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is upper case."""
        raise NotImplementedError


@register_validator(name='valid-url', data_type=['string', 'url'])
class ValidUrl(Validator):
    """Validate that a value is a valid URL."""

    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        """Validate that a value is a valid URL."""
        logger.debug(f"Validating {value} is a valid URL...")

        import requests

        # Check that the URL exists and can be reached
        try:
            response = requests.get(value)
            if not response.status_code == 200:
                validation_outcome = False
                error = ValueError(f"URL {value} returned status code {response.status_code}")
        except requests.exceptions.ConnectionError as e:
            validation_outcome = False
            error = e

        logger.debug(f"Validation outcome: {validation_outcome}")

        if not validation_outcome:
            return self.on_fail(key, value, schema, error=error)

        return schema

    def reask(
            self,
            key: str,
            value: Any,
            schema: Union[Dict, List],
            error: BaseException
    ) -> Dict:
        """Validate that a value is upper case."""

        helpful_prompt = f'URL {value} returned status code {error.message}'

        return helpful_prompt
