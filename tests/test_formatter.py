"""Tests for the markdown formatter."""

from unittest.mock import Mock

from extract_openreview_comments.formatter import MarkdownFormatter


def create_mock_note(
    note_id: str = "test_id",
    signatures: list[str] | None = None,
    cdate: int = 1609459200000,  # 2021-01-01
    content: dict | None = None,
    replyto: str | None = None,
):
    """Create a mock Note object for testing."""
    note = Mock()
    note.id = note_id
    note.signatures = signatures or ["Test Author"]
    note.cdate = cdate
    note.content = content or {}
    note.replyto = replyto
    note.details = {}
    return note


class TestMarkdownFormatter:
    """Tests for MarkdownFormatter class."""

    def test_extract_value_dict(self):
        """Test extracting value from dict format."""
        field = {"value": "Test content"}
        result = MarkdownFormatter._extract_value(field)
        assert result == "Test content"

    def test_extract_value_string(self):
        """Test extracting value from string format."""
        field = "Test content"
        result = MarkdownFormatter._extract_value(field)
        assert result == "Test content"

    def test_extract_value_number(self):
        """Test extracting value from number format."""
        field = 42
        result = MarkdownFormatter._extract_value(field)
        assert result == "42"

    def test_extract_value_none(self):
        """Test extracting value from None."""
        result = MarkdownFormatter._extract_value(None)
        assert result is None

    def test_format_note_basic(self):
        """Test formatting a basic note."""
        note = create_mock_note(
            content={"comment": {"value": "This is a test comment"}}
        )

        result = MarkdownFormatter.format_note(note, include_replies=False)

        assert "## Comment by Test Author" in result
        assert "2021-01-01" in result
        assert "This is a test comment" in result

    def test_format_note_with_rating(self):
        """Test formatting a note with rating."""
        note = create_mock_note(
            content={
                "review": {"value": "Good paper"},
                "rating": {"value": "8: Top 50% of accepted papers"},
                "confidence": {"value": "4: High"},
            }
        )

        result = MarkdownFormatter.format_note(note, include_replies=False)

        assert "Good paper" in result
        assert "Rating:** 8: Top 50% of accepted papers" in result
        assert "Confidence:** 4: High" in result

    def test_format_note_with_replies(self):
        """Test formatting a note with replies."""
        reply = create_mock_note(
            note_id="reply_1",
            signatures=["Author Reply"],
            content={"comment": {"value": "Thank you for the review"}},
        )

        parent_note = create_mock_note(content={"review": {"value": "Good paper"}})
        parent_note.details = {"directReplies": [reply]}

        result = MarkdownFormatter.format_note(parent_note, include_replies=True)

        assert "Good paper" in result
        assert "Replies:" in result
        assert "Author Reply" in result
        assert "Thank you for the review" in result

    def test_format_all_notes_empty(self):
        """Test formatting empty list of notes."""
        result = MarkdownFormatter.format_all_notes([])

        assert "OpenReview Comments" in result
        assert "Total Comments:** 0" in result

    def test_format_all_notes_with_submission(self):
        """Test formatting notes with main submission."""
        submission = create_mock_note(
            note_id="submission_1",
            content={
                "title": {"value": "Test Paper"},
                "abstract": {"value": "This is a test abstract"},
            },
            replyto=None,
        )

        comment = create_mock_note(
            note_id="comment_1",
            content={"comment": {"value": "Great work!"}},
            replyto="submission_1",
        )

        result = MarkdownFormatter.format_all_notes(
            [submission, comment], submission_title="Test Paper"
        )

        assert "Test Paper" in result
        assert "Main Submission" in result
        assert "Comments and Reviews" in result
        assert "Great work!" in result

    def test_format_note_to_file(self):
        """Test formatting a note for file output."""
        note = create_mock_note(
            signatures=["Reviewer ABC"],
            cdate=1609459200000,
            content={"comment": {"value": "Test comment"}},
        )

        markdown, filename = MarkdownFormatter.format_note_to_file(note, "")

        assert "Test comment" in markdown
        assert "20210101" in filename
        assert "Reviewer_ABC" in filename  # Spaces are replaced with underscores
        assert filename.endswith(".md")

    def test_format_note_multiple_signatures(self):
        """Test formatting a note with multiple signatures."""
        note = create_mock_note(
            signatures=["Author1", "Author2", "Author3"],
            content={"comment": {"value": "Joint response"}},
        )

        result = MarkdownFormatter.format_note(note, include_replies=False)

        assert "Author1, Author2, Author3" in result
        assert "Joint response" in result

    def test_extract_value_html_entities(self):
        """Test that HTML entities are unescaped."""
        # Test with common HTML entities
        assert MarkdownFormatter._extract_value("It&#39;s working") == "It's working"
        assert (
            MarkdownFormatter._extract_value("Say &quot;hello&quot;") == 'Say "hello"'
        )
        assert (
            MarkdownFormatter._extract_value("Less &lt; more &gt;") == "Less < more >"
        )
        assert MarkdownFormatter._extract_value("A &amp; B") == "A & B"

        # Test with dict format
        assert (
            MarkdownFormatter._extract_value({"value": "It&#39;s working"})
            == "It's working"
        )

    def test_format_note_with_html_entities(self):
        """Test formatting a note with HTML entities in content."""
        note = create_mock_note(
            content={
                "comment": {
                    "value": "The model&#39;s performance is &quot;excellent&quot; &amp; promising."
                }
            }
        )

        result = MarkdownFormatter.format_note(note, include_replies=False)

        # Check that HTML entities are unescaped in output
        assert "model's performance" in result
        assert '"excellent"' in result
        assert "& promising" in result
        # Make sure raw entities are not in output
        assert "&#39;" not in result
        assert "&quot;" not in result
        assert "&amp;" not in result
