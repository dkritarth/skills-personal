---
name: orchestrate
version: 2.0.0
description: Route T3 Code agent workflows using Kritarth's account priority, model limits, and reasoning preferences. Use for delegation or complex workflow coordination; routine tasks need no Opus consultation.
allowed-tools: [Agent, Read, Grep, Glob, Bash, "mcp__t3_code__*"]
disable-model-invocation: true
---

# Orchestrate for T3 Code

Account-aware T3 delegation replaces PLAN.md's generic model tiers.

## When to use

Apply when orchestrating or delegating work in T3 Code.

## When not to use

Outside T3 Code, follow the current environment's delegation rules.

## Routing policy

Conversation instructions override this policy, including earlier model-specific high-reasoning requests. Propagate overrides to children.

```yaml
gpt_accounts: # Ordered priority; user-reported account context, 2026-10-08.
  - providerInstanceId: codex_ff6378d1-48cf-483c-b7de-0d006580d645
    displayName: ChatGPT - KD
    context: Extra account with 2500 credits; consume these first.
  - providerInstanceId: codex
    displayName: Codex
    context: Normal $20 account; use after KD credits run out or KD is unavailable.
routes:
  orchestrator:
    providerInstanceId: claudeAgent
    model: claude-opus-5-5
    options: {effort: medium}
  implementation:
    provider: gpt_accounts
    model: gpt-6.1-sol
    options: {reasoningEffort: medium}
  routine:
    provider: gpt_accounts
    model: gpt-6-luna
    options: {reasoningEffort: medium} # High is also permitted when useful.
  research:
    providerInstanceIds: [antigravity, antigravity_2]
    model: gemini-3.8-flash-high
```

- Opus coordinates complex workflows, instructs workers, and resolves exceptionally difficult questions. Existing Opus parents coordinate directly; other parents delegate one Opus coordinator when needed. Routine work goes straight to workers. The parent model cannot be changed by this skill.
- Sol edits codebases, implements, debugs, and validates. Opus delegates execution to Sol.
- Luna handles charts, reports, datasets, authorized GitHub updates/pushes, repetitive workflows, and monitoring. Route codebase implementation to Sol.
- Before Luna monitors HPCC, load `msu-dminer-fleet` and its `references/hpcc.md`; use verified hosts and job IDs.
- Flash High handles internet lookup, source verification, and research. Prefer the first available Antigravity instance.
- Only these models are allowed by default. Claude uses only Opus 5.5; OpenCode and other providers require a user override.
- Credits are user context, not live balances. Prefer KD for all GPT work; fall back to Codex on quota/access failure without duplicating active tasks. Report other unavailable routes; do not substitute unlisted models.

## Execution

1. Call `orchestrator_capabilities`; verify accounts, availability, models, and options. Set model and effort explicitly. Flash's effort is encoded in its model ID.
2. Use T3 `delegate_task` for account-specific GPT and cross-provider work. Supply the goal, paths, edit scope, policy/overrides, deliverables, and checks. Parallelize independent work with separate file ownership; serialize dependencies.
3. Verify artifacts and checks before integrating. For task tracking, review rounds, or missing MCP tools, read [references/t3-protocol.md](references/t3-protocol.md).

Keep task IDs in workflow context; this skill stores no persistent state.
