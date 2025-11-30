"""Markdown formatting for OpenReview comments."""

import html
from datetime import datetime
from typing import Any

from openreview.api import Note


class MarkdownFormatter:
    """Format OpenReview notes as Markdown."""

    @staticmethod
    def _get_attr(note: Note | dict[str, Any], attr: str, default: Any = None) -> Any:
        """Get attribute from Note object or dict."""
        if isinstance(note, dict):
            return note.get(attr, default)
        return getattr(note, attr, default)

    @staticmethod
    def format_note(
        note: Note | dict[str, Any], include_replies: bool = True, level: int = 0
    ) -> str:
        """Format a single note as Markdown.

        Args:
            note: The note to format (can be Note object or dict from API)
            include_replies: Whether to include direct replies
            level: Indentation level for nested comments

        Returns:
            Markdown formatted string
        """
        indent = "  " * level
        markdown_lines = []

        # Header with author and date
        signatures_raw = MarkdownFormatter._get_attr(note, "signatures")
        signatures = ", ".join(signatures_raw) if signatures_raw else "Anonymous"
        cdate = MarkdownFormatter._get_attr(note, "cdate")
        date_str = (
            datetime.fromtimestamp(cdate / 1000).strftime("%Y-%m-%d %H:%M:%S")
            if cdate
            else "Unknown date"
        )

        markdown_lines.append(f"{indent}## Comment by {signatures}")
        markdown_lines.append(f"{indent}**Date:** {date_str}")
        markdown_lines.append("")

        # Extract and format content
        content = MarkdownFormatter._get_attr(note, "content")
        if content:
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
        details = MarkdownFormatter._get_attr(note, "details")
        if include_replies and details:
            replies = details.get("directReplies", [])
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
            String value or None (with HTML entities unescaped)
        """
        value = None
        if isinstance(field, dict):
            value = field.get("value")
        elif isinstance(field, str):
            value = field
        elif isinstance(field, (int, float)):
            value = str(field)

        # Unescape HTML entities (e.g., &#39; -> ', &quot; -> ")
        if value and isinstance(value, str):
            value = html.unescape(value)

        return value

    @staticmethod
    def _build_children_map(notes: list[Note]) -> dict[str, list[Note]]:
        """Build a map of parent_id -> list of child notes.

        Args:
            notes: List of all notes from the forum

        Returns:
            Dict mapping note_id to list of direct reply notes (sorted by date)
        """
        children_map: dict[str, list[Note]] = {}

        for note in notes:
            replyto = getattr(note, "replyto", None)
            if replyto:
                if replyto not in children_map:
                    children_map[replyto] = []
                children_map[replyto].append(note)

        # Sort children by creation date
        for parent_id in children_map:
            children_map[parent_id].sort(key=lambda n: n.cdate if n.cdate else 0)

        return children_map

    @staticmethod
    def _format_note_recursive(
        note: Note | dict[str, Any],
        children_map: dict[str, list[Note]],
        level: int = 0,
    ) -> str:
        """Format a note and recursively format all replies.

        Args:
            note: The note to format
            children_map: Map of note_id -> list of child notes
            level: Indentation level for nested comments

        Returns:
            Markdown formatted string
        """
        indent = "  " * level
        markdown_lines = []

        # Header with author and date
        signatures_raw = MarkdownFormatter._get_attr(note, "signatures")
        signatures = ", ".join(signatures_raw) if signatures_raw else "Anonymous"
        cdate = MarkdownFormatter._get_attr(note, "cdate")
        date_str = (
            datetime.fromtimestamp(cdate / 1000).strftime("%Y-%m-%d %H:%M:%S")
            if cdate
            else "Unknown date"
        )

        markdown_lines.append(f"{indent}## Comment by {signatures}")
        markdown_lines.append(f"{indent}**Date:** {date_str}")
        markdown_lines.append("")

        # Extract and format content
        content = MarkdownFormatter._get_attr(note, "content")
        if content:
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

        # Get replies from children_map (built from replyto field, not API directReplies)
        note_id = MarkdownFormatter._get_attr(note, "id")
        replies = children_map.get(note_id, []) if note_id else []

        if replies:
            markdown_lines.append(f"{indent}### Replies:")
            markdown_lines.append("")
            for reply in replies:
                reply_md = MarkdownFormatter._format_note_recursive(
                    reply, children_map, level=level + 1
                )
                markdown_lines.append(reply_md)

        markdown_lines.append(f"{indent}---")
        markdown_lines.append("")

        return "\n".join(markdown_lines)

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

        # Build children map from replyto fields (captures ALL replies at all levels)
        children_map = MarkdownFormatter._build_children_map(sorted_notes)

        # Separate main submission from comments
        main_submission = None

        for note in sorted_notes:
            # The main submission typically doesn't have a replyto field
            if not hasattr(note, "replyto") or not note.replyto:
                main_submission = note
                break

        # Format main submission if present
        if main_submission:
            markdown_lines.append("# Main Submission")
            markdown_lines.append("")
            markdown_lines.append(
                MarkdownFormatter.format_note(main_submission, include_replies=False)
            )
            markdown_lines.append("")

        # Format comments - get top-level comments (direct replies to main submission)
        markdown_lines.append("# Comments and Reviews")
        markdown_lines.append("")

        top_level_comments: list[Note] = []
        if main_submission and main_submission.id:
            top_level_comments = children_map.get(main_submission.id, [])
        for note in top_level_comments:
            markdown_lines.append(
                MarkdownFormatter._format_note_recursive(note, children_map, level=0)
            )

        return "\n".join(markdown_lines)

    @staticmethod
    def format_note_to_file(
        note: Note | dict[str, Any], filename: str
    ) -> tuple[str, str]:
        """Format a single note as a standalone file.

        Args:
            note: The note to format (can be Note object or dict from API)
            filename: Suggested filename (will be sanitized)

        Returns:
            Tuple of (markdown content, sanitized filename)
        """
        # Create a title from the note
        signatures_raw = MarkdownFormatter._get_attr(note, "signatures")
        signatures = ", ".join(signatures_raw) if signatures_raw else "Anonymous"
        cdate = MarkdownFormatter._get_attr(note, "cdate")
        date_str = (
            datetime.fromtimestamp(cdate / 1000).strftime("%Y%m%d")
            if cdate
            else "unknown"
        )

        # Sanitize filename
        safe_filename = (
            f"{date_str}_{signatures.replace('/', '_').replace(' ', '_')}.md"
        )

        markdown = MarkdownFormatter.format_note(note, include_replies=True, level=0)

        return markdown, safe_filename
