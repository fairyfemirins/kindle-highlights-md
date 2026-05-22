# Kindle Highlights to Markdown

A CLI tool to convert Kindle's "My Clippings.txt" into structured Markdown notes.

## Features
- Parse Kindle's "My Clippings.txt" into structured JSON.
- Convert highlights to Markdown (book title as H1, highlights as bullet points).
- Support for metadata (location, date, page).
- Output to file or stdout.

## Installation
```bash
pip install --user .
```

## Usage
```bash
kindle2md --input "My Clippings.txt" --output notes.md
```

## License
MIT