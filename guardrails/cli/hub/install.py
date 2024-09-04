import sys
from typing import Optional

import typer

from guardrails.cli.hub.hub import hub_command
from guardrails.cli.logger import logger
from guardrails.cli.telemetry import trace_if_enabled


@hub_command.command()
def install(
    package_uri: str = typer.Argument(
        help="URI to the package to install.\
Example: hub://guardrails/regex_match."
    ),
    local_models: Optional[bool] = typer.Option(
        None,
        "--install-local-models/--no-install-local-models",
        help="Install local models",
    ),
    verbose: bool = typer.Option(
        False,
        "-v",
        "--verbose",
        help="Run the command in verbose mode to increase output verbosity.",
    ),
):
    try:
        trace_if_enabled("hub/install")
        from guardrails.hub.install import install

        def confirm():
            return typer.confirm(
                "This validator has a Guardrails AI inference endpoint available. "
                "Would you still like to install the"
                " local models for local inference?",
            )

        is_quiet = not verbose
        install(
            package_uri,
            install_local_models=local_models,
            quiet=is_quiet,
            install_local_models_confirm=confirm,
        )
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)
