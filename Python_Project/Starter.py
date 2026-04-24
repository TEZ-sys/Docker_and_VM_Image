import os
import json
import logging
import argparse
import requests
from urllib.parse import urlparse
from JsonParser import APIClient
from GithubTrigger import GitHubClient

logger = logging.getLogger(__name__)

def loadEnvVars():
    env_path = "./.env"
    if not os.path.exists(env_path):
        logger.warning(f"File {env_path} not found. Checking system env...")
        return
    
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value.strip('"').strip("'")
    logger.info("Environment variables loaded from .env")

def validate_input_params(url: str):
    """Checks only if the URL string is valid."""
    result = urlparse(url)
    if not all([result.scheme, result.netloc]):
        raise ValueError(f"Invalid URL format: {url}")

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DevOps Automation Script - API Interaction")
    parser.add_argument("--fetch", action="store_true", help="Fetch all data")
    parser.add_argument("--list", action="store_true", help="List content in a human-readable format")
    parser.add_argument("--search-item-id", type=int, help="Search for a specific resource ID")
    parser.add_argument("--search-user-id", type=int, help="Search for a specific user ID")
    parser.add_argument("--trigger-pipeline", action="store_true", help="Trigger GitHub Actions workflow")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution")
    return parser

def run(args: argparse.Namespace):
    logger.info("Starting script execution...")
    loadEnvVars()
    url = os.getenv("URL")
    
    if not url:
        logger.error("URL missing from .env")
        return

    try:
        validate_input_params(url)
    except ValueError as e:
        logger.error(e)
        return

    client = APIClient(base_url=url, dry_run=args.dry_run)

    # STEP 3: Execute Logic
    if args.fetch:
        client.fetchPage()

    elif args.search_item_id:
        if args.search_item_id < 1:
            logger.error("ID must be positive.")
            return
        client.searchByID(args.search_item_id)

    elif args.search_user_id:
        if args.search_user_id < 1:
            logger.error("User ID must be positive.")
            return
        client.searchByUserID(args.search_user_id)

    elif args.list:
        client.listContent()
        
    elif args.trigger_pipeline:
        gh = GitHubClient(dry_run=args.dry_run)
        gh.trigger_workflow()
    else:
        logger.warning("No action specified. Use --help.")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    parser = get_parser()
    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    main()
