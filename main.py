import argparse
import json
import os
from typing import List

from jira_scraper import ApacheJiraFetcher
from text_utils import transform_issue
from config import (
    DEFAULT_PROJECTS, RAW_DIR, TRAIN_FILE,
    ensure_dir, save_state, load_state
)

def scrape_projects(projects: List[str], transform_only: bool = False):
    # Load previous scraping state to avoid duplicate work
    state = load_state()
    processed_issues = set(state.get('processed_issues', []))

    # Step 1: Scrape data (if not in transform-only mode)
    if not transform_only:
        jira = ApacheJiraFetcher()
        for project in projects:
            print(f"Fetching issues from project: {project}")
            project_dir = os.path.join(RAW_DIR, project)
            ensure_dir(project_dir)

            # Go through each issue in the project
            for issue in jira.process_project(project):
                issue_key = issue['key']
                if issue_key in processed_issues:
                    continue  # Skip already scraped issues

                # Save the raw issue data for future use
                issue_file = os.path.join(project_dir, f"{issue_key}.json")
                with open(issue_file, 'w', encoding='utf-8') as f:
                    json.dump(issue, f, indent=2)

                # Keep track of what’s already processed
                processed_issues.add(issue_key)
                save_state({'processed_issues': list(processed_issues)})

    # Step 2: Transform all raw issue data into a structured JSONL file
    ensure_dir(os.path.dirname(TRAIN_FILE))
    with open(TRAIN_FILE, 'w', encoding='utf-8') as out:
        for project in projects:
            project_dir = os.path.join(RAW_DIR, project)
            if not os.path.exists(project_dir):
                continue

            for filename in os.listdir(project_dir):
                if not filename.endswith('.json'):
                    continue

                # Read and transform issue into model-ready format
                with open(os.path.join(project_dir, filename), encoding='utf-8') as f:
                    issue = json.load(f)
                    transformed = transform_issue(issue)
                    out.write(json.dumps(transformed) + '\n')

def main():
    parser = argparse.ArgumentParser(description='Apache JIRA Data Scraper and Transformer')
    parser.add_argument(
        '--projects', nargs='+', default=DEFAULT_PROJECTS,
        help='List of Apache JIRA project keys to fetch (default: common open-source ones)'
    )
    parser.add_argument(
        '--transform-only', action='store_true',
        help='Skip data fetching and only transform already downloaded data'
    )
    args = parser.parse_args()

    scrape_projects(args.projects, args.transform_only)

if __name__ == '__main__':
    main()
