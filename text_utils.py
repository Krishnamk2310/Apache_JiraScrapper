# Utility functions for cleaning and transforming Apache JIRA issue data

import re
from html import unescape
from typing import Dict, Any

def clean_text(text: str) -> str:
    # Cleans and normalizes text by removing unnecessary spaces and line breaks
    if not text:
        return ""
    text = " ".join(text.split())  # Collapse multiple spaces and newlines
    return text.strip()

def remove_html_tags(html_text: str) -> str:
    # Strips out HTML tags and converts encoded entities to readable text
    if not html_text:
        return ""
    tag_pattern = re.compile('<.*?>')
    plain_text = re.sub(tag_pattern, '', html_text)
    decoded_text = unescape(plain_text)
    return clean_text(decoded_text)

def transform_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    # Converts a raw JIRA issue into a cleaner, standardized format
    fields = issue.get('fields', {})
    return {
        'key': issue['key'],
        'summary': clean_text(fields.get('summary', '')),
        'description': remove_html_tags(fields.get('description', '')),
        'status': fields.get('status', {}).get('name', ''),
        'created': fields.get('created', ''),
        'comments': [
            {
                'author': c.get('author', {}).get('displayName', ''),
                'text': remove_html_tags(c.get('body', '')),
                'created': c.get('created', '')
            }
            for c in fields.get('comment', {}).get('comments', [])
        ]
    }
