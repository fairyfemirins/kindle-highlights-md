"""CLI interface for the Kindle Highlights to Markdown tool."""
import click
from pathlib import Path

from .markdown_generator import generate_markdown
from .parser import parse_clippings


@click.command()
@click.option('--input', '-i', type=click.Path(exists=True), required=True, help='Path to My Clippings.txt')
@click.option('--output', '-o', type=click.Path(), required=True, help='Output directory for Markdown files')
def main(input: str, output: str) -> None:
    """Convert Kindle highlights to Markdown files."""
    books = parse_clippings(input)
    for book in books:
        generate_markdown(book, output)
    click.echo(f"Generated {len(books)} Markdown files in {output}")


if __name__ == '__main__':
    main()