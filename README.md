# Kindle Highlights to Markdown Converter

A tool to convert Kindle's "My Clippings.txt" file into structured Markdown notes for easy integration into note-taking systems or blogs.

## Features
- Parses `My Clippings.txt` into book titles, highlights, notes, and metadata.
- Converts highlights into clean Markdown with blockquotes and metadata.
- Supports Unicode and special characters.

## Usage
### Prerequisites
- Python 3.6+

### Installation
Clone the repository:
```bash
git clone https://github.com/Femirins/kindle-highlights-to-markdown.git
cd kindle-highlights-to-markdown
```

### Convert Clippings
```bash
python3 kindle_to_md.py "My Clippings.txt" output.md
```

### Example
**Input (`My Clippings.txt`):**
```
The Pragmatic Programmer: Your Journey to Mastery (Andrew Hunt)
- Your Highlight on page 123 | Added on Tuesday, May 14, 2026 9:28:25 PM

The most important thing is to **think** about what you're doing.\n==========
```

**Output (`output.md`):**
```markdown
# The Pragmatic Programmer: Your Journey to Mastery (Andrew Hunt)

> **Your Highlight on page 123** | Added on Tuesday, May 14, 2026 9:28:25 PM

> The most important thing is to **think** about what you're doing.

---
```

## Technical Architecture
### Parsing Logic
1. **Splitting Clippings:** The `My Clippings.txt` file is split into individual clippings using the `==========` delimiter.
2. **Metadata Extraction:** Each clipping is parsed to extract:
   - Book title
   - Clipping type (highlight, note, or bookmark)
   - Date added
   - Highlight or note text
3. **Markdown Generation:** The parsed data is converted into Markdown with:
   - Book titles as headers (`#`)
   - Metadata as bold text (`** **`)
   - Highlights/notes as blockquotes (`> `)

### Error Handling
- Skips malformed clippings (e.g., missing metadata or text).
- Handles Unicode and special characters using `utf-8-sig` encoding.

## License
This project is licensed under the **MIT License**.