# Apache JIRA Scraper - Handles API requests and issue data fetching

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
from config import JIRA_BASE, SEARCH_API, ISSUE_API, COMMENTS_API, PAGE_SIZE

class ApacheJiraFetcher:
    def __init__(self):
        self.session = self._create_session()

    def _create_session(self):
        # Create a session with retry logic for better reliability
        session = requests.Session()
        retry_policy = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_policy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def fetch_issues(self, project: str, start_at: int = 0):
        # Fetch issues from a given project (supports pagination)
        jql = f'project = {project} ORDER BY key ASC'
        params = {
            'jql': jql,
            'maxResults': PAGE_SIZE,
            'startAt': start_at,
            'fields': 'summary,description,created,status,comment'
        }
        response = self.session.get(SEARCH_API, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_issue_details(self, issue_key: str):
        # Get detailed information about a specific issue
        url = ISSUE_API.format(issue_key=issue_key)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_comments(self, issue_key: str):
        # Retrieve comments for a particular issue
        url = COMMENTS_API.format(issue_key=issue_key)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def process_project(self, project: str):
        # Iterate through all issues in a project using pagination
        start_at = 0
        total = None

        while total is None or start_at < total:
            data = self.fetch_issues(project, start_at)
            total = data['total']
            yield from data['issues']  # Yield issues one by one
            start_at += len(data['issues'])
            time.sleep(1)  # Prevent hitting API rate limits
