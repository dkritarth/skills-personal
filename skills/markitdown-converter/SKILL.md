---
name: markitdown-converter
version: 1.0.0
description: Convert documents (PDF, Word, Excel, PowerPoint, HTML, etc.) to markdown using Microsoft's markitdown library, then read the markdown output instead of binary files
license: MIT
compatibility: claude-code codex morphmind opencode
allowed-tools: [Read, Write, Edit, Bash]
auto-invoke: ['\.pdf$', '\.docx?$', '\.xlsx?$', '\.pptx?$', '\.html?$']
---

# Markitdown Converter Skill

Automatically convert documents to markdown before reading them. Supports PDFs, Word docs, Excel spreadsheets, PowerPoint presentations, HTML, and more.

## Setup

Requires Python 3.10+ and the `markitdown` package.

```bash
pip install markitdown
```

Optional dependencies for specific formats:
- **Audio transcription**: `pip install "markitdown[audio]"` (requires ffmpeg)
- **YouTube transcription**: `pip install "markitdown[youtube]"`
- **Office formats (doc, ppt)**: LibreOffice (system package)

## How It Works

When any tool needs to inspect a binary document format (PDF, DOCX, XLSX, PPTX, HTML):

1. Instead of reading raw bytes, run `markitdown` via the conversion script
2. The script outputs clean markdown to stdout or a cached `.md` file alongside the original
3. Read the markdown output using the standard Read tool
4. Do not commit generated markdown files unless explicitly asked

## Conversion Script

Use `scripts/convert.py` to convert files:

```bash
# Convert to stdout
python3 scripts/convert.py path/to/document.pdf

# Convert to file (defaults to <name>.converted.md alongside source)
python3 scripts/convert.py path/to/document.docx -o output.md

# Convert with LLM-enhanced image descriptions (requires OPENAI_API_KEY)
python3 scripts/convert.py path/to/slides.pptx --use-llm
```

## Supported Formats

| Extension | Format | Engine |
|-----------|--------|--------|
| `.pdf` | PDF documents | pdfminer.six |
| `.docx`, `.doc` | Word documents | python-docx / LibreOffice |
| `.xlsx`, `.xls` | Excel spreadsheets | openpyxl / xlrd |
| `.pptx`, `.ppt` | PowerPoint slides | python-pptx / LibreOffice |
| `.html`, `.htm` | Web pages | BeautifulSoup4 |
| `.csv`, `.tsv` | Tabular data | pandas |
| `.json`, `.xml` | Structured data | built-in parsers |
| `.zip` | Archives | extracts and converts contents |
| `.mp3`, `.wav` | Audio (speech-to-text) | speech_recognition |

## Best Practices

- **Large PDFs**: If a PDF is > 50 pages, convert specific page ranges if supported, or grep the converted markdown rather than reading the whole file into context.
- **Spreadsheets**: MarkItDown formats sheets as markdown tables. Very wide tables may wrap awkwardly; consider querying specific columns or rows if needed.
- **Images in documents**: By default, embedded images produce placeholder text. Pass `--use-llm` if image contents (diagrams, charts) are essential to the task.
