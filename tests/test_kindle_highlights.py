"""Unit tests for the Kindle Highlights to Markdown tool."""
import pytest
from datetime import datetime
from pathlib import Path

from kindle_highlights_to_markdown.parser import parse_clippings, Book, Highlight
from kindle_highlights_to_markdown.markdown_generator import generate_markdown


@pytest.fixture
def mock_clippings_file():
    return "tests/mock_clippings.txt"


def test_parse_clippings(mock_clippings_file):
    books = parse_clippings(mock_clippings_file)
    assert len(books) == 2

    # Test first book
    book1 = books[0]
    assert book1.title == "Sample Book Title"
    assert book1.author == "Sample Author"
    assert len(book1.highlights) == 2

    # Test first highlight
    highlight1 = book1.highlights[0]
    assert highlight1.text == "This is a highlighted text."
    assert highlight1.location == 123
    assert highlight1.date == datetime(2023, 10, 1, 12, 0, 0)
    assert highlight1.note is None

    # Test note
    note1 = book1.highlights[1]
    assert note1.text == ""
    assert note1.note == "This is a note."

    # Test second book
    book2 = books[1]
    assert book2.title == "Another Book"
    assert book2.author == "Another Author"
    assert len(book2.highlights) == 1

    highlight2 = book2.highlights[0]
    assert highlight2.text == "This is another highlight."
    assert highlight2.location == 456
    assert highlight2.page == 45


def test_generate_markdown(tmp_path):
    book = Book(
        title="Test Book",
        author="Test Author",
        highlights=[
            Highlight(
                text="Test highlight.",
                location=1,
                date=datetime(2023, 1, 1, 12, 0, 0),
            )
        ],
    )
    generate_markdown(book, str(tmp_path))

    output_file = tmp_path / "Test_Book.md"
    assert output_file.exists()
    content = output_file.read_text()
    assert "# Test Book" in content
    assert "Test highlight." in content
    assert "Location: 1" in content
    assert "2023-01-01" in content