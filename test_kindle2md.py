#!/usr/bin/env python3
"""
Test cases for Kindle Highlights to Markdown CLI Tool
"""

import pytest
import tempfile
import json
from pathlib import Path
from kindle2md import parse_clippings, to_markdown


def test_parse_clippings():
    """Test parsing of Kindle clippings."""
    sample = """The Pragmatic Programmer (Andrew Hunt)
- Your Highlight on Location 123-124 | Added on Sunday, May 17, 2026 12:00:00 AM

The most important thing is to THINK about what you read.
==========

原子习惯 (James Clear)
- Your Highlight on 位置 456-457 | Added on Sunday, May 17, 2026 12:01:00 AM

You do not rise to the level of your goals. You fall to the level of your systems.
=========="""
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(sample)
        f.flush()
        
        books = parse_clippings(f.name)
        
        assert len(books) == 2
        assert 'The Pragmatic Programmer' in books
        assert books['The Pragmatic Programmer']['author'] == 'Andrew Hunt'
        assert len(books['The Pragmatic Programmer']['highlights']) == 1
        assert books['The Pragmatic Programmer']['highlights'][0]['content'] == 'The most important thing is to THINK about what you read.'
        
        assert '原子习惯' in books
        assert books['原子习惯']['author'] == 'James Clear'
        assert len(books['原子习惯']['highlights']) == 1
        assert books['原子习惯']['highlights'][0]['content'] == 'You do not rise to the level of your goals. You fall to the level of your systems.'


def test_to_markdown():
    """Test conversion to Markdown."""
    books = {
        'The Pragmatic Programmer': {
            'author': 'Andrew Hunt',
            'highlights': [
                {
                    'content': 'The most important thing is to THINK about what you read.',
                    'location': '123',
                    'timestamp': None
                }
            ]
        }
    }
    
    markdown = to_markdown(books)
    assert '# Kindle Highlights' in markdown
    assert '## The Pragmatic Programmer (Andrew Hunt)' in markdown
    assert '> The most important thing is to THINK about what you read.' in markdown


def test_json_output():
    """Test JSON output."""
    books = {
        'The Pragmatic Programmer': {
            'author': 'Andrew Hunt',
            'highlights': [
                {
                    'content': 'The most important thing is to THINK about what you read.',
                    'location': '123',
                    'timestamp': None
                }
            ]
        }
    }
    
    output = json.dumps(books, indent=2, default=str)
    data = json.loads(output)
    
    assert data['The Pragmatic Programmer']['author'] == 'Andrew Hunt'
    assert len(data['The Pragmatic Programmer']['highlights']) == 1


if __name__ == '__main__':
    pytest.main([__file__])