"""Tests for the CLI password prompt behavior."""

from unittest.mock import Mock, patch

from click.testing import CliRunner

from extract_openreview_comments.cli import main


class TestCliPasswordPrompt:
    """Tests for interactive password prompting."""

    @patch("extract_openreview_comments.cli.OpenReviewClient")
    def test_username_without_password_prompts(self, mock_client_class):
        """Test that providing username without password prompts for it."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.get_forum_notes.return_value = [Mock()]
        mock_client.get_submission_title.return_value = "Test Title"

        runner = CliRunner()
        result = runner.invoke(
            main,
            ["test_forum", "-u", "myuser"],
            input="secret_password\n",
        )

        assert result.exit_code == 0
        mock_client_class.assert_called_once_with(
            username="myuser", password="secret_password", baseurl="https://api2.openreview.net"
        )

    @patch("extract_openreview_comments.cli.OpenReviewClient")
    def test_username_with_password_does_not_prompt(self, mock_client_class):
        """Test that providing both username and password skips the prompt."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.get_forum_notes.return_value = [Mock()]
        mock_client.get_submission_title.return_value = "Test Title"

        runner = CliRunner()
        result = runner.invoke(
            main,
            ["test_forum", "-u", "myuser", "-p", "mypass"],
        )

        assert result.exit_code == 0
        mock_client_class.assert_called_once_with(
            username="myuser", password="mypass", baseurl="https://api2.openreview.net"
        )

    @patch("extract_openreview_comments.cli.OpenReviewClient")
    def test_no_username_no_password_does_not_prompt(self, mock_client_class):
        """Test that omitting both username and password skips the prompt."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.get_forum_notes.return_value = [Mock()]
        mock_client.get_submission_title.return_value = "Test Title"

        runner = CliRunner()
        result = runner.invoke(main, ["test_forum"])

        assert result.exit_code == 0
        mock_client_class.assert_called_once_with(
            username=None, password=None, baseurl="https://api2.openreview.net"
        )
