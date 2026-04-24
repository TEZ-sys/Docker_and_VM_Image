Collecting workspace informationFiltering to most relevant information```markdown
# python-nebo

A small Python automation project for interacting with an API and optionally triggering a GitHub Actions workflow.

## Files

- [`Starter.py`](Starter.py) - main CLI entry point
- [`JsonParser.py`](JsonParser.py) - API client for fetching and filtering JSON data
- [`GithubTrigger.py`](GithubTrigger.py) - GitHub Actions workflow trigger client
- [`requirements.txt`](requirements.txt) - project dependencies

## Prerequisites

- Python 3.12+ (the repository includes a virtual environment at `nebo_venv/`)
- `requests` library

## Setup

1. Create and activate a virtual environment, or use the included `nebo_venv`
2. Install dependencies:

```sh
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
URL=https://jsonplaceholder.typicode.com/posts
GITHUB_TOKEN=your_token_here
GITHUB_REPO=owner/repo
GITHUB_WORKFLOW=workflow_file_name.yml
GITHUB_REF=main
```

`URL` is required for API requests.

## Usage

Run the script with one of the supported flags:

```sh
python Starter.py --help
```

Examples:

- Fetch all data and save to `output.json`:
  ```sh
  python Starter.py --fetch
  ```

- List API response content:
  ```sh
  python Starter.py --list
  ```

- Search by resource ID:
  ```sh
  python Starter.py --search-item-id 5
  ```

- Search by user ID:
  ```sh
  python Starter.py --search-user-id 2
  ```

- Trigger a GitHub Actions workflow:
  ```sh
  python Starter.py --trigger-pipeline
  ```

- Dry run mode:
  ```sh
  python Starter.py --fetch --dry-run
  ```

## Notes

- [`Starter.py`](Starter.py) loads environment variables from `.env` if present, then validates `URL`.
- [`JsonParser.py`](JsonParser.py) includes retry handling for HTTP GET requests.
- [`GithubTrigger.py`](GithubTrigger.py) triggers a GitHub workflow dispatch using the GitHub API and retries up to 3 times.
```