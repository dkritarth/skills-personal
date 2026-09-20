---
name: orchestrate
version: 0.2.0
description: Decomposes complex tasks into five provider-neutral difficulty tiers and routes subagents to the most cost-effective model. Supports Claude Code and OpenAI Codex mappings.
allowed-tools: [Agent, Read, Grep, Glob, Bash]
disable-model-invocation: true
---

# Orchestrate

Task decomposition and difficulty-tier routing for agent sub-tasks.

Decompose work into discrete sub-tasks, map each sub-task to a difficulty tier, and spawn subagents using the corresponding model. Do not use for small tasks that can be completed directly in a single turn.

## The five difficulty tiers

Classify every sub-task into one tier before dispatching agents:

| Tier | Name | Target scope |
|------|------|--------------|
| 0 | Orchestration | Decomposing tasks, writing subagent prompts, parallelizing work, synthesizing outputs, evaluating conflicting results. Always runs in the primary session. |
| 1 | Deep reasoning | System architecture, concurrency bugs, cryptographic logic, security audits, formal verifications. |
| 2 | Standard implementation | Multi-file features with clear specs, bounded refactors, writing unit tests for documented behaviors, code reviews. |
| 3 | Mechanical execution | Renames, code formatting, boilerplate generation, applying an existing pattern across multiple files. |
| 4 | Bulk retrieval & labeling | Scanning large file trees, search query aggregation, structured data extraction, document summarization. |

## Provider mapping

| Tier | Anthropic (Claude Code) | OpenAI (Codex) |
|------|------------------------|----------------|
| 0 | Primary session model | Primary session model (reasoning effort: `xhigh`) |
| 1 | Opus | gpt-5.1-codex-max (reasoning effort: `high`) |
| 2 | Sonnet | gpt-5.1-codex (reasoning effort: `medium`) |
| 3 | Haiku | gpt-5.1-codex-mini (reasoning effort: `low`) |
| 4 | Haiku | gpt-5.1-codex-mini (reasoning effort: `minimal`) |

## Execution rules

1. **Verify model availability**: Confirm target model flags before spawning. If newer model generations are active in the environment, select the tier-equivalent replacement.
2. **Consistent providers**: Stick with a single provider family within a workflow tier to keep latency and tool conventions predictable.
3. **Escalation**: If a Tier 2 or 3 agent fails repeatedly on an ambiguous failure mode, escalate the sub-task directly to Tier 1 with an updated prompt specifying the failure criteria.
