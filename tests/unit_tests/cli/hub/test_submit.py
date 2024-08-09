import pytest
from typer.testing import CliRunner
from guardrails.cli.hub import hub_command
import os


@pytest.fixture
def mock_post_validator_submit(mocker):
    return mocker.patch(
        "guardrails.cli.hub.submit.post_validator_submit",
        new=lambda *args, **kwargs: None,
    )


def test_submit_command_success(mock_post_validator_submit):
    runner = CliRunner()
    package_name = "test_validator"

    with runner.isolated_filesystem():
        package_path = f"{package_name}.py"

        # Create a temporary file with the package name
        with open(package_path, "w+") as file:
            file.write("# Test validator content")

        result = runner.invoke(hub_command, ["submit", package_name])

        assert result.exit_code == 0

        os.remove(package_path)


def test_submit_command_failure(mock_post_validator_submit):
    runner = CliRunner()
    package_name = "test_validator"

    result = runner.invoke(hub_command, ["submit", package_name])
    assert result.exit_code != 0
