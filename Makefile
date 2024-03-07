MKDOCS_SERVE_ADDR ?= localhost:8000 # Default address for mkdocs serve, format: <host>:<port>, override with `make docs-serve MKDOCS_SERVE_ADDR=<host>:<port>`

# Extract major package versions for OpenAI and Pydantic
OPENAI_VERSION_MAJOR := $(shell python -c 'import openai; print(openai.__version__.split(".")[0])')
PYDANTIC_VERSION_MAJOR := $(shell python -c 'import pydantic; print(pydantic.__version__.split(".")[0])')

# Construct the typing command using only major versions
TYPING_CMD := type-pydantic-v$(PYDANTIC_VERSION_MAJOR)-openai-v$(OPENAI_VERSION_MAJOR)

autoformat:
	poetry run black guardrails/ tests/
	poetry run isort --atomic guardrails/ tests/
	poetry run docformatter --in-place --recursive guardrails tests

type:
	poetry run pyright guardrails/

.PHONY: typing
type-local:
	@make $(TYPING_CMD)

type-pydantic-v1-openai-v0:
	echo '{"exclude": ["guardrails/utils/pydantic_utils/v2.py", "guardrails/utils/openai_utils/v1.py"]}' > pyrightconfig.json
	poetry run pyright guardrails/
	rm pyrightconfig.json

type-pydantic-v1-openai-v1:
	echo '{"exclude": ["guardrails/utils/pydantic_utils/v2.py", "guardrails/utils/openai_utils/v0.py"]}' > pyrightconfig.json
	poetry run pyright guardrails/
	rm pyrightconfig.json

type-pydantic-v2-openai-v0:
	echo '{"exclude": ["guardrails/utils/pydantic_utils/v1.py", "guardrails/utils/openai_utils/v1.py"]}' > pyrightconfig.json
	poetry run pyright guardrails/
	rm pyrightconfig.json

type-pydantic-v2-openai-v1:
	echo '{"exclude": ["guardrails/utils/pydantic_utils/v1.py", "guardrails/utils/openai_utils/v0.py"]}' > pyrightconfig.json
	poetry run pyright guardrails/
	rm pyrightconfig.json

lint:
	poetry run isort -c guardrails/ tests/
	poetry run black guardrails/ tests/ --check
	poetry run flake8 guardrails/ tests/

test:
	poetry run pytest tests/

test-basic:
	set -e
	python -c "import guardrails as gd"
	python -c "import guardrails.version as mversion"

test-cov:
	poetry run pytest tests/ --cov=./guardrails/ --cov-report=xml

view-test-cov:
	poetry run pytest tests/ --cov=./guardrails/ --cov-report html && open htmlcov/index.html

view-test-cov-file:
	poetry run pytest tests/unit_tests/test_logger.py --cov=./guardrails/ --cov-report html && open htmlcov/index.html

docs-serve:
	poetry run mkdocs serve -a $(MKDOCS_SERVE_ADDR)

docs-deploy:
	poetry run mkdocs gh-deploy

dev:
	poetry install

full:
	poetry install --all-extras

docs-gen:
	poetry run python ./docs/pydocs/generate_pydocs.py
	cp -r docs docs-build
	poetry run nbdoc_build --force_all True --srcdir ./docs-build

self-install:
	pip install -e .

all: autoformat type lint docs test

precommit:
	# pytest -x -q --no-summary
	pyright guardrails/
	make lint
	./github/workflows/scripts/update_notebook_matrix.sh
