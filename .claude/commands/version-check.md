---
description: Check whether a specific Asterisk feature, configuration option, dialplan application, or module is available in the current stack (Asterisk 21, FreePBX 17). Returns a clear version matrix and flags outdated syntax.
---

You are performing a version compatibility check for the Asterisk + FreePBX 17 stack.

## Understand the Query

The user wants to know if a specific feature, config option, application, or module is:
- Available in Asterisk 21
- Available in FreePBX 17
- Changed between versions
- Deprecated or removed

Identify what they're asking about (e.g., `chan_sip`, `Macro()`, `MixMonitor`, `PJSIP`, `ExternalMedia`, a specific ARI endpoint, etc.)

## Version Matrix Template

Respond with a clear version matrix like this:

```
Feature/Option: <name>

| Version        | Status     | Notes |
|----------------|------------|-------|
| Asterisk 16    | Available  | ...   |
| Asterisk 18    | Deprecated | ...   |
| Asterisk 20    | Removed    | ...   |
| Asterisk 21    | REMOVED    | Use X instead |
| FreePBX 16     | Supported  | ...   |
| FreePBX 17     | NOT SUPPORTED | Use Y instead |

Current stack (Asterisk 21 + FreePBX 17): ✅ Available / ❌ Not Available / ⚠️ Changed

Recommended alternative (if removed/changed): <what to use instead>
```

## Key Known Version Facts

Reference these without needing to search:

**Removed in Asterisk 21:**
- `chan_sip` → use `chan_pjsip` (res_pjsip)
- `app_macro` / `Macro()` → use `GoSub()`
- `NoCDR()` → use `Set(CDR_PROP(disable)=1)`
- `IAXJB` jitter buffer option
- Several deprecated HTTP server changes

**Removed in FreePBX 17 (relative to 16):**
- chan_sip support entirely dropped
- Macro-based internal routing replaced with GoSub
- Old ISO installer replaced by Debian 12 script

**Changed behavior in Asterisk 21:**
- Translation cost improvements (may affect codec selection order)
- HTTP server changes (affects ARI endpoint paths — verify with official docs)

**Still available in Asterisk 21:**
- `chan_pjsip`, `res_pjsip` — full PJSIP stack
- `app_agi`, `app_fastagi` — AGI interface
- `res_ari` — full ARI support
- `app_audiosocket` — AudioSocket (added in Asterisk 18)
- `app_stasis` — Stasis dialplan application
- `MixMonitor()`, `Monitor()` — call recording
- `GoSub()`, `Return()` — subroutine execution

## Fetch if Uncertain

If you are not certain about a specific feature, fetch the official source:
- Asterisk 21 What's New: https://docs.asterisk.org/Asterisk_21_Documentation/WhatsNew/
- Asterisk CHANGES file: https://github.com/asterisk/asterisk/blob/21/CHANGES
- Module list: https://docs.asterisk.org/Asterisk_21_Documentation/

Always cite the source when reporting version status.
