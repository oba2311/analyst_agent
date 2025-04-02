"""
Tests for the formatting utilities.
"""

import unittest
from src.utils.formatting import format_cli_response, format_table, highlight_text


class TestFormatting(unittest.TestCase):
    """Tests for the formatting utilities."""

    def test_format_cli_response(self):
        """Test the CLI response formatting."""
        # Test numbered list formatting
        numbered_list = "1. First item2. Second item3. Third item"
        expected = "1. First item\n\n2. Second item\n\n3. Third item"
        self.assertEqual(format_cli_response(numbered_list), expected)

        # Test header formatting
        headers = "# Header\nSome text\n## Subheader\nMore text"
        expected = "# Header\n\nSome text\n## Subheader\n\nMore text"
        self.assertEqual(format_cli_response(headers), expected)

        # Test bullet points
        bullets = "* First point* Second point* Third point"
        expected = "* First point\n* Second point\n* Third point"
        self.assertEqual(format_cli_response(bullets), expected)

    def test_format_table(self):
        """Test the table formatting."""
        headers = ["Name", "Value", "Description"]
        rows = [
            ["Item 1", "10", "First item"],
            ["Item 2", "20", "Second item"],
            ["Item 3", "30", "Third item with long description"]
        ]

        # Generate table
        table = format_table(headers, rows)

        # Check if table contains all headers and row data
        for header in headers:
            self.assertIn(header, table)

        for row in rows:
            for cell in row:
                self.assertIn(cell, table)

        # Check for empty data handling
        empty_table = format_table(headers, [])
        self.assertEqual(empty_table, "No data available.")

        # Test with title
        titled_table = format_table(headers, rows, title="Test Table")
        self.assertIn("Test Table", titled_table)

    def test_highlight_text(self):
        """Test the text highlighting."""
        test_text = "This is a test string with some important terms to highlight."
        highlights = ["test", "important", "highlight"]

        # Generate highlighted text
        highlighted = highlight_text(test_text, highlights)

        # The result should be longer due to ANSI codes
        self.assertGreater(len(highlighted), len(test_text))

        # Test with empty highlights
        no_highlights = highlight_text(test_text, [])
        self.assertEqual(no_highlights, test_text)

        # Test case insensitivity
        case_text = "Test TEST test"
        case_highlighted = highlight_text(case_text, ["test"])
        # All three instances should be highlighted (3 occurrences of "test" in different cases)
        # Each highlight adds 2 ANSI sequences
        expected_extra_chars = 3 * (len("\033[1;33m") + len("\033[0m"))
        self.assertEqual(len(case_highlighted), len(case_text) + expected_extra_chars)


if __name__ == "__main__":
    unittest.main() 