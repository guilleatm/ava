---
description: AVA project coding conventions and patterns. Loaded when writing or reviewing code to ensure consistency.
user-invocable: false
---

# AVA Coding Conventions

## Imports

```python
# 1. Standard library
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List

# 2. Third-party
import structlog
from pydantic import BaseModel, Field

# 3. Local
from src.config import AppConfig, load_config
from src.tools.base import Tool, ToolDefinition
```

## Class Patterns

**Interfaces/Contracts** → ABC:
```python
class AIProviderInterface(ABC):
    @abstractmethod
    async def start_session(self, call_id: str, on_event: callable) -> None: ...
```

**Data models** → dataclass:
```python
@dataclass
class CallSession:
    call_id: str
    channel_id: str
    state: str = "active"
```

**Config models** → Pydantic v2 BaseModel:
```python
class AsteriskConfig(BaseModel):
    host: str = "localhost"
    ari_port: int = 8088
```

**Options** → Enum:
```python
class ToolPhase(Enum):
    PRE_CALL = "pre_call"
    IN_CALL = "in_call"
    POST_CALL = "post_call"
```

## Async

Everything is async. Entry point: `asyncio.run(main())`.
Synchronization: `asyncio.Lock()`, never threading locks.

## Logging

```python
import structlog
log = structlog.get_logger(__name__)

log.info("call_started", call_id=call_id, provider=provider_name)
log.error("tool_failed", tool=tool_name, error=str(e))
```

## Tool Return Values

```python
# Success
return {"status": "success", "message": "Transfer complete", "extension": "100"}

# Error
return {"status": "error", "message": "Extension not found"}
```

## Testing

- pytest + pytest-asyncio (asyncio_mode=auto)
- `AsyncMock()` for async, `Mock()` for sync
- Fixtures in conftest.py
- Arrange → Act → Assert
