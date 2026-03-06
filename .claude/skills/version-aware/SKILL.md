---
description: Background knowledge for version-aware answering. Enforces that every technical answer specifies which Asterisk/FreePBX version it applies to, flags outdated syntax, and redirects deprecated features to their modern equivalents.
user-invocable: false
---

# Version-Aware Answering — Background Rules

This skill is always active. It modifies how you answer any technical question about Asterisk, FreePBX, or the AVA project.

## Core Rule: Always Declare the Version Context

Before or within every technical answer, state which version(s) the information applies to. Examples:

- "In Asterisk 21, ..." (not just "In Asterisk, ...")
- "As of FreePBX 17, ..." (not just "In FreePBX, ...")
- "This applies to Asterisk 18+. In Asterisk 21 specifically, ..."

If you are uncertain which version introduced or removed something, say so and fetch the official changelog.

## Outdated Syntax Detection

Immediately flag and redirect if the user (or a source they reference) uses:

| Outdated | Reason | Correct Replacement |
|---------|--------|---------------------|
| `chan_sip` | Removed in Asterisk 21 | `chan_pjsip` / `res_pjsip` |
| `[general]` SIP config | chan_sip syntax | pjsip.conf object model |
| `Macro()` | Removed in Asterisk 21 | `GoSub()` + `Return()` |
| `[macro-name]` context | app_macro syntax | `[sub-name]` + GoSub |
| `NoCDR()` | Removed in Asterisk 21 | `Set(CDR_PROP(disable)=1)` |
| `type=friend` in sip.conf | chan_sip only | PJSIP endpoint/identify objects |
| `qualify=yes` in sip.conf | chan_sip only | `qualify_frequency` on AOR in pjsip.conf |

## Tutorial Skepticism Protocol

When the user references an external tutorial or guide:
1. Check if the tutorial specifies an Asterisk/FreePBX version.
2. If it does not specify, treat it as potentially outdated.
3. If it uses any "outdated syntax" from the table above, flag it before proceeding.
4. State: "This tutorial appears to target [older version]. Here's the equivalent for Asterisk 21 / FreePBX 17:"

## Version-Specific Sections

When an answer has behavior that differs between versions, use explicit markers:
```
**Asterisk 21**: [behavior]
**Asterisk 18-20**: [behavior]
**FreePBX 17**: [behavior]
**FreePBX 16 and earlier**: [behavior — may not apply to your setup]
```

## The Current Stack

Always answer in the context of:
- **Asterisk 21**
- **FreePBX 17** (on Debian 12)
- **AVA project**: hkjarral/AVA-AI-Voice-Agent-for-Asterisk
- **AWS EC2** (two instances, private VPC networking)

If a user explicitly asks about a different version for comparison purposes, answer it, but always bring the conclusion back to what applies to this stack.

## Beginner vs. Expert Adaptation

The same version-aware rules apply regardless of the user's level. The difference is presentation:
- **Beginners**: "chan_sip is the old SIP driver that was removed in Asterisk 21. Your setup uses chan_pjsip, which is the modern replacement. Here's how to do what you're looking for with pjsip..."
- **Experts**: "Note: this uses chan_sip syntax (removed in Asterisk 21). pjsip equivalent below."
