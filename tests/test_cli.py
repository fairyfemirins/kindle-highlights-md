import pytest
import tempfile
from kindle_highlights_md.cli import parse_clippings, Highlight, group_by_book, generate_markdown


def test_parse_clippings():
    # Sample My Clippings.txt content (realistic formatting)
    sample = """The Pragmatic Programmer (Andrew Hunt)
- Your Highlight on page 42 | Location 123-124 | Added on Friday, May 22, 2026 12:00:00 PM

This is a highlight.\n==========\nThe Pragmatic Programmer (Andrew Hunt)
- Your Note on Location 125 | Added on Friday, May 22, 2026 12:05:00 PM

This is a note.\n==========\n"""
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8-sig', delete=False) as f:
        f.write(sample)
        temp_path = f.name

    highlights = parse_clippings(temp_path)
    assert len(highlights) == 2
    
    # Test highlight
    assert highlights[0].book_title == "The Pragmatic Programmer"
    assert highlights[0].content == "This is a highlight."
    assert highlights[0].page == "42"
    assert highlights[0].location == "123-124"
    assert highlights[0].type == "highlight"
    
    # Test note
    assert highlights[1].book_title == "The Pragmatic Programmer"
    assert highlights[1].content == "This is a note."
    assert highlights[1].page == "N/A"
    assert highlights[1].location == "125"
    assert highlights[1].type == "note"


def test_group_by_book():
    highlights = [
        Highlight(
            book_title="Book 1",
            content="Highlight 1",
            page="42",
            location="123-124",
            date="Friday, May 22, 2026 12:00:00 PM",
            type="highlight"
        ),
        Highlight(
            book_title="Book 2",
            content="Highlight 2",
            page="43",
            location="125-126",
            date="Friday, May 22, 2026 12:05:00 PM",
            type="highlight"
        ),
        Highlight(
            book_title="Book 1",
            content="Note 1",
            page="N/A",
            location="127",
            date="Friday, May 22, 2026 12:10:00 PM",
            type="note"
        )
    ]
    
    books = group_by_book(highlights)
    assert len(books) == 2
    assert len(books["Book 1"]) == 2
    assert len(books["Book 2"]) == 1


def test_generate_markdown():
    books = {
        "The Pragmatic Programmer": [
            Highlight(
                book_title="The Pragmatic Programmer",
                content="This is a highlight.",
                page="42",
                location="123-124",
                date="Friday, May 22, 2026 12:00:00 PM",
                type="highlight"
            )
        ]
    }
    
    md = generate_markdown(books)
    assert "# Kindle Highlights" in md
    assert "## The Pragmatic Programmer" in md
    assert "### Highlight" in md
    assert "> This is a highlight." in md