#!/usr/bin/env python3
"""
Kindle Highlights to Markdown CLI

Parses Kindle's "My Clippings.txt", deduplicates highlights, and exports to Markdown.
Supports Obsidian vault integration.
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Tuple
import click
from rich.console import Console
from rich.table import Table

console = Console()

# --- Constants ---
CLIPPINGS_FILE = "My Clippings.txt"
OUTPUT_DIR = "output"
OBSIDIAN_DIR = "obsidian_vault"

# --- Data Models ---
class Highlight:
    def __init__(self, book_title: str, content: str, location: str, page: str = ""):
        self.book_title = book_title.strip()
        self.content = content.strip()
        self.location = location.strip()
        self.page = page.strip()
        self.key = f"{book_title}_{location}_{content}"  # Deduplication key

    def __repr__(self):
        return f"Highlight(book='{self.book_title}', content='{self.content[:30]}...')"

# --- Parsing Logic ---
def parse_clippings(file_path: str) -> List[Highlight]:
    """Parse Kindle's My Clippings.txt into a list of Highlight objects."""
    with open(file_path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    
    # Split into entries (Kindle separates entries with "==========")
    entries = re.split(r"==========", content)
    highlights = []
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        # Extract book title, content, and metadata
        lines = entry.split("\n")
        if len(lines) < 3:
            continue
        
        book_title = lines[0].strip()
        metadata_line = lines[1].strip()
        content = "\n".join(lines[3:]).strip()
        
        # Parse metadata (e.g., "- Your Highlight on Location 123-124 | Added on Monday, June 1, 2026")
        location_match = re.search(r"Location (\d+)(?:-(\d+))?", metadata_line)
        page_match = re.search(r"page (\d+)", metadata_line, re.IGNORECASE)
        
        location = location_match.group(1) if location_match else ""
        page = page_match.group(1) if page_match else ""
        
        if content and book_title:
            highlights.append(Highlight(book_title, content, location, page))
    
    return highlights

# --- Deduplication ---
def deduplicate_highlights(highlights: List[Highlight]) -> List[Highlight]:
    """Remove duplicate highlights (same book, location, and content)."""
    seen = set()
    unique_highlights = []
    
    for highlight in highlights:
        if highlight.key not in seen:
            seen.add(highlight.key)
            unique_highlights.append(highlight)
    
    return unique_highlights

# --- Export Logic ---
def export_to_markdown(highlights: List[Highlight], output_dir: str) -> None:
    """Export highlights to Markdown files (one per book)."""
    os.makedirs(output_dir, exist_ok=True)
    books = {}
    
    for highlight in highlights:
        if highlight.book_title not in books:
            books[highlight.book_title] = []
        books[highlight.book_title].append(highlight)
    
    for book_title, book_highlights in books.items():
        # Sanitize filename
        safe_title = re.sub(r"[^a-zA-Z0-9 ]", "_", book_title)
        filename = f"{safe_title}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {book_title}\n\n")
            for highlight in book_highlights:
                f.write(f"> {highlight.content}\n")
                if highlight.location or highlight.page:
                    f.write("\n")
                    if highlight.location:
                        f.write(f"**Location:** {highlight.location}\n")
                    if highlight.page:
                        f.write(f"**Page:** {highlight.page}\n")
                f.write("\n---\n\n")

# --- Obsidian Integration ---
def export_to_obsidian(highlights: List[Highlight], vault_dir: str) -> None:
    """Export highlights to Obsidian vault format."""
    export_to_markdown(highlights, vault_dir)

# --- CLI ---
@click.command()
@click.option("--input", "-i", type=click.Path(exists=True), required=True, help="Path to My Clippings.txt")
@click.option("--output", "-o", type=click.Path(), default=OUTPUT_DIR, help="Output directory for Markdown files")
@click.option("--obsidian", "-v", type=click.Path(), help="Obsidian vault directory (enables Obsidian integration)")
@click.option("--dedupe/--no-dedupe", default=True, help="Enable deduplication (default: enabled)")
def cli(input: str, output: str, obsidian: str, dedupe: bool) -> None:
    """Kindle Highlights to Markdown CLI"""
    console.print("[bold green]📚 Kindle Highlights to Markdown[/bold green]")
    
    # Parse highlights
    console.print(f"🔍 Parsing {input}...")
    highlights = parse_clippings(input)
    console.print(f"✅ Found {len(highlights)} highlights")
    
    # Deduplicate
    if dedupe:
        highlights = deduplicate_highlights(highlights)
        console.print(f"🧹 Deduplicated to {len(highlights)} highlights")
    
    # Export
    if obsidian:
        console.print(f"📁 Exporting to Obsidian vault: {obsidian}")
        export_to_obsidian(highlights, obsidian)
    else:
        console.print(f"📁 Exporting to {output}")
        export_to_markdown(highlights, output)
    
    console.print("[bold green]✨ Done![/bold green]")

if __name__ == "__main__":
    cli()