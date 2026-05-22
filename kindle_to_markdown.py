#!/usr/bin/env python3
"""
Kindle Highlights to Markdown Converter

Parses Kindle "My Clippings.txt" and converts highlights into structured Markdown.
Supports multi-language metadata (Location/位置), deduplication, and customizable output.
"""

import re
import sys
from datetime import datetime
from pathlib import Path


def parse_clippings(file_path: str) -> list:
    """Parse Kindle "My Clippings.txt" into a list of structured highlights."""
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()
    
    # Split clippings by separator
    clippings = re.split(r'==========\s*', content)
    highlights = []
    
    for clipping in clippings:
        clipping = clipping.strip()
        if not clipping:
            continue
        
        # Parse metadata (title, author, location, timestamp)
        metadata_match = re.match(
            r'^(.*?)(?: \((.*?)\))?(?: \| (?:Location|位置) (\d+)(?:-\d+)?(?: \| Added on )?(.*?))?$',
            clipping.split('\n')[0].strip()
        )
        if not metadata_match:
            continue
        
        book_title = metadata_match.group(1).strip()
        author = metadata_match.group(2).strip() if metadata_match.group(2) else "Unknown Author"
        # Extract timestamp from metadata line
        timestamp_match = re.search(r'Added on (.*?)$', clipping.split('\n')[0])
        timestamp = timestamp_match.group(1).strip() if timestamp_match else "Unknown Date"
        
        # Extract location from metadata line
        location_match = re.search(r'(?:Location|位置) (\d+(?:-\d+)?)', clipping.split('\n')[1])
        location = location_match.group(1).strip() if location_match else "Unknown Location"
        
        # Parse highlight content (skip metadata line)
        highlight_lines = clipping.split('\n')[2:]
        highlight_content = '\n'.join([line.strip() for line in highlight_lines if line.strip()])
        
        if not highlight_content:
            continue
        
        highlights.append({
            "book_title": book_title,
            "author": author,
            "location": location,
            "timestamp": timestamp,
            "content": highlight_content
        })
    
    return highlights


def deduplicate_highlights(highlights: list) -> list:
    """Remove duplicate highlights (same content)."""
    seen = set()
    unique_highlights = []
    
    for highlight in highlights:
        content = highlight["content"]
        if content not in seen:
            seen.add(content)
            unique_highlights.append(highlight)
    
    return unique_highlights


def generate_markdown(highlights: list) -> str:
    """Convert highlights into Markdown format."""
    markdown = "# Kindle Highlights\n\n"
    
    # Group highlights by book
    books = {}
    for highlight in highlights:
        book_key = (highlight["book_title"], highlight["author"])
        if book_key not in books:
            books[book_key] = []
        books[book_key].append(highlight)
    
    # Generate Markdown for each book
    for (book_title, author), book_highlights in books.items():
        markdown += f"## {book_title} ({author})\n\n"
        for highlight in book_highlights:
            markdown += f"> {highlight['content']}\n\n"
            # Add metadata as a comment
            metadata = f"Location: {highlight['location']}"
            if highlight["timestamp"] != "Unknown Date":
                try:
                    # Parse and reformat timestamp
                    dt = datetime.strptime(highlight["timestamp"], "%A, %B %d, %Y %I:%M:%S %p")
                    metadata += f" | Added on: {dt.strftime('%Y-%m-%d %H:%M:%S')}"
                except ValueError:
                    metadata += f" | Added on: {highlight['timestamp']}"
            markdown += f"<!-- {metadata} -->\n\n"
    
    return markdown


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python kindle_to_markdown.py <path_to_My_Clippings.txt>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    
    highlights = parse_clippings(file_path)
    unique_highlights = deduplicate_highlights(highlights)
    markdown = generate_markdown(unique_highlights)
    
    output_path = Path(file_path).stem + "_highlights.md"
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(markdown)
    
    print(f"Successfully converted highlights to Markdown: {output_path}")


if __name__ == "__main__":
    main()