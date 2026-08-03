import os
import json
import sys
import traceback
from openai import OpenAI
from github import Github

try:
    # 1. Load environment variables
    api_key = os.getenv("DEEPSEEK_API_KEY2")
    github_token = os.getenv("GITHUB_TOKEN")
    event_path = os.getenv("GITHUB_EVENT_PATH")

    if not api_key or not github_token or not event_path:
        raise Exception(f"Missing env vars. API_KEY present: {bool(api_key)}, TOKEN present: {bool(github_token)}")

    # 2. Read event data
    with open(event_path, 'r') as f:
        event_data = json.load(f)

    comment_body = event_data.get('comment', {}).get('body', '')
    issue_number = event_data.get('issue', {}).get('number')
    repo_full_name = os.getenv("GITHUB_REPOSITORY")

    if not comment_body or not issue_number:
        raise Exception("Could not find comment or issue number.")

    # 3. Init DeepSeek and GitHub
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    github = Github(github_token)
    repo = github.get_repo(repo_full_name)

    # 4. Post a success message so we know it worked!
    issue = repo.get_issue(number=issue_number)
    issue.create_comment(
        "✅ **DEBUG SUCCESS!** The Python environment is alive, and your GitHub token and DeepSeek API key are correctly passed. "
        "We are now ready to swap this file for the full ecosystem review script."
    )

except Exception as e:
    # If anything breaks, we print the full traceback to the Actions log AND post it to the issue!
    error_msg = f"🔥 CRASH REPORT:\n```\n{traceback.format_exc()}\n```"
    print(error_msg)
    try:
        # Try to post the error back to the GitHub issue so you see it right there
        if 'issue' in locals():
            issue.create_comment(f"🚨 The script crashed with this error:\n\n{error_msg}")
    except:
        pass
    sys.exit(1)
