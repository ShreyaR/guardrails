# noqa:W291
import pytest

from guardrails.validators import (
    BugFreeSQL,
    ExtractedSummarySentencesMatch,
    ExtractiveSummary,
    FailResult,
    Filter,
    PassResult,
    Refrain,
    SimilarToDocument,
    SqlColumnPresence,
    check_refrain_in_dict,
    filter_in_dict,
)
from tests.unit_tests.mock_embeddings import mock_create_embedding


@pytest.mark.parametrize(
    "input_dict, expected",
    [
        ({"a": 1, "b": Refrain()}, True),
        ({"a": 1, "b": {"c": 2, "d": Refrain()}}, True),
        ({"a": [1, 2, Refrain()], "b": 4}, True),
        ({"a": [1, 2, {"c": Refrain()}]}, True),
        ({"a": [1, 2, [3, 4, Refrain()]]}, True),
        ({"a": 1}, False),
    ],
)
def test_check_refrain(input_dict, expected):
    assert check_refrain_in_dict(input_dict) == expected


@pytest.mark.parametrize(
    "input_dict, expected_dict",
    [
        ({"a": 1, "b": Filter(), "c": 3}, {"a": 1, "c": 3}),
        (
            {"a": 1, "b": {"c": 2, "d": Filter()}, "e": 4},
            {"a": 1, "b": {"c": 2}, "e": 4},
        ),
        ({"a": [1, 2, Filter()], "b": 4}, {"a": [1, 2], "b": 4}),
        ({"a": [1, 2, {"c": Filter(), "d": 3}]}, {"a": [1, 2, {"d": 3}]}),
        ({"a": [1, 2, [3, 4, Filter()]]}, {"a": [1, 2, [3, 4]]}),
        ({"a": 1}, {"a": 1}),
    ],
)
def test_filter_in_dict(input_dict, expected_dict):
    assert filter_in_dict(input_dict) == expected_dict


# TODO: Implement testing with models on CI
@pytest.mark.skip(
    reason="This test requires the text-embedding-ada-002 embedding model."
    " Testing with models needs to be implemented."
)
def test_similar_to_document_validator():
    import os

    datapath = os.path.abspath(os.path.dirname(__file__) + "/../data/article1.txt")
    val = SimilarToDocument(
        document=open(datapath, "r").read(),
        model="text-embedding-ada-002",
        threshold=0.85,
    )
    summary = "All legislative powers are held by a Congress"
    " consisting of two chambers, the Senate and the House of Representatives."
    assert isinstance(val.validate(summary, {}), PassResult)


class TestBugFreeSQLValidator:
    def test_bug_free_sql(self):
        # TODO Make this robust by computing the abs path of the sql file
        # relative to this file
        val = BugFreeSQL(
            schema_file="./tests/unit_tests/test_assets/valid_schema.sql",
            conn="sqlite://",
        )
        bad_query = "select name, fro employees"
        result = val.validate(bad_query, {})
        assert isinstance(result, FailResult)
        assert result.error_message != ""

        good_query = "select name from employees;"
        assert isinstance(val.validate(good_query, {}), PassResult)

    def test_long_sql_schema_no_exception(self):
        val = BugFreeSQL(
            schema_file="./tests/unit_tests/test_assets/spider.sql",
            conn="sqlite://",
        )
        assert val is not None

    def test_bug_free_sql_simple(self):
        val = BugFreeSQL()
        bad_query = "select name, fro employees"

        result = val.validate(bad_query, {})
        assert isinstance(result, FailResult)
        assert result.error_message != ""

        good_query = "select name from employees;"
        assert isinstance(val.validate(good_query, {}), PassResult)

    def test_sql_column_presense(self):
        sql = "select name, age from employees;"
        columns = ["name", "address"]
        val = SqlColumnPresence(cols=columns)

        result = val.validate(sql, {})
        assert isinstance(result, FailResult)
        assert result.error_message in (
            "Columns [age] not in [name, address]",
            "Columns [age] not in [address, name]",
        )


def test_summary_validators(mocker):
    mocker.patch("openai.Embedding.create", new=mock_create_embedding)
    mocker.patch("guardrails.embedding.OpenAIEmbedding.output_dim", new=2)

    summary = "It was a nice day. I went to the park. I saw a dog."
    metadata = {
        "filepaths": [
            "./tests/unit_tests/test_assets/article1.txt",
            "./tests/unit_tests/test_assets/article2.txt",
        ]
    }

    val = ExtractedSummarySentencesMatch(threshold=0.1)
    result = val.validate(summary, metadata)
    assert isinstance(result, PassResult)
    assert "citations" in result.metadata
    assert "summary_with_citations" in result.metadata
    assert result.metadata["citations"] == {1: 1, 2: 1, 3: 1}
    assert (
        result.metadata["summary_with_citations"]
        == """It was a nice day. [1] I went to the park. [1] I saw a dog. [1]

[1] ./tests/unit_tests/test_assets/article1.txt
[2] ./tests/unit_tests/test_assets/article2.txt"""
    )

    val = ExtractiveSummary(
        threshold=30,
    )
    result = val.validate(summary, metadata)
    assert isinstance(result, PassResult)
    assert "citations" in result.metadata
    assert "summary_with_citations" in result.metadata
    assert result.metadata["citations"] == {1: 1, 2: 2, 3: 1}
    assert (
        result.metadata["summary_with_citations"]
        == """It was a nice day. [1] I went to the park. [2] I saw a dog. [1]

[1] ./tests/unit_tests/test_assets/article1.txt
[2] ./tests/unit_tests/test_assets/article2.txt"""
    )
