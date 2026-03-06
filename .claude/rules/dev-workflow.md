---
description: Development workflow rules for the AVA codebase.
globs: ["src/**/*.py", "tests/**/*.py"]
---

# Development Workflow Rules

## Before Modifying Code
- Read the file first. Understand existing patterns before changing them.
- Check if similar functionality already exists (avoid duplication).
- For new tools: follow the Tool ABC pattern in `src/tools/base.py`.
- For new providers: follow AIProviderInterface in `src/providers/base.py`.

## Code Style
- Absolute imports from project root: `from src.config import AppConfig`
- structlog for all logging: `structlog.get_logger(__name__)`
- Async everywhere: `async def`, `await`, `asyncio.Lock()`
- Type hints on all function signatures
- Dataclasses for data, ABC for contracts, Pydantic v2 for config

## Testing Requirements
- Every new tool or provider needs tests
- Use `AsyncMock()` for async dependencies
- Tests go in `tests/test_<module>.py`
- Follow Arrange → Act → Assert pattern

## Config Changes
- Never put secrets in `ai-agent.yaml` — use `.env`
- Operator-specific settings go in `ai-agent.local.yaml`
- New config fields need Pydantic v2 model updates in `src/config.py`
