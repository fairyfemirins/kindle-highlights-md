# Kindle Highlights to Markdown CLI

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A **standalone CLI tool** to parse Kindle's `My Clippings.txt`, deduplicate highlights, and export them to **Markdown** or an **Obsidian vault**.

## Features

- **Deduplication**: Remove duplicate highlights (same book, location, and content).
- **Markdown Export**: One file per book with clean formatting.
- **Obsidian Integration**: Export directly to an Obsidian vault.
- **Non-Interactive**: Designed for automation and scripting.

## Note

This repository was published under `fairyfemirins` due to GitHub namespace restrictions. A transfer to `femirins` is pending.

To request a transfer, open an issue in this repository or contact `@femirins` on GitHub.

---

## Installation

```bash
git clone https://github.com/fairyfemirins/kindle-highlights-md.git
cd kindle-highlights-md
pip install click rich
```

## Usage

### Basic Export
```bash
python kindle_highlights.py --input "My Clippings.txt" --output output
```

### Deduplication
```bash
python kindle_highlights.py --input "My Clippings.txt" --output output --dedupe
```

### Obsidian Integration
```bash
python kindle_highlights.py --input "My Clippings.txt" --obsidian "~/obsidian_vault/Kindle"
```

## Example Output

**`The Pragmatic Programmer_Andrew Hunt.md`**

```markdown
# The Pragmatic Programmer: Your Journey to Mastery (Andrew Hunt)

> Debugging is twice as hard as writing the code in the first place.

**Location:** 123

---
```

## Technical Architecture

1. **Parsing**: Uses regex to split `My Clippings.txt` into entries and extract metadata (book title, location, page, content).
2. **Deduplication**: Generates a unique key for each highlight (`book_title + location + content`) and filters duplicates.
3. **Export**: Writes one Markdown file per book with proper formatting for Obsidian compatibility.

## Limitations

- Only supports **English-language** Kindle clippings (metadata format varies by language).
- Does not support **bookmarks** or **notes** (highlights only).

## License

MIT