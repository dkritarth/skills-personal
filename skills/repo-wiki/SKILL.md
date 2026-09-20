---
name: repo-wiki
version: 0.2.0
description: Generates and synchronizes a GitHub wiki from project documentation, READMEs, CLAUDE.md, AGENTS.md, and codebase structure. Keeps documentation centralized and version-controlled.
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit]
disable-model-invocation: true
---

# Repo-Wiki

Distill repository documentation and architecture into a versioned GitHub wiki.

Use this skill when onboarding to an unfamiliar codebase, centralizing scattered architectural notes, or setting up persistent reference documentation.

## GitHub wiki mechanics

A GitHub wiki is an independent Git repository hosted at `<repo-url>.wiki.git`.
Pages are Markdown files placed at the wiki root:
- `Home.md`: Primary entry point and navigation index.
- Filenames map directly to page titles (for example, `Architecture.md` displays as "Architecture").
- Enable wikis under repository settings before cloning (`gh repo edit --enable-wiki`).

## Process

### 1. Gather reference sources
Read existing documentation in priority order:
- `CLAUDE.md` and `AGENTS.md`
- `README.md` and `docs/`
- Architecture notes (`ARCHITECTURE.md`, `PLAN.md`)
- Package manifests (`package.json`, `Cargo.toml`, `pyproject.toml`) and directory layout.

Do not invent conventions or unverified facts. Ground all statements in source files.

### 2. Clone the wiki repository
Clone into a temporary workspace:

```bash
git clone https://github.com/<owner>/<repo>.wiki.git /tmp/wiki
```

If the clone fails with HTTP 404, verify the wiki feature is enabled on the remote repository and initialize `Home.md` through the GitHub web UI or API.

### 3. Generate structured pages
Create or update key pages:
- `Home.md`: Project summary, quick reference links, page directory, and source commit hash.
- `Architecture.md`: Component layout, data flow, and directory structure.
- `Setup.md`: Prerequisites, installation steps, build commands, and test suites.
- `Conventions.md`: Code style guidelines, commit rules, and branch workflows.

### 4. Push updates
Review diffs, commit changes with clear summaries, and push to the wiki remote:

```bash
git -C /tmp/wiki add -A
git -C /tmp/wiki commit -m "docs: update wiki from commit <sha>"
git -C /tmp/wiki push origin master
```
