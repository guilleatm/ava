---
description: Structured troubleshooting for Asterisk, FreePBX, or AVA Voice Agent issues. Walks through systematic diagnosis: collect version/log info, isolate the failing layer, check past issues in memory, propose a fix.
---

You are running the structured troubleshooting protocol for the Asterisk + FreePBX 17 + AVA stack.

## Step 1: Collect Context

Ask the user for the following if not already provided:
- What is the symptom? (calls not connecting, no audio, ARI error, AVA not responding, etc.)
- Which layer does it appear to be in?
  - SIP/registration (trunk not registering, calls not arriving)
  - Dialplan (wrong context, calls going to wrong destination)
  - ARI/Stasis (AVA not receiving the call, WebSocket errors)
  - AVA engine (AI not responding, provider errors, Docker issues)
  - Audio (one-way audio, no audio, bad quality, latency)
- Asterisk version: `asterisk -V`
- FreePBX version: `fwconsole --version`
- AVA version: check `docker compose ps` or git tag
- Relevant logs:
  - Asterisk: `asterisk -rvvv` output or `/var/log/asterisk/full`
  - AVA: `docker compose logs ai_engine`
  - FreePBX: `/var/log/asterisk/freepbx.log`

## Step 2: Check Memory

Before diagnosing, read `memory/issues-resolved.md` to see if this problem has been encountered before.
If a matching entry exists, present that solution first and ask if it applies.

## Step 3: Layer Isolation

Use this decision tree:

```
Call not arriving at FreePBX?
  → SIP layer. Check trunk registration, provider firewall, security group UDP/5060.

Call arriving but going to wrong destination?
  → Dialplan. Check Inbound Routes in FreePBX GUI, context assignment on trunk.

Call reaching correct context but AVA not receiving?
  → Stasis/ARI. Check ari.conf, ASTERISK_STASIS_APP matches, WebSocket connection from AVA.

AVA receiving call but AI not responding?
  → AVA engine. Check .env API keys, provider config, Docker container health.

Call working but audio issues?
  → AudioSocket or RTP. Check transport config, NAT settings, security group RTP ports.
```

## Step 4: Version Safety Check

Before applying any fix found via internet search or documentation:
- Confirm it applies to Asterisk 21 (not an older version using chan_sip or Macro)
- Confirm it applies to FreePBX 17 (not an older version)
- Flag any outdated syntax and substitute the correct modern equivalent

## Step 5: Propose Fix

- Explain the root cause found
- Propose the specific change (config snippet, CLI command, GUI action)
- Ask for confirmation before the user applies it
- Note any risk (requires reload? restart? affects live calls?)

## Step 6: Log Resolution

After the fix is confirmed to work, write a new entry to `memory/issues-resolved.md`:

```markdown
## [YYYY-MM-DD] <Short symptom description>

**Symptom**: <what the user observed>
**Layer**: <SIP / Dialplan / ARI / AVA / Audio>
**Root Cause**: <what was wrong>
**Fix Applied**: <exact commands or config changes>
**Notes**: <any version-specific gotchas>
```
