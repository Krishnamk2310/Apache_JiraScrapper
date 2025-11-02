import os
import json
from typing import Dict, Any

# Base URLs for JIRA APIs
JIRA_BASE = "https://issues.apache.org/jira"
SEARCH_API = f"{JIRA_BASE}/rest/api/2/search"
ISSUE_API = f"{JIRA_BASE}/rest/api/2/issue/{{issue_key}}"
COMMENTS_API = f"{JIRA_BASE}/rest/api/2/issue/{{issue_key}}/comment"

# Scraper setup
PAGE_SIZE = 100  # Number of issues to fetch per page
DEFAULT_PROJECTS = ["TIKA", "ZOOKEEPER", "OPENNLP"]

# Output folders and files
OUTDIR = "data"
RAW_DIR = os.path.join(OUTDIR, "raw")
STATE_FILE = os.path.join(OUTDIR, "state.json")
TRAIN_FILE = os.path.join(OUTDIR, "train.jsonl")

def ensure_dir(path: str):
    # Make sure the directory exists before saving files
    os.makedirs(path, exist_ok=True)

def save_state(state: Dict[str, Any]):
    # Save scraper progress so it can resume later if stopped
    ensure_dir(os.path.dirname(STATE_FILE))
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

def load_state() -> Dict[str, Any]:
    # Load previously saved scraper progress (if available)
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding='utf-8') as f:
            return json.load(f)
    return {}