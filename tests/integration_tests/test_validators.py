# noqa:W291
import pytest

from guardrails import Guard
from guardrails.datatypes import DataType
from guardrails.schema import StringSchema
from guardrails.validators import PIIFilter, SimilarToList

from .mock_embeddings import MOCK_EMBEDDINGS
from .mock_presidio import mock_anonymize


def test_similar_to_list():
    """Test initialisation of SimilarToList."""

    int_prev_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    str_prev_values = ["broadcom", "paypal"]

    def embed_function(text: str):
        """Mock embedding function."""
        return MOCK_EMBEDDINGS[text]

    # Initialise Guard from string (default parameters)
    guard = Guard.from_string(
        validators=[SimilarToList()],
        description="testmeout",
    )

    guard = Guard.from_string(
        validators=[SimilarToList(standard_deviations=2, threshold=0.2, on_fail="fix")],
        description="testmeout",
    )

    # Check types remain intact
    output_schema: StringSchema = guard.rail.output_schema
    data_type: DataType = getattr(output_schema._schema, "string")
    validators = data_type.format_attr.validators
    validator: SimilarToList = validators[0]

    assert isinstance(validator._standard_deviations, int)
    assert isinstance(validator._threshold, float)

    # 1. Test for integer values
    # 1.1 Test for values within the standard deviation
    val = 3
    output = guard.parse(
        llm_output=val,
        metadata={"prev_values": int_prev_values},
    )
    assert int(output) == val

    # 1.2 Test not passing prev_values
    # Should raise ValueError
    with pytest.raises(ValueError):
        val = 3
        output = guard.parse(
            llm_output=val,
        )

    # 1.3 Test passing str prev values for int val
    # Should raise ValueError
    with pytest.raises(ValueError):
        val = 3
        output = guard.parse(
            llm_output=val,
            metadata={"prev_values": [str(i) for i in int_prev_values]},
        )

    # 1.4 Test for values outside the standard deviation
    val = 300
    output = guard.parse(
        llm_output=val,
        metadata={"prev_values": int_prev_values},
    )
    assert output is None

    # 2. Test for string values
    # 2.1 Test for values within the standard deviation
    val = "cisco"
    output = guard.parse(
        llm_output=val,
        metadata={"prev_values": str_prev_values, "embed_function": embed_function},
    )
    assert output == val

    # 2.2 Test not passing prev_values
    # Should raise ValueError
    with pytest.raises(ValueError):
        val = "cisco"
        output = guard.parse(
            llm_output=val,
            metadata={"embed_function": embed_function},
        )

    # 2.3 Test passing int prev values for str val
    # Should raise ValueError
    with pytest.raises(ValueError):
        val = "cisco"
        output = guard.parse(
            llm_output=val,
            metadata={"prev_values": int_prev_values, "embed_function": embed_function},
        )

    # 2.4 Test not pasisng embed_function
    # Should raise ValueError
    with pytest.raises(ValueError):
        val = "cisco"
        output = guard.parse(
            llm_output=val,
            metadata={"prev_values": str_prev_values},
        )

    # 2.5 Test for values outside the standard deviation
    val = "taj mahal"
    output = guard.parse(
        llm_output=val,
        metadata={"prev_values": str_prev_values, "embed_function": embed_function},
    )
    assert output is None


def test_pii_filter(mocker):
    """Integration test for PIIFilter."""

    # Mock the analyze and anomymize functions
    mocker.patch(
        "guardrails.validators.PIIFilter.get_anonymized_text", new=mock_anonymize
    )

    # ------------------
    # 1. Initialise Guard from string (default parameters)
    # Just check whether all parameters are correctly initialised
    guard = Guard.from_string(
        validators=[PIIFilter(on_fail="fix")],
        description="testmeout",
    )
    output_schema: StringSchema = guard.rail.output_schema
    data_type: DataType = getattr(output_schema._schema, "string")
    validators = data_type.format_attr.validators
    validator: SimilarToList = validators[0]

    # When guard is initailised using default parameters, following need to be True
    assert validator.pii_entities is not None
    assert validator.pii_analyzer is not None
    assert validator.pii_anonymizer is not None

    # ------------------
    # 2. Initialise Guard from string with setting pii_entities as a string
    # Also check whether all parameters are correctly initialised
    guard = Guard.from_string(
        validators=[PIIFilter(pii_entities="pii", on_fail="fix")],
        description="testmeout",
    )
    output_schema: StringSchema = guard.rail.output_schema
    data_type: DataType = getattr(output_schema._schema, "string")
    validators = data_type.format_attr.validators
    validator: SimilarToList = validators[0]

    # Check whether following is True
    assert isinstance(validator.pii_entities, str)
    assert validator.pii_analyzer is not None
    assert validator.pii_anonymizer is not None

    # Do parse call
    text = "My email address is demo@lol.com, and my phone number is 1234567890"
    output = guard.parse(
        llm_output=text,
    )
    # Validated output should be different from input
    assert output != text

    # Validated output should contain masked pii entities
    assert all(entity in output for entity in ["<EMAIL_ADDRESS>", "<PHONE_NUMBER>"])

    # ------------------
    # 3. Initialise Guard from string with setting pii_entities as a list
    # Also check whether all parameters are correctly initialised
    guard = Guard.from_string(
        validators=[
            PIIFilter(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail="fix")
        ],
        description="testmeout",
    )
    output_schema: StringSchema = guard.rail.output_schema
    data_type: DataType = getattr(output_schema._schema, "string")
    validators = data_type.format_attr.validators
    validator: SimilarToList = validators[0]

    # Check whether following is True
    assert isinstance(validator.pii_entities, list)
    assert validator.pii_analyzer is not None
    assert validator.pii_anonymizer is not None

    # Do parse call
    text = "My email address is demo@lol.com, and my phone number is 1234567890"
    output = guard.parse(
        llm_output=text,
    )
    # Validated output should be different from input
    assert output != text

    # Validated output should contain masked pii entities
    assert all(entity in output for entity in ["<EMAIL_ADDRESS>", "<PHONE_NUMBER>"])

    # Check with text without any pii entities
    text = "My email address is xyz and my phone number is unavailable."
    output = guard.parse(
        llm_output=text,
    )
    # Validated output should be same as input
    assert output == text

    # ------------------
    # 4. Initialise Guard from string without setting pii_entities
    # Also don't pass through metadata
    # Should raise ValueError
    guard = Guard.from_string(
        validators=[PIIFilter(on_fail="fix")],
        description="testmeout",
    )

    text = "My email address is demo@lol.com, and my phone number is 1234567890"
    with pytest.raises(ValueError):
        output = guard.parse(
            llm_output=text,
        )

    # ------------------
    # 5. Initialise Guard from string without setting pii_entities
    guard = Guard.from_string(
        validators=[PIIFilter(on_fail="fix")],
        description="testmeout",
    )
    text = "My email address is demo@lol.com, and my phone number is 1234567890"

    # Now try with string of pii entities passed through metadata
    output = guard.parse(
        llm_output=text,
        metadata={"pii_entities": "pii"},
    )
    # Validated output should be different from input
    assert output != text

    # Validated output should contain masked pii entities
    assert all(entity in output for entity in ["<EMAIL_ADDRESS>", "<PHONE_NUMBER>"])

    # Now try with list of pii entities passed through metadata
    output = guard.parse(
        llm_output=text,
        metadata={"pii_entities": ["EMAIL_ADDRESS", "PHONE_NUMBER"]},
    )
    # Validated output should be different from input
    assert output != text

    # Validated output should contain masked pii entities
    assert all(entity in output for entity in ["<EMAIL_ADDRESS>", "<PHONE_NUMBER>"])

    # ------------------
    # 6. Initialise Guard from string setting
    # pii_entities as a string "pii" -> all entities
    # But also pass in metadata with all pii_entities as a list
    # only containing EMAIL_ADDRESS
    # metadata should override the pii_entities passed in the constructor,
    # and only mask in EMAIL_ADDRESS

    guard = Guard.from_string(
        validators=[PIIFilter(pii_entities="pii", on_fail="fix")],
        description="testmeout",
    )
    text = "My email address is demo@lol.com, and my phone number is 1234567890"

    output = guard.parse(
        llm_output=text,
        metadata={"pii_entities": ["EMAIL_ADDRESS"]},
    )
    # Validated output should be different from input
    assert output != text

    # Validated output should contain masked EMAIL_ADDRESS
    # and not PHONE_NUMBER
    assert "<EMAIL_ADDRESS>" in output
    assert "<PHONE_NUMBER>" not in output

    # ------------------
    # 7. Initialise Guard from string setting an incorrect string of pii_entities
    # Should raise ValueError during validate

    guard = Guard.from_string(
        validators=[PIIFilter(pii_entities="piii", on_fail="fix")],
        description="testmeout",
    )
    text = "My email address is demo@lol.com, and my phone number is 1234567890"

    with pytest.raises(ValueError):
        output = guard.parse(
            llm_output=text,
        )
