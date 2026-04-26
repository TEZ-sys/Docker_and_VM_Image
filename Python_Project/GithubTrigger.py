import os
import logging
import requests
import time

logger = logging.getLogger(__name__)

class GitHubClient:
    def __init__(self, token: str, repo: str, workflow: str, branch: str = "main", dry_run: bool = False):
        self.token = token
        self.repo = repo
        self.workflow = workflow
        self.branch = branch
        self.dry_run = dry_run
        self.base_url = f"https://api.github.com/repos/{self.repo}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def _validate(self):
        missing = [k for k, v in {
            "GITHUB_TOKEN": self.token,
            "GITHUB_REPO": self.repo,
            "GITHUB_WORKFLOW": self.workflow
        }.items() if not v]
        if missing:
            logger.error(f"Missing env vars: {', '.join(missing)}")
            return False
        return True

    def trigger_workflow(self, inputs: dict = {}):
        if not self._validate():
            return

        url = f"{self.base_url}/actions/workflows/{self.workflow}/dispatches"
        payload = {"ref": self.branch, "inputs": inputs}

        if self.dry_run:
            logger.info(f"[DRY-RUN] POST {url} | payload: {payload}")
            return

        for attempt in range(1, 4):
            try:
                response = requests.post(url, headers=self.headers, json=payload, timeout=10)
                response.raise_for_status()
                logger.info(f"Workflow '{self.workflow}' triggered on '{self.branch}'")
                return
            except Exception as e:
                logger.warning(f"Attempt {attempt}/3 failed: {e}")
                if attempt < 3:
                    time.sleep(2)

        logger.error("Failed to trigger workflow after 3 attempts.")
