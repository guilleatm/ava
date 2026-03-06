---
description: Version constraints for Asterisk 21 and FreePBX 17. Always enforced.
globs: ["**/*.conf", "**/*.yaml", "**/*.md"]
---

# Version Constraints — Always Enforce

## Asterisk 21 Removals (NEVER reference as available)
- `chan_sip` — REMOVED. Use `chan_pjsip` / `res_pjsip`.
- `app_macro` / `Macro()` — REMOVED. Use `GoSub()`.
- `NoCDR()` — REMOVED.

## FreePBX 17 Constraints
- Install method: bash script on vanilla Debian 12.
- NEVER edit `extensions.conf` or `extensions_additional.conf` — FreePBX regenerates them.
- Custom dialplan goes in `extensions_custom.conf` only.
- Macros are gone: always use `GoSub()`.

## AVA Config Model
1. `config/ai-agent.yaml` — Golden baseline (git-tracked)
2. `config/ai-agent.local.yaml` — Operator overrides (git-ignored, deep-merged)
3. `.env` — API keys and secrets (git-ignored)
