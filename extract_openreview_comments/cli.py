"""Command-line interface for OpenReview Comment Extractor."""

import sys
from pathlib import Path

import click

from .client import OpenReviewClient
from .formatter import MarkdownFormatter


@click.command()
@click.argument("forum_id")
@click.option(
    "--username",
    "-u",
    help="OpenReview username (optional for public content)",
    default=None,
)
@click.option(
    "--password",
    "-p",
    help="OpenReview password (optional for public content)",
    default=None,
)
@click.option(
    "--output",
    "-o",
    help="Output file path (default: comments.md)",
    default="comments.md",
    type=click.Path(),
)
@click.option(
    "--separate-files",
    "-s",
    is_flag=True,
    help="Save each comment to a separate file",
)
@click.option(
    "--output-dir",
    "-d",
    help="Output directory for separate files (default: comments/)",
    default="comments",
    type=click.Path(),
)
@click.option(
    "--baseurl",
    help="OpenReview API base URL (default: https://api2.openreview.net)",
    default="https://api2.openreview.net",
)
def main(
    forum_id: str,
    username: str | None,
    password: str | None,
    output: str,
    separate_files: bool,
    output_dir: str,
    baseurl: str,
):
    """Extract comments from an OpenReview forum.

    FORUM_ID: The OpenReview forum ID to extract comments from.

    Examples:

    \b
    # Extract all comments to a single file
    extract-openreview-comments <forum_id>

    \b
    # Extract with authentication
    extract-openreview-comments <forum_id> -u username -p password

    \b
    # Save each comment to a separate file
    extract-openreview-comments <forum_id> --separate-files

    \b
    # Specify output file
    extract-openreview-comments <forum_id> -o my_comments.md
    """
    try:
        click.echo(f"Fetching comments from forum: {forum_id}")

        # Initialize client
        client = OpenReviewClient(username=username, password=password, baseurl=baseurl)

        # Fetch notes
        click.echo("Retrieving notes...")
        notes = client.get_forum_notes(forum_id)

        if not notes:
            click.echo("No comments found in this forum.", err=True)
            sys.exit(1)

        click.echo(f"Found {len(notes)} notes")

        # Get submission title
        submission_title = client.get_submission_title(forum_id)

        if separate_files:
            # Save each comment to a separate file
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            click.echo(f"Saving comments to directory: {output_path}")

            # Filter out main submission and get only comments
            comments = [
                note for note in notes if hasattr(note, "replyto") and note.replyto
            ]

            if not comments:
                click.echo("No comments found (only main submission).", err=True)
                sys.exit(1)

            for i, note in enumerate(comments, 1):
                markdown, suggested_filename = MarkdownFormatter.format_note_to_file(
                    note, ""
                )
                file_path = output_path / f"comment_{i:03d}_{suggested_filename}"

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(markdown)

                click.echo(f"  Saved: {file_path}")

            click.echo(f"\nSuccessfully saved {len(comments)} comments!")

        else:
            # Save all comments to a single file
            click.echo("Formatting comments as Markdown...")
            markdown_content = MarkdownFormatter.format_all_notes(
                notes, submission_title
            )

            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            click.echo(f"\nSuccessfully saved comments to: {output_path}")

    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
