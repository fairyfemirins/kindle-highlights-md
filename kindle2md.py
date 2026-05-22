#!/usr/bin/env python3
"""
Kindle Highlights to Markdown CLI Tool

Parses Kindle's "My Clippings.txt" and converts highlights to Markdown.
"""

import re
import argparse
import json
from datetime import datetime
from pathlib import Path


def parse_clippings(input_path):
    """Parse Kindle clippings into structured data."""
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    # Split clippings by separator
    clippings = re.split(r'^==========$', content, flags=re.MULTILINE)
    clippings = [c.strip() for c in clippings if c.strip()]
    
    books = {}
    
    for clipping in clippings:
        # Split into metadata and highlight
        parts = clipping.split('\n', 2)
        if len(parts) < 3:
            continue
        
        metadata, _, highlight = parts
        
        # Parse metadata (title, author, location, timestamp)
        match = re.match(
            r'^(.*?)(?: \((.*?)\))?(?: \| (?:Location|位置) (\d+)(?:-\d+)?(?: \| Added on )?(.*?))?$',
            metadata.strip()
        )
        if not match:
            continue
        
        title, author, location, timestamp = match.groups()
        title = title.strip()
        author = author.strip() if author else "Unknown"
        highlight = highlight.strip()
        
        # Parse timestamp
        try:
            timestamp = datetime.strptime(timestamp, '%A, %B %d, %Y %I:%M:%S %p')
        except (ValueError, TypeError):
            timestamp = None
        
        # Group by book
        if title not in books:
            books[title] = {
                'author': author,
                'highlights': []
            }
        
        books[title]['highlights'].append({
            'content': highlight,
            'location': location,
            'timestamp': timestamp
        })
    
    return books


def to_markdown(books, output_path=None):
    """Convert parsed clippings to Markdown."""
    markdown = "# Kindle Highlights\n\n"
    
    for title, data in books.items():
        markdown += f"## {title} ({data['author']})\n\n"
        for highlight in data['highlights']:
            markdown += f"> {highlight['content']}\n"
            if highlight['location']:
                markdown += f"\n*Location: {highlight['location']}*\n"
            if highlight['timestamp']:
                markdown += f"\n*Added on: {highlight['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}*\n"
            markdown += "\n\n"
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
    
    return markdown


def main():
    parser = argparse.ArgumentParser(description='Convert Kindle highlights to Markdown.')
    parser.add_argument('--input', required=True, help='Path to "My Clippings.txt"')
    parser.add_argument('--output', help='Output Markdown file (default: stdout)')
    parser.add_argument('--json', action='store_true', help='Output as JSON instead of Markdown')
    
    args = parser.parse_args()
    
    books = parse_clippings(args.input)
    
    if args.json:
        output = json.dumps(books, indent=2, default=str)
    else:
        output = to_markdown(books, args.output)
    
    if not args.output:
        print(output)


if __name__ == '__main__':
    main()