---
description: AVA project structure and architecture reference. Loaded on-demand when exploring or modifying the codebase.
user-invocable: false
---

# AVA Codebase Map

## Source Layout (src/)

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `src/` (root) | Core engine | `engine.py` (async main), `config.py` (Pydantic v2), `ari_client.py`, `rtp_server.py` |
| `src/core/` | Call state & audio processing | `models.py` (dataclasses), `session_store.py` (asyncio.Lock), `vad_manager.py`, `playback_manager.py` |
| `src/providers/` | AI provider integrations | `base.py` (AIProviderInterface ABC), then `openai_realtime.py`, `deepgram.py`, `google_live.py`, `local.py`, `elevenlabs_agent.py` |
| `src/pipelines/` | STT/LLM/TTS pipeline | `base.py` (Component ABC), `orchestrator.py` (PipelineOrchestrator) |
| `src/tools/` | AI-callable tools | `base.py` (Tool/PreCallTool/PostCallTool ABC), `registry.py` (singleton) |
| `src/tools/telephony/` | Call control tools | `transfer.py`, `hangup.py`, `voicemail.py`, `attended_transfer.py` |
| `src/tools/http/` | HTTP integration tools | `generic_webhook.py`, `in_call_lookup.py`, `generic_lookup.py` |
| `src/tools/business/` | Business logic tools | `email_dispatcher.py`, `gcal_tool.py`, `request_transcript.py` |
| `src/tools/adapters/` | Provider-specific tool schemas | `openai.py`, `deepgram.py`, `google.py`, `elevenlabs.py` |
| `src/audio/` | Audio transport | `audiosocket_server.py`, `resampler.py` |
| `src/config/` | Config loading | `loaders.py` (YAML + env expansion + deep merge) |
| `src/mcp/` | MCP protocol support | Model Context Protocol integration |
| `src/utils/` | Shared utilities | Normalizers, helpers |

## Config Loading Chain

```
.env (secrets) → ai-agent.yaml (baseline) → ai-agent.local.yaml (overrides)
    ↓                    ↓                           ↓
  env vars         load_yaml_with_env_expansion   deep_merge
    ↓                         ↓
              load_config() → AppConfig (Pydantic v2)
```

## Call Flow (Simplified)

```
Asterisk → ARI WebSocket → engine.py (StasisStart event)
  → session_store.create_session()
  → provider = resolve_provider(config)
  → provider.start_session(call_id, on_event)
  → AudioSocket/RTP → provider.send_audio(chunk)
  → provider fires events → engine handles (playback, tool calls, hangup)
  → tool call → ToolRegistry.get(name) → tool.execute(params, context)
```

## Testing Layout

```
tests/
├── conftest.py (if exists)    # Shared fixtures
├── tools/conftest.py          # Tool-specific fixtures (mock_ari_client, tool_context)
├── test_<module>.py           # One test file per module/feature
└── config/                    # Test config fixtures
```
