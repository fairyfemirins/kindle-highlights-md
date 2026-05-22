import re
from dataclasses import dataclass
from typing import List, Dict
import click


@dataclass
class Highlight:
    book_title: str
    content: str
    page: str
    location: str
    date: str
    type: str  # highlight, note, or bookmark


def parse_clippings(file_path: str) -> List[Highlight]:
    """Parse Kindle's My Clippings.txt into a list of Highlight objects."""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Split into entries
    entries = re.split(r'==========\n', content)
    entries = [e.strip() for e in entries if e.strip()]

    highlights = []
    for entry in entries:
        lines = entry.split('\n')
        if len(lines) < 4:
            continue

        # Parse metadata
        metadata = lines[0].strip()
        match = re.match(
            r'^(?P<title>.+) \((?P<author>.+)\)$',
            metadata
        )
        if not match:
            continue
        book_title = match.group('title').strip()

        # Parse location and date
        location_line = lines[1].strip()
        location_match = re.match(
            r'^\s{0,4}- (?P<type>Your (Highlight|Note|Bookmark)) (?:on|at) (?:page (?P<page>\d+) \| )?Location (?P<location>\d+-\d+|\d+) \| Added on (?P<date>.+)$',
            location_line
        )
        if not location_match:
            continue

        highlight_type = location_match.group('type').lower().replace('your ', '').replace(' ', '_')
        page = location_match.group('page') or 'N/A'
        location = location_match.group('location')
        date = location_match.group('date')

        # Parse content
        content = '\n'.join(lines[3:]).strip()

        highlights.append(
            Highlight(
                book_title=book_title,
                content=content,
                page=page,
                location=location,
                date=date,
                type=highlight_type
            )
        )

    return highlights


def group_by_book(highlights: List[Highlight]) -> Dict[str, List[Highlight]]:
    """Group highlights by book title."""
    books = {}
    for h in highlights:
        if h.book_title not in books:
            books[h.book_title] = []
        books[h.book_title].append(h)
    return books


def generate_markdown(books: Dict[str, List[Highlight]]) -> str:
    """Generate Markdown from grouped highlights."""
    md = "# Kindle Highlights\n\n"
    for book_title, highlights in books.items():
        md += f"## {book_title}\n\n"
        for h in highlights:
            md += f"### {h.type.replace('_', ' ').title()}\n"
            md += f"- **Page**: {h.page}\n"
            md += f"- **Location**: {h.location}\n"
            md += f"- **Date**: {h.date}\n"
            md += f"\n> {h.content}\n\n"
        md += "\n---\n\n"
    return md


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path(), required=False)
def main(input_file: str, output_file: str):
    """Convert Kindle's My Clippings.txt to Markdown."""
    highlights = parse_clippings(input_file)
    books = group_by_book(highlights)
    md = generate_markdown(books)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md)
        click.echo(f"Markdown saved to {output_file}")
    else:
        click.echo(md)


if __name__ == '__main__':
    main()