"""Convert parsed highlights into Markdown files."""
import re
from pathlib import Path
from typing import List

from .parser import Book, Highlight


def generate_markdown(book: Book, output_dir: str) -> None:
    """Generate a Markdown file for a book's highlights."""
    output_path = Path(output_dir) / f"{_sanitize_filename(book.title)}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(f"# {book.title}\n\n")
        file.write(f"**Author**: {book.author}\n\n")

        for highlight in book.highlights:
            if highlight.text:
                file.write(f"> {highlight.text}\n\n")
            if highlight.note:
                file.write(f"**Note**: {highlight.note}\n\n")
            if highlight.location or highlight.page or highlight.date:
                metadata = []
                if highlight.location:
                    metadata.append(f"Location: {highlight.location}")
                if highlight.page:
                    metadata.append(f"Page: {highlight.page}")
                if highlight.date:
                    metadata.append(f"Date: {highlight.date.strftime('%Y-%m-%d')}")
                file.write(f"> **{' | '.join(metadata)}**\n\n")
            file.write("---\n\n")


def _sanitize_filename(title: str) -> str:
    """Sanitize the book title for use as a filename."""
    # Replace spaces with underscores and remove invalid characters
    sanitized = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in title).strip()
    # Replace consecutive underscores with a single underscore
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized