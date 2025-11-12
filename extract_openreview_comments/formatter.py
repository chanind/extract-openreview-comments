"""Markdown formatting for OpenReview comments."""

from datetime import datetime
from typing import Any

from openreview.api import Note


class MarkdownFormatter:
    """Format OpenReview notes as Markdown."""

    @staticmethod
    def format_note(note: Note, include_replies: bool = True, level: int = 0) -> str:
        """Format a single note as Markdown.

        Args:
            note: The note to format
            include_replies: Whether to include direct replies
            level: Indentation level for nested comments

        Returns:
            Markdown formatted string
        """
        indent = "  " * level
        markdown_lines = []

        # Header with author and date
        signatures = ", ".join(note.signatures) if note.signatures else "Anonymous"
        date_str = (
            datetime.fromtimestamp(note.cdate / 1000).strftime("%Y-%m-%d %H:%M:%S")
            if note.cdate
            else "Unknown date"
        )

        markdown_lines.append(f"{indent}## Comment by {signatures}")
        markdown_lines.append(f"{indent}**Date:** {date_str}")
        markdown_lines.append("")

        # Extract and format content
        if hasattr(note, "content") and note.content:
            content = note.content

            # Title (if present and not the main submission)
            if "title" in content and level > 0:
                title_value = MarkdownFormatter._extract_value(content["title"])
                if title_value:
                    markdown_lines.append(f"{indent}**Title:** {title_value}")
                    markdown_lines.append("")

            # Main content fields
            for field_name in ["comment", "review", "summary", "response"]:
                if field_name in content:
                    field_value = MarkdownFormatter._extract_value(content[field_name])
                    if field_value:
                        markdown_lines.append(f"{indent}**{field_name.title()}:**")
                        markdown_lines.append("")
                        # Indent content
                        for line in field_value.split("\n"):
                            markdown_lines.append(f"{indent}{line}")
                        markdown_lines.append("")

            # Other relevant fields
            for field_name in [
                "rating",
                "confidence",
                "strengths",
                "weaknesses",
                "questions",
            ]:
                if field_name in content:
                    field_value = MarkdownFormatter._extract_value(content[field_name])
                    if field_value:
                        markdown_lines.append(
                            f"{indent}**{field_name.replace('_', ' ').title()}:** {field_value}"
                        )
                        markdown_lines.append("")

        # Add replies if present
        if include_replies and hasattr(note, "details") and note.details:
            replies = note.details.get("directReplies", [])
            if replies:
                markdown_lines.append(f"{indent}### Replies:")
                markdown_lines.append("")
                for reply in replies:
                    reply_md = MarkdownFormatter.format_note(
                        reply, include_replies=True, level=level + 1
                    )
                    markdown_lines.append(reply_md)

        markdown_lines.append(f"{indent}---")
        markdown_lines.append("")

        return "\n".join(markdown_lines)

    @staticmethod
    def _extract_value(field: Any) -> str | None:
        """Extract the value from a field, handling different formats.

        Args:
            field: The field to extract value from

        Returns:
            String value or None
        """
        if isinstance(field, dict):
            return field.get("value")
        elif isinstance(field, str):
            return field
        elif isinstance(field, (int, float)):
            return str(field)
        return None

    @staticmethod
    def format_all_notes(
        notes: list[Note], submission_title: str = "OpenReview Comments"
    ) -> str:
        """Format all notes into a single Markdown document.

        Args:
            notes: List of notes to format
            submission_title: Title for the document

        Returns:
            Complete Markdown document
        """
        markdown_lines = [
            f"# {submission_title}",
            "",
            f"**Total Comments:** {len(notes)}",
            "",
            "---",
            "",
        ]

        # Sort notes by creation date
        sorted_notes = sorted(notes, key=lambda n: n.cdate if n.cdate else 0)

        # Separate main submission from comments
        main_submission = None
        comments = []

        for note in sorted_notes:
            # The main submission typically doesn't have a replyto field
            if not hasattr(note, "replyto") or not note.replyto:
                main_submission = note
            else:
                comments.append(note)

        # Format main submission if present
        if main_submission:
            markdown_lines.append("# Main Submission")
            markdown_lines.append("")
            markdown_lines.append(
                MarkdownFormatter.format_note(main_submission, include_replies=False)
            )
            markdown_lines.append("")

        # Format comments
        markdown_lines.append("# Comments and Reviews")
        markdown_lines.append("")

        for note in comments:
            # Only format top-level comments; replies are handled recursively
            if not hasattr(note, "replyto") or note.replyto == (
                main_submission.id if main_submission else None
            ):
                markdown_lines.append(
                    MarkdownFormatter.format_note(note, include_replies=True)
                )

        return "\n".join(markdown_lines)

    @staticmethod
    def format_note_to_file(note: Note, filename: str) -> tuple[str, str]:
        """Format a single note as a standalone file.

        Args:
            note: The note to format
            filename: Suggested filename (will be sanitized)

        Returns:
            Tuple of (markdown content, sanitized filename)
        """
        # Create a title from the note
        signatures = ", ".join(note.signatures) if note.signatures else "Anonymous"
        date_str = (
            datetime.fromtimestamp(note.cdate / 1000).strftime("%Y%m%d")
            if note.cdate
            else "unknown"
        )

        # Sanitize filename
        safe_filename = (
            f"{date_str}_{signatures.replace('/', '_').replace(' ', '_')}.md"
        )

        markdown = MarkdownFormatter.format_note(note, include_replies=True, level=0)

        return markdown, safe_filename
