.PHONY: format lint

SRC := camstat/ tests/ main.py

lint:
	@echo "Linting code..."
	@mypy $(SRC)
	@flake8 $(SRC)

format:
	@echo "Formatting code..."
	@black --line-length 79 $(SRC)
	@isort $(SRC) --profile black --line-length=79