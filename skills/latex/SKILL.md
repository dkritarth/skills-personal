---
name: latex
version: 0.2.0
description: Focused LaTeX utility for compile-error log triage, bibliography validation, and venue template setup. Identifies precise error source files and lines from engine logs.
license: MIT
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
disable-model-invocation: true
---

# LaTeX

Targeted assistance for LaTeX compilation triage, BibTeX hygiene, and venue formatting.

## Scope

This skill covers three specific tasks:
1. Parsing messy compiler logs down to the exact offending source file and line.
2. Checking `.bib` files for duplicate keys and missing required citation fields.
3. Setting up paper skeletons matching conference and journal submission standards.

Do not use this skill for general conversational LaTeX tutorials or mathematical proof checking (use `math`).

## When to use

- A LaTeX build fails and produces an error log (`.log`).
- Auditing citations and `.bib` records prior to submission.
- Bootstrapping a manuscript template for target venues.

## Process

### 1. Compile log triage
Run the log parser against your build log:

```bash
python3 scripts/parse_log.py path/to/compile.log
```

The script tracks open TeX source files through nested parentheses and matches `!` error lines to source locations (`<file>:<line>: <message>`). Inspect the reported file and line directly before modifying code.

### 2. Bibliography validation
Audit reference files before compilation:

```bash
python3 scripts/bib_lint.py references.bib
```

Flags duplicated citation keys and reports entries missing fields mandated by standard BibTeX entry types (such as missing `author`, `title`, `journal`, or `year` in `@article`).

### 3. Venue templates
Use `templates/generic-article/main.tex` as a clean starting point, or adapt specific venue templates under `templates/<venue>-<year>/`. Keep macro definitions minimal and separate from main content.

## Scripts

- `scripts/parse_log.py <compile.log>`: Standard library Python script for pinpointing LaTeX errors.
- `scripts/bib_lint.py <file.bib>`: Standard library Python script for checking BibTeX entry integrity.
