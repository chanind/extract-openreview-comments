"""OpenReview API client for fetching forum comments."""

import openreview
from openreview.api import Note


class OpenReviewClient:
    """Client for interacting with the OpenReview API."""

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        baseurl: str = "https://api2.openreview.net",
    ):
        """Initialize the OpenReview client.

        Args:
            username: OpenReview username (optional for public content)
            password: OpenReview password (optional for public content)
            baseurl: Base URL for the OpenReview API (default: API v2)
        """
        self.client = openreview.api.OpenReviewClient(  # type: ignore
            baseurl=baseurl, username=username, password=password
        )

    def get_forum_notes(self, forum_id: str) -> list[Note]:
        """Fetch all notes (comments) for a given forum.

        Args:
            forum_id: The forum ID to fetch comments from

        Returns:
            List of Note objects from the forum

        Raises:
            openreview.OpenReviewException: If the forum cannot be accessed
        """
        # Get the main submission note
        try:
            self.client.get_note(forum_id)
        except Exception as e:
            raise ValueError(f"Could not fetch forum {forum_id}: {e}") from e

        # Get all notes in the forum (including the main note and all comments)
        all_notes = self.client.get_all_notes(forum=forum_id, details="directReplies")

        return all_notes

    def get_submission_title(self, forum_id: str) -> str:
        """Get the title of the submission.

        Args:
            forum_id: The forum ID

        Returns:
            The submission title
        """
        try:
            main_note = self.client.get_note(forum_id)
            return main_note.content.get("title", {}).get("value", "Unknown Title")
        except Exception:
            return f"Forum {forum_id}"
