"""Parse Kindle's 'My Clippings.txt' into structured data."""
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Highlight:
    text: str
    location: Optional[int] = None
    page: Optional[int] = None
    date: Optional[datetime] = None
    note: Optional[str] = None


@dataclass
class Book:
    title: str
    author: str
    highlights: List[Highlight]


def parse_clippings(file_path: str) -> List[Book]:
    """Parse 'My Clippings.txt' and return a list of Book objects."""
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()

    # Split clippings by separator
    clippings = re.split(r'==========\n', content)
    books = {}

    for clipping in clippings:
        if not clipping.strip():
            continue

        # Extract metadata
        lines = clipping.strip().split('\n')
        if len(lines) < 3:
            continue

        title_author = lines[0].strip()
        metadata = lines[1].strip()
        text = '\n'.join(lines[3:]).strip()

        # Parse title and author
        title, author = _parse_title_author(title_author)

        # Parse metadata (location, date)
        location, page, date = _parse_metadata(metadata)

        # Determine if this is a highlight or note
        is_note = "Your Note" in metadata
        highlight_text = text if not is_note else ""
        note_text = text if is_note else ""

        # Add to book
        if title not in books:
            books[title] = Book(title=title, author=author, highlights=[])

        highlight = Highlight(
            text=highlight_text,
            location=location,
            page=page,
            date=date,
            note=note_text if is_note else None,
        )
        books[title].highlights.append(highlight)

    return list(books.values())


def _parse_title_author(title_author: str) -> tuple:
    """Extract title and author from the first line."""
    # Handle cases like "Title (Author)"
    match = re.match(r'^(.*?)\s*\((.*?)\)$', title_author)
    if match:
        return match.group(1), match.group(2)
    return title_author, "Unknown Author"


def _parse_metadata(metadata: str) -> tuple:
    """Extract location, page, and date from metadata line."""
    location = None
    page = None
    date = None

    # Extract location
    loc_match = re.search(r'Location (\d+)', metadata)
    if loc_match:
        location = int(loc_match.group(1))

    # Extract page
    page_match = re.search(r'page (\d+)', metadata, re.IGNORECASE)
    if page_match:
        page = int(page_match.group(1))

    # Extract date
    date_match = re.search(
        r'(Added on|on) (\w+,\s*\w+\s*\d+,\s*\d+\s*\d+:\d+:\d+\s*[AP]M)', metadata
    )
    if date_match:
        date_str = date_match.group(2)
        try:
            date = datetime.strptime(date_str, '%A, %B %d, %Y %I:%M:%S %p')
        except ValueError:
            pass

    return location, page, date