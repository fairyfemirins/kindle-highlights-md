# kindle-highlights-md

Convert Kindle's `My Clippings.txt` into structured Markdown notes.

## Features
- Parse `My Clippings.txt` into Markdown.
- Group highlights by book.
- Support for notes, highlights, and bookmarks.
- CLI interface for easy use.
- Output to file or stdout.

## Installation
```bash
pip install --user git+https://github.com/fairyfemirins/kindle-highlights-md.git
```

## Usage
```bash
# Convert to Markdown and save to file
kindle-highlights-md /path/to/My\ Clippings.txt output.md

# Print to terminal
kindle-highlights-md /path/to/My\ Clippings.txt
```

## Example
### Input (`My Clippings.txt`)
```
The Pragmatic Programmer (Andrew Hunt)
- Your Highlight on page 42 | Location 123-124 | Added on Friday, May 22, 2026 12:00:00 PM

This is a highlight.\n==========\n```

### Output (`output.md`)
```markdown
# Kindle Highlights

## The Pragmatic Programmer

### Highlight
- **Page**: 42
- **Location**: 123-124
- **Date**: Friday, May 22, 2026 12:00:00 PM

> This is a highlight.
```

## License
MIT