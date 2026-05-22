# Technical Architecture

## Overview
This tool parses Kindle's "My Clippings.txt" and converts highlights to Markdown or JSON. It is designed for **reusability**, **multi-language support**, and **CLI-based workflows**.

## Components

### 1. Parser (`parse_clippings`)
- **Input**: Path to "My Clippings.txt"
- **Output**: Structured data (Python dict)
- **Key Features**:
  - Regex-based parsing for **multi-language metadata** (`Location` vs `位置`).
  - Deduplication via **unique content hashing** (not implemented in MVP, but planned).
  - Timestamp parsing (optional).

### 2. Markdown Generator (`to_markdown`)
- **Input**: Structured data from `parse_clippings`
- **Output**: Markdown-formatted highlights
- **Key Features**:
  - Book title as **H1**, author in parentheses.
  - Highlights as **blockquotes**.
  - Metadata (location, timestamp) as *italic*.

### 3. CLI (`main`)
- **Arguments**:
  - `--input`: Path to "My Clippings.txt" (required).
  - `--output`: Output file (optional, defaults to stdout).
  - `--json`: Output as JSON instead of Markdown.

## Edge Cases Handled
- **Multi-language metadata**: Regex alternation for `Location`/`位置`.
- **Missing authors**: Defaults to "Unknown".
- **Empty clippings**: Skips malformed entries.
- **Duplicate highlights**: Planned for future (SQLite deduplication).

## Future Work
- **SQLite deduplication**: Store highlights in a database with `UNIQUE` constraints.
- **Obsidian/Logseq integration**: Direct export to note-taking apps.
- **GUI wrapper**: Optional Tkinter/Qt interface for non-CLI users.

---

# Reproducible Tutorial

## Step 1: Clone the Repository
```bash
cd ~ && git clone https://github.com/femirins/kindle-highlights-to-markdown.git
cd kindle-highlights-to-markdown
```

## Step 2: Install Dependencies
```bash
pip install --user pytest
```

## Step 3: Run Tests
```bash
python3 -m pytest test_kindle2md.py -v
```

## Step 4: Test with Sample Data
1. Create a sample clippings file:
   ```bash
   cat > sample_clippings.txt << 'EOF'
   The Pragmatic Programmer (Andrew Hunt)
   - Your Highlight on Location 123-124 | Added on Sunday, May 17, 2026 12:00:00 AM
   
   The most important thing is to THINK about what you read.
   ==========
   
   原子习惯 (James Clear)
   - Your Highlight on 位置 456-457 | Added on Sunday, May 17, 2026 12:01:00 AM
   
   You do not rise to the level of your goals. You fall to the level of your systems.
   ==========
   EOF
   ```

2. Run the tool:
   ```bash
   python3 kindle2md.py --input sample_clippings.txt --output highlights.md
   ```

3. View the output:
   ```bash
   cat highlights.md
   ```

## Step 5: Use with Your Kindle Data
1. Copy "My Clippings.txt" from your Kindle:
   ```bash
   cp /media/Kindle/documents/My\ Clippings.txt ~/kindle_clippings.txt
   ```

2. Convert to Markdown:
   ```bash
   python3 kindle2md.py --input ~/kindle_clippings.txt --output ~/kindle_highlights.md
   ```

3. (Optional) Convert to JSON:
   ```bash
   python3 kindle2md.py --input ~/kindle_clippings.txt --json > ~/kindle_highlights.json
   ```