"""Tests for the OpenReview client."""

from unittest.mock import Mock, patch

import pytest

from extract_openreview_comments.client import OpenReviewClient


class TestOpenReviewClient:
    """Tests for OpenReviewClient class."""

    @patch("extract_openreview_comments.client.openreview.api.OpenReviewClient")
    def test_init_with_credentials(self, mock_openreview):
        """Test initializing client with credentials."""
        OpenReviewClient(username="test_user", password="test_pass")

        mock_openreview.assert_called_once_with(
            baseurl="https://api2.openreview.net",
            username="test_user",
            password="test_pass",
        )

    @patch("extract_openreview_comments.client.openreview.api.OpenReviewClient")
    def test_init_without_credentials(self, mock_openreview):
        """Test initializing client without credentials."""
        OpenReviewClient()

        mock_openreview.assert_called_once_with(
            baseurl="https://api2.openreview.net", username=None, password=None
        )

    @patch("extract_openreview_comments.client.openreview.api.OpenReviewClient")
    def test_init_custom_baseurl(self, mock_openreview):
        """Test initializing client with custom base URL."""
        OpenReviewClient(baseurl="https://custom.openreview.net")

        mock_openreview.assert_called_once_with(
            baseurl="https://custom.openreview.net", username=None, password=None
        )

    @patch("extract_openreview_comments.client.openreview.api.OpenReviewClient")
    def test_get_forum_notes_success(self, mock_openreview_class):
        """Test successfully fetching forum notes."""
        # Setup mocks
        mock_client = Mock()
        mock_openreview_class.return_value = mock_client

        mock_note = Mock()
        mock_note.id = "test_forum_id"
        mock_client.get_note.return_value = mock_note

        mock_notes = [Mock(), Mock(), Mock()]
        mock_client.get_all_notes.return_value = mock_notes

        # Test
        client = OpenReviewClient()
        result = client.get_forum_notes("test_forum_id")

        # Assertions
        mock_client.get_note.assert_called_once_with("test_forum_id")
        mock_client.get_all_notes.assert_called_once_with(
            forum="test_forum_id", details="directReplies"
        )
        assert result == mock_notes

    @patch("extract_openreview_comments.client.openreview.api.OpenReviewClient")
    def test_get_forum_notes_invalid_forum(self, mock_openreview_class):
        """Test fetching notes from invalid forum."""
        # Setup mocks
        mock_client = Mock()
        mock_openreview_class.return_value = mock_client
        mock_client.get_note.side_effect = Exception("Forum not found")

        # Test
        client = OpenReviewClient()

        with pytest.raises(ValueError, match="Could not fetch forum"):
            client.get_forum_notes("invalid_forum_id")

    @patch("extract_openreview_comments.client.openreview.api.OpenReviewClient")
    def test_get_submission_title_success(self, mock_openreview_class):
        """Test successfully getting submission title."""
        # Setup mocks
        mock_client = Mock()
        mock_openreview_class.return_value = mock_client

        mock_note = Mock()
        mock_note.content = {"title": {"value": "Test Paper Title"}}
        mock_client.get_note.return_value = mock_note

        # Test
        client = OpenReviewClient()
        result = client.get_submission_title("test_forum_id")

        # Assertions
        assert result == "Test Paper Title"

    @patch("extract_openreview_comments.client.openreview.api.OpenReviewClient")
    def test_get_submission_title_missing_title(self, mock_openreview_class):
        """Test getting submission title when title is missing."""
        # Setup mocks
        mock_client = Mock()
        mock_openreview_class.return_value = mock_client

        mock_note = Mock()
        mock_note.content = {}
        mock_client.get_note.return_value = mock_note

        # Test
        client = OpenReviewClient()
        result = client.get_submission_title("test_forum_id")

        # Assertions
        assert result == "Unknown Title"

    @patch("extract_openreview_comments.client.openreview.api.OpenReviewClient")
    def test_get_submission_title_error(self, mock_openreview_class):
        """Test getting submission title when API call fails."""
        # Setup mocks
        mock_client = Mock()
        mock_openreview_class.return_value = mock_client
        mock_client.get_note.side_effect = Exception("API Error")

        # Test
        client = OpenReviewClient()
        result = client.get_submission_title("test_forum_id")

        # Assertions
        assert result == "Forum test_forum_id"
