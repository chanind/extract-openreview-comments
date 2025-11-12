# Extract OpenReview Comments

[![PyPI version](https://badge.fury.io/py/extract-openreview-comments.svg)](https://badge.fury.io/py/extract-openreview-comments)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python command-line tool to extract OpenReview comments for a paper into markdown format for easy copy/pasting when writing rebuttals.

## Features

- 📥 Extract all comments and reviews from any OpenReview forum
- 📝 Format comments as clean, readable Markdown
- 🔐 Support for both public and private content (with authentication)
- 📁 Save to a single file or split into separate files per comment
- 🔄 Preserves reply threads and nested discussions
- ⚡ Fast and easy to use

## Installation

### From PyPI (recommended)

```bash
pip install extract-openreview-comments
```

### From Source

```bash
git clone https://github.com/chanind/extract-openreview-comments.git
cd extract-openreview-comments
pip install -e .
```

### For Development

```bash
git clone https://github.com/chanind/extract-openreview-comments.git
cd extract-openreview-comments
pip install -e ".[dev]"
```

Or with [uv](https://github.com/astral-sh/uv) (faster):

```bash
uv sync
```

## Usage

### Basic Usage

Extract comments from a public OpenReview forum:

```bash
extract-openreview-comments <forum_id>
```

This will save all comments to `comments.md` in the current directory.

### With Authentication

For private content or to access additional information:

```bash
extract-openreview-comments <forum_id> -u your_email@example.com -p your_password
```

### Save to Custom File

```bash
extract-openreview-comments <forum_id> -o my_reviews.md
```

### Split into Separate Files

Save each comment to a separate file in a directory:

```bash
extract-openreview-comments <forum_id> --separate-files -d output_directory/
```

### Finding the Forum ID

The forum ID is the unique identifier for a paper on OpenReview. You can find it in the URL:

```
https://openreview.net/forum?id=FORUM_ID_HERE
```

For example, in `https://openreview.net/forum?id=rJXMpikCZ`, the forum ID is `rJXMpikCZ`.

## Command-Line Options

```
Usage: extract-openreview-comments [OPTIONS] FORUM_ID

Options:
  -u, --username TEXT    OpenReview username (optional for public content)
  -p, --password TEXT    OpenReview password (optional for public content)
  -o, --output PATH      Output file path (default: comments.md)
  -s, --separate-files   Save each comment to a separate file
  -d, --output-dir PATH  Output directory for separate files (default: comments/)
  --baseurl TEXT         OpenReview API base URL (default: https://api2.openreview.net)
  --help                 Show this message and exit.
```

## Output Format

The tool generates well-formatted Markdown with:

- Comment metadata (author, date)
- Review content (summary, strengths, weaknesses, questions)
- Ratings and confidence scores
- Nested reply threads
- Clear section separators

Example output:

```markdown
# Paper Title

**Total Comments:** 5

---

## Comment by Reviewer_ABC
**Date:** 2024-01-15 10:30:00

**Review:**

This paper presents an interesting approach to...

**Rating:** 8: Top 50% of accepted papers

**Confidence:** 4: High

### Replies:

## Comment by Authors
**Date:** 2024-01-20 14:00:00

**Response:**

We thank the reviewer for their feedback...

---
```

## Development

### Running Tests

```bash
uv run pytest
```

### Linting and Formatting

```bash
uv run ruff check .
uv run ruff format .
```

### Type Checking

```bash
uv run pyright
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using the [OpenReview Python API](https://github.com/openreview/openreview-py)
- CLI powered by [Click](https://click.palletsprojects.com/)

## Links

- [GitHub Repository](https://github.com/chanind/extract-openreview-comments)
- [Issue Tracker](https://github.com/chanind/extract-openreview-comments/issues)
- [PyPI Package](https://pypi.org/project/extract-openreview-comments/)
