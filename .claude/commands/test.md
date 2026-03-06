---
description: Run tests for the AVA project. Optionally specify a scope (file, function, marker).
---

You are running tests for the AVA project.

## Determine Scope

Ask the user (if not specified) what to test:
- **All tests**: `python -m pytest tests/ -v`
- **Specific file**: `python -m pytest tests/test_<name>.py -v`
- **Specific function**: `python -m pytest tests/test_<name>.py::test_function -v`
- **By marker**: `python -m pytest tests/ -m unit -v`
- **With coverage**: Add `--cov=src --cov-report=term-missing`

## Execute

Use the **test-runner** agent to run the tests and report results.

## Report

Provide a summary: passed/failed/skipped counts, and details on any failures.
