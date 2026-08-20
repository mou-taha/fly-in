PYTHON = python3
MODULE = src
SRC_DIR = src
TEST = pytest
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

all:run

install:
	uv sync

run:
	uv run $(PYTHON) -m $(MODULE)

debug:
	uv run $(PYTHON) -m pdb -m $(MODULE)

test:
	uv run $(TEST)

clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name ".venv" -o -name ".pytest_cache" \) -exec rm -rf {} +

lint:
	flake8 .
	mypy . $(MYPY_FLAGS)

lint-strict:
	flake8 .
	mypy . --strict