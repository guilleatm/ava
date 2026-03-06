# AVA AI Voice Agent — Project Context

## What This Is

Forked AVA (Asterisk AI Voice Agent) — we extend the AI engine with new tools, providers, and features.
Python 3.11 async codebase, 104 source files. See `.claude/skills/codebase-map/` for full structure.

## Stack (Pinned Versions)

| Component | Version | Host |
|-----------|---------|------|
| FreePBX | 17 | EC2 #1 (Debian 12) |
| Asterisk | 21 | EC2 #1 (managed by FreePBX) |
| AVA AI Voice Agent | forked | EC2 #2 (Amazon Linux) |
| SIP Stack | chan_pjsip only | (chan_sip removed in Asterisk 21) |

## CRITICAL: Version Constraints

Detailed rules in `.claude/rules/version-constraints.md`. Key points:
- **Asterisk 21**: `chan_sip` REMOVED, `Macro()` REMOVED, use `chan_pjsip` and `GoSub()`.
- **FreePBX 17**: Never edit `extensions.conf` — use `extensions_custom.conf` only.
- **AVA config**: `ai-agent.yaml` (baseline) + `ai-agent.local.yaml` (overrides) + `.env` (secrets).

## Development Workflow

Coding conventions in `.claude/rules/dev-workflow.md` and `.claude/skills/coding-conventions/`.

### Key Patterns
- **ABC** for contracts (providers, tools, pipelines)
- **Dataclasses** for data models, **Pydantic v2** for config
- **Async/await** everywhere, `asyncio.Lock()` for sync
- **structlog** for logging (`structlog.get_logger(__name__)`)
- **pytest + pytest-asyncio** (`asyncio_mode=auto`)

### Research → Plan → Implement
Use `/explore` to understand code, `/implement` to build features, `/test` to validate.

## Agents

### Development Agents
- **code-researcher**: Explore codebase, trace flows, find implementations (read-only)
- **python-developer**: Write/modify Python code following project conventions
- **test-runner**: Run tests, report results, catch regressions

### Infrastructure Agents
- **asterisk-pjsip-expert**: Asterisk dialplan, PJSIP, ARI, AudioSocket
- **freepbx-admin-expert**: FreePBX UI, modules, fwconsole, dialplan customization
- **ava-project-expert**: AVA Docker, YAML config, providers, transport modes

## Commands

| Command | Purpose |
|---------|---------|
| `/explore` | Research codebase architecture before changes |
| `/implement` | Plan and implement a feature/fix (R→P→I) |
| `/test` | Run tests with optional scope |
| `/troubleshoot` | Structured diagnosis for stack issues |
| `/log-config` | Record a config change to memory |
| `/version-check` | Check feature availability in current stack |

## AWS Architecture

```
EC2 #1 — FreePBX/Asterisk (Debian 12)
  Ports: SIP UDP/5060, RTP UDP/10000-20000, ARI TCP/8088

EC2 #2 — AVA AI Engine (Amazon Linux)
  ARI: http://<ec2-1-private-ip>:8088
  AudioSocket: TCP from EC2 #1 to EC2 #2
  Use private IPs for ARI + AudioSocket (same VPC)
```

## ARI / Stasis Model

AVA registers as a Stasis app. Dialplan routes calls via:
```
exten => s,1,Stasis(asterisk-ai-voice-agent)
```
The ai_engine connects via ARI WebSocket and takes full channel control.

## AudioSocket (Default Transport)
- Format: 16-bit signed linear PCM, 8kHz mono, 320-byte frames (20ms)
- Protocol: TLV packets over TCP

## Memory Policy

Before answering: check `memory/configurations.md` and `memory/issues-resolved.md`.
After applying config: use `/log-config`.
After resolving issue: record in `memory/issues-resolved.md`.

## Communication Guidelines

- State which version info applies to. Flag version changes.
- Treat tutorials not specifying "Asterisk 21" / "FreePBX 17" as potentially outdated.
- Beginners: provide context first. Experts: be concise.

## Key Documentation

- Asterisk 21: https://docs.asterisk.org/Asterisk_21_Documentation/
- PJSIP config: https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/
- ARI: https://docs.asterisk.org/Configuration/Interfaces/Asterisk-REST-Interface-ARI/
- AVA docs: `docs/` directory in this repo
- FreePBX 17: https://sangomakb.atlassian.net/wiki/spaces/FP/pages/222101505/FreePBX+17
