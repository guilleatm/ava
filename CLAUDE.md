# Asterisk + FreePBX + AVA Voice Agent — Project Context

## Stack (Pinned Versions)

| Component | Version | Host |
|-----------|---------|------|
| FreePBX | 17 | EC2 #1 (Debian 12) |
| Asterisk | 21 | EC2 #1 (managed by FreePBX) |
| AVA AI Voice Agent | latest (hkjarral/AVA-AI-Voice-Agent-for-Asterisk) | EC2 #2 (Amazon Linux) |
| OS — FreePBX | Debian 12 | EC2 #1 |
| OS — AVA | Amazon Linux | EC2 #2 |
| SIP Stack | chan_pjsip only | (chan_sip is removed in Asterisk 21) |

## CRITICAL: Version Constraints — Always Enforce These

### Asterisk 21 Removals (NEVER reference these as available)
- `chan_sip` — REMOVED. Use `chan_pjsip` / `res_pjsip` exclusively.
- `app_macro` / `Macro()` — REMOVED. Use `GoSub()` exclusively.
- `NoCDR()` — REMOVED.
- Any tutorial or doc referencing these for "Asterisk" without specifying a version predates Asterisk 21.

### FreePBX 17 Constraints
- Install method: bash script on vanilla Debian 12 (no ISO).
- Dialplan: NEVER edit `extensions.conf` or `extensions_additional.conf` — FreePBX regenerates them.
- Custom dialplan goes in `extensions_custom.conf` only.
- Module reload: `fwconsole reload` or `asterisk -rx "dialplan reload"`.
- Macros are gone: always use `GoSub()`.

### AVA Project Config Model (Three Files)
1. `config/ai-agent.yaml` — Golden baseline (git-tracked)
2. `config/ai-agent.local.yaml` — Operator overrides (git-ignored, deep-merged)
3. `.env` — API keys and secrets (git-ignored)

## AWS Architecture

```
EC2 #1 — FreePBX/Asterisk (Debian 12)
  - Elastic IP: [see memory/infrastructure.md]
  - Ports: SIP UDP/5060, RTP UDP/10000-20000, ARI TCP/8088 (restricted to EC2 #2)
  - PJSIP: external_media_address + external_signaling_address = Elastic IP
           local_net = VPC CIDR

EC2 #2 — AVA AI Engine (Amazon Linux)
  - Runs: ai_engine + optionally local_ai_server (Docker)
  - ARI connection: ASTERISK_ARI_URL = http://<ec2-1-private-ip>:8088
  - AudioSocket: TCP from EC2 #1 to EC2 #2
  - Use private IPs for ARI + AudioSocket traffic (same VPC)
```

## ARI / Stasis Model
AVA registers as a Stasis application. Dialplan routes calls via:
```
exten => s,1,Stasis(asterisk-ai-voice-agent)
```
The ai_engine container connects via ARI WebSocket and takes full channel control.

## AudioSocket (Default AVA Transport)
- Format: 16-bit signed linear PCM, 8kHz mono, 320-byte frames (20ms each)
- Protocol: TLV packets over TCP
- Bandwidth: ~128 kbps per active call

## Communication Guidelines

- **Beginners**: Always provide context before the answer. Define jargon on first use.
- **Experts**: Be precise and concise. Skip basics unless asked.
- **All answers**: State which version a piece of information applies to. Flag if a feature changed between versions.
- **Version traps**: If a user asks about something removed in Asterisk 21 or changed in FreePBX 17, redirect immediately and explain why.
- **Tutorials from the internet**: Treat any tutorial not specifying "Asterisk 21" or "FreePBX 17" as potentially outdated.

## Memory Policy

Before answering any question:
1. Check `memory/configurations.md` — has this already been configured?
2. Check `memory/issues-resolved.md` — has this problem been seen before?

After applying any configuration:
- Use `/log-config` to record it in `memory/configurations.md`.

After resolving any issue:
- Record in `memory/issues-resolved.md` with: symptom, root cause, fix applied.

## Key Documentation

Full curated doc index: `asterisk-ai-voice-agent-documentation-sources.md`

Quick links:
- Asterisk 21 docs: https://docs.asterisk.org/Asterisk_21_Documentation/
- PJSIP config: https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/PJSIP-Configuration-Sections-and-Relationships/
- ARI overview: https://docs.asterisk.org/Configuration/Interfaces/Asterisk-REST-Interface-ARI/
- AVA Installation: https://github.com/hkjarral/AVA-AI-Voice-Agent-for-Asterisk/blob/main/docs/INSTALLATION.md
- AVA Config Reference: https://github.com/hkjarral/AVA-AI-Voice-Agent-for-Asterisk/blob/main/docs/Configuration-Reference.md
- FreePBX 17 Wiki: https://sangomakb.atlassian.net/wiki/spaces/FP/pages/222101505/FreePBX+17

## Subagents Available

- **asterisk-pjsip-expert**: Asterisk dialplan, PJSIP, ARI, AudioSocket questions
- **freepbx-admin-expert**: FreePBX UI, modules, fwconsole, dialplan customization
- **ava-project-expert**: AVA Docker, YAML config, providers, transport modes, tool calling
