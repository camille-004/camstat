.PHONY: format lint

SRC := camstat/ main.py
TEST_DIR := tests/

lint:
	@echo "Linting code..."
	@mypy $(SRC)
	@flake8 $(SRC)

format:
	@echo "Formatting code..."
	@black --line-length 79 $(SRC) $(TEST_DIR)
	@isort $(SRC) $(TEST_DIR) --profile black --line-length=79

test:
	pytest tests/