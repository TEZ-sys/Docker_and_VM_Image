import json
import logging
import requests
import os
import time

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str, dry_run: bool = False):
        self.base_url = base_url.rstrip('/')
        self.dry_run = dry_run
        self.timeout = 10

    def _execute_request(self, url: str, retries: int = 3):
        if self.dry_run:
            logger.info(f"[DRY-RUN] Request to: {url}")
            return None

        for attempt in range(1, retries + 1):
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.warning(f"Attempt {attempt}/{retries} failed: {e}")
                if attempt < retries:
                    time.sleep(2)

        logger.error(f"All {retries} attempts failed for {url}")
        return None

    def fetchPage(self, output_file: str = "output.json"):
        data = self._execute_request(self.base_url)
        if data and not self.dry_run:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logger.info(f"Saved to: {os.path.abspath(output_file)}")

    def listContent(self):
        data = self._execute_request(self.base_url)
        if data:
            print(json.dumps(data, indent=4))

    def searchByID(self, resource_id: int):
        url = f"{self.base_url}/{resource_id}"
        data = self._execute_request(url)
        if data:
            print(json.dumps(data, indent=4))

    def searchByUserID(self, user_id: int):
            url = f"{self.base_url}?userId={user_id}"
            
            data = self._execute_request(url)
            if data:
                if isinstance(data, list) and len(data) == 0:
                    logger.warning(f"No posts found for User ID {user_id}.")
                else:
                    logger.info(f"Successfully filtered posts for User ID {user_id}.")
                    print(json.dumps(data, indent=4))