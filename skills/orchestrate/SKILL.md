---
name: orchestrate
version: 0.3.0
description: Routes subagent workflows across provider-neutral reasoning tiers and models from Anthropic and OpenAI. Matches tasks to reasoning budgets (high, medium, low, minimal) to prevent token waste and ensure reliable execution.
allowed-tools: [Agent, Read, Grep, Glob, Bash]
disable-model-invocation: true
---

# Orchestrate

Task decomposition and reasoning-budget routing for subagent workflows.

Rather than running every subagent on maximum compute or inheriting session defaults indiscriminately, this skill breaks tasks into discrete units, classifies each by required reasoning depth, and dispatches subagents with calibrated thinking budgets.

## Reasoning tiers

Classify every delegable sub-task into one tier before spawning an agent:

| Tier | Purpose | Scope and characteristics | Target reasoning depth |
|------|---------|---------------------------|------------------------|
| 0 | Orchestration & Synthesis | Task decomposition, drafting subagent specs, parallel execution planning, reconciling conflicting outputs, final integration. Always runs in the primary session. | High |
| 1 | Deep Reasoning & Architecture | System boundary design, multi-system concurrency, cryptographic protocols, complex algorithmic optimization, subtle state-machine bugs, security audits. | Maximum / Extended |
| 2 | Standard Implementation | Bounded feature development with clear specs, localized refactoring, writing unit and integration tests, reviewing pull requests against documented standards. | Medium / Balanced |
| 3 | Mechanical Execution | Type annotations, linting fixes, file renames, applying an established pattern across known files, template instantiation where the diff is specified in the prompt. | Low / Fast |
| 4 | Bulk Retrieval & Extraction | Large file tree grepping, call-graph tracing, structured JSON data extraction from documentation, log filtering, wide document scans. | Minimal / Raw Speed |

## Model and reasoning configuration

### Anthropic tier mapping

Anthropic models leverage configurable thinking budgets (extended thinking). Adjust the thinking budget to match task complexity:

| Tier | Model | Thinking configuration | Guidance |
|------|-------|------------------------|----------|
| 0 | Primary Session Model | High thinking | Coordinates workflow and synthesizes results. Do not spawn as a background subagent. |
| 1 | Opus / Sonnet | Extended thinking (16k to 32k tokens) | Provide full context and explicit correctness bounds. Allow the model room to explore edge cases before generating code. |
| 2 | Sonnet | Medium thinking (4k to 8k tokens) | Standard workhorse for features and test suites. Balances thorough planning with fast generation. |
| 3 | Sonnet | Low thinking (1k to 2k tokens) | Restrict prompt to the specific target file and the exact pattern to replicate. Fast turnaround. |
| 4 | Sonnet | Minimal or off (0 to 1k tokens) | Optimize for throughput and token economy. Ideal for scanning multiple files and returning structured summaries. |

### OpenAI tier mapping

OpenAI reasoning models utilize the `reasoning_effort` parameter (`high`, `medium`, `low`, `minimal`):

| Tier | Model | Reasoning effort | Guidance |
|------|-------|------------------|----------|
| 0 | Primary Session Model | `high` | Retains full planning state and evaluates subagent completions. |
| 1 | o3 / o1 | `high` | Solves hard algorithmic problems, architectural trade-offs, and root-cause debugging. |
| 2 | o3 / o3-mini | `medium` | Standard multi-file code editing, bug fixes with clear reproduction cases, and test authoring. |
| 3 | o3-mini | `low` | Rapid mechanical edits, boilerplate translation, and predictable refactors. |
| 4 | o3-mini | `minimal` | High-throughput queries, codebase indexing, and tabular data extraction. |

## Dispatch rules

1. **Keep subagent context tight**: Do not dump the entire workspace into subagent prompts. Pass only the relevant file paths, the specific task description, and a testable completion check.
2. **Serial vs parallel dispatch**:
   - Tiers 3 and 4 support concurrent fan-out (for example, analyzing five modules across five parallel workers).
   - Tier 1 must run serially when subsequent architecture depends on its decisions.
3. **Escalation protocol**:
   - If a Tier 2 subagent fails a test loop twice on unexpected edge cases, escalate the task to Tier 1 with the test failure log attached.
   - Do not re-run a failed Tier 3 task on Tier 3 without changing prompt specificity; if the task was more ambiguous than anticipated, promote it to Tier 2.
4. **Provider consistency**: Use a single provider family within an integrated task pipeline to avoid conflicting tool conventions and formatting drift.
