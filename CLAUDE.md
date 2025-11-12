# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenReview Comment Extractor - A Python script to extract OpenReview comments for a paper into a markdown file for easy copy/pasting during rebuttals.

This should be a command-line tool via CLI that takes in a forum ID and optionally user credentials, and uses the OpenReview API to get the comments and format them as markdown for easy copy/pasting during rebuttals.

## Features

- Can save all comments to a single file (default behavior), or save each comment to a separate file
- Can run as a CLI command `extract-openreview-comments`
- Is publishable as a PyPI package `extract-openreview-comments`

## Development Environment

- Python: >=3.11
- Package manager: Uses pyproject.toml (uses uv)
- Type checking: pyright
- Linting/formatting: ruff
- Testing: pytest

## Common Commands

```bash
# Install dependencies (development)
uv sync

# Run the script
python main.py

# Type checking
uv run pyright

# Linting and formatting
uv run ruff check .
uv run ruff format .

# Run tests
uv run pytest

# Run a single test file
uv run pytest tests/test_file.py

# Run a specific test
uv run pytest tests/test_file.py::test_function_name
```

## Code Architecture

The project is structured as a Python package:

- `extract_openreview_comments/` - Main package directory
  - `__init__.py` - Package initialization
  - `cli.py` - Command-line interface using Click
  - `client.py` - OpenReview API client wrapper
  - `formatter.py` - Markdown formatting logic
- `tests/` - Unit tests for the package
  - `test_client.py` - Tests for API client
  - `test_formatter.py` - Tests for markdown formatter
- `main.py` - Alternative entry point for development
- `pyproject.toml` - Project configuration and dependencies
