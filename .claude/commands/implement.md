---
description: Plan and implement a feature or fix in the AVA codebase. Follows the Research-Plan-Implement pattern.
---

You are starting an implementation task using the Research → Plan → Implement workflow.

## Step 1: Research

Before writing any code, understand the relevant parts of the codebase:
- Use the **code-researcher** agent (or Explore agent) to understand how the area you'll modify currently works
- Identify the files that need changes
- Understand the patterns already used in those files

## Step 2: Plan

Present a plan to the user before implementing:
- List the files to create or modify
- Describe each change briefly
- Note any new dependencies needed
- Identify which tests need to be added or updated

Wait for user approval before proceeding.

## Step 3: Implement

Write the code following the project conventions:
- Use the **python-developer** agent for complex implementations
- Follow ABC/dataclass/async patterns established in the codebase
- Use structlog for logging, Pydantic v2 for config
- Add tests for new functionality

## Step 4: Validate

After implementation:
- Use the **test-runner** agent to run relevant tests
- Verify no regressions in existing tests
- Check that the new code follows project conventions
