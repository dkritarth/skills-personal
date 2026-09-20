# Personal Skills

Personal skills for Kritarth Dandapat.

## Core skills

- **UNSLOP** — cut AI tells from any writing; enforce natural, direct prose.
- **WRITING** — paper-writing skill that tracks modification history and
  translates it into future intent of the work (i.e. remembers where a
  draft is headed, not just its current state).
- **LATEX** — highly fine-tuned LaTeX skill (venue templates, compile-error
  log triage, bib hygiene).
- **MATH** — proper structure for generating proofs and mathematical
  conceptual understanding with SymPy verification.

## Agent-infrastructure skills

Second track (see PLAN.md "Second track"):

- **orchestrate** — five-tier, provider-neutral model routing for
  subagents, with mappings for Anthropic (Fable orchestrates; Opus
  deep-reasons; Sonnet implements; Haiku executes mechanical/bulk work) and
  OpenAI Codex (gpt-5.1-codex-max/-codex/-codex-mini with reasoning-effort
  settings), cross-provider routing via the codex/claude CLIs, and
  escalation/demotion rules.
- **repo-wiki** — generates a GitHub wiki from CLAUDE.md/README/docs with
  source-commit staleness stamps, and makes it the first-read entry point
  for exploring agents via pointers in both CLAUDE.md and AGENTS.md
  (Claude Code and Codex respectively).
- **llm-harness** — builds an eval harness (cases, graders, baseline
  accuracy) around any LLM-dependent system so prompt changes are measured,
  not vibes.

## Status

MVP built: `.claude-plugin/marketplace.json` plus skills implemented.
Distribution model: a personal Claude Code plugin marketplace, following the
existing `~/.claude/plugins/marketplaces/` pattern (like `caveman`), not
standalone skill repos.

See `PLAN.md` for the full concept: problem statement, decisions, skill
specs, phased milestones, success criteria, and risks. See `AGENTS.md` and
`CLAUDE.md` for how to build and test skills in this repo.
