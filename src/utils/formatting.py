"""
Formatting utilities for the Marketing Analyst Agent CLI.
"""

import re
from typing import Dict, Any, List, Optional, Union


def format_cli_response(text: str) -> str:
    """
    Format the response text for CLI output with proper spacing,
    highlighting, and breaks for readability.
    
    Args:
        text: The response text to format
        
    Returns:
        Formatted text for CLI display
    """
    # Add proper line breaks
    text = re.sub(r'(\d+\.\s[^\n]+)(?=\d+\.)', r'\1\n\n', text)
    
    # Add spacing after headers
    text = re.sub(r'(#+\s[^\n]+)\n', r'\1\n\n', text)
    
    # Add spacing for bullet points
    text = re.sub(r'(\*\s[^\n]+)(?=\*\s)', r'\1\n', text)
    
    return text


def format_table(headers: List[str], rows: List[List[str]], title: Optional[str] = None) -> str:
    """
    Create an ASCII table for displaying structured data in the CLI.
    
    Args:
        headers: List of column headers
        rows: List of rows, each a list of string values
        title: Optional title for the table
        
    Returns:
        Formatted ASCII table as a string
    """
    if not rows:
        return "No data available."
    
    # Determine column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Create table format
    separator = '+' + '+'.join(['-' * (width + 2) for width in col_widths]) + '+'
    header_row = '|' + '|'.join([f' {h:<{col_widths[i]}} ' for i, h in enumerate(headers)]) + '|'
    
    # Build the table
    table = []
    if title:
        title_width = len(separator) - 2
        table.append(separator)
        table.append(f"|{title.center(title_width)}|")
    
    table.append(separator)
    table.append(header_row)
    table.append(separator)
    
    for row in rows:
        row_str = '|' + '|'.join([f' {str(cell):<{col_widths[i]}} ' for i, cell in enumerate(row)]) + '|'
        table.append(row_str)
    
    table.append(separator)
    
    return '\n'.join(table)


def highlight_text(text: str, highlights: List[str]) -> str:
    """
    Highlight specified terms in the text (when terminal supports it).
    
    Args:
        text: The text to highlight
        highlights: List of terms to highlight
        
    Returns:
        Text with highlighted terms
    """
    # ANSI color codes
    HIGHLIGHT_START = "\033[1;33m"  # Bold yellow
    HIGHLIGHT_END = "\033[0m"       # Reset
    
    result = text
    for term in highlights:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        result = pattern.sub(f"{HIGHLIGHT_START}\\g<0>{HIGHLIGHT_END}", result)
    
    return result 