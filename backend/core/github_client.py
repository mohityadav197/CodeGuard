"""Thin wrapper around the GitHub REST API endpoints CodeGuard needs:
fetching a PR's changed files (with unified diff patches) and posting a
single review with inline comments back onto the PR.
"""

from __future__ import annotations

import requests

API_BASE = "https://api.github.com"


class GitHubClient:
    def __init__(self, token: str):
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )

    def get_pr_files(self, owner: str, repo: str, pr_number: int) -> list[dict]:
        """Return the list of changed files for a PR, each with a `patch` field
        (unified diff), paginating through all results."""
        files: list[dict] = []
        url = f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        params = {"per_page": 100}
        while url:
            resp = self._session.get(url, params=params)
            resp.raise_for_status()
            files.extend(resp.json())
            url = resp.links.get("next", {}).get("url")
            params = None  # subsequent `next` urls already carry query params
        return files

    def post_review(
        self,
        owner: str,
        repo: str,
        pr_number: int,
        summary: str,
        comments: list[dict],
    ) -> dict:
        """Post one PR review with a summary body and inline comments.

        `comments` entries must be `{"path": ..., "line": ..., "body": ...}`.
        """
        url = f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        payload = {"body": summary, "event": "COMMENT", "comments": comments}
        resp = self._session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()
