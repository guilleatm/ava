---
description: Log a configuration step to the project memory. Use this after applying any change to Asterisk, FreePBX, AVA, or AWS infrastructure so the team's progress is tracked across sessions.
---

You are logging a configuration step to the persistent project memory.

## Gather the Information

Ask the user to describe what was configured. Collect:

1. **Component**: Which part of the stack was configured?
   - FreePBX (module, trunk, route, extension, IVR)
   - Asterisk (ari.conf, pjsip.conf, extensions_custom.conf, etc.)
   - AVA (ai-agent.yaml, ai-agent.local.yaml, .env, Docker)
   - AWS (security group, Elastic IP, VPC, EC2 config)
   - Other

2. **What was done**: Brief description of the change

3. **Config snippet** (optional but recommended): The actual values/lines applied

4. **Why**: What problem does this solve or what feature does this enable?

5. **Status**: Did it work? Any follow-up needed?

## Write to Memory

Append a new entry to `memory/configurations.md` in this format:

```markdown
## [YYYY-MM-DD] <Component> — <Short description>

**Component**: <FreePBX / Asterisk / AVA / AWS / Other>
**Action**: <What was done>
**Config**:
```
<paste config snippet here if applicable>
```
**Purpose**: <Why this was done>
**Status**: <Working / Pending verification / Needs follow-up>
**Notes**: <Any version-specific details, caveats, or dependencies>
```

## Update MEMORY.md if Needed

If this entry represents a significant milestone (e.g., trunk connected, AVA first call working, ARI connected), add a one-line summary to `memory/MEMORY.md` in the "Recent Milestones" section.

After writing, confirm to the user: "Logged to memory/configurations.md on [date]."
