import os
import json
import sys
from openai import OpenAI
from github import Github

# 1. Load environment variables
api_key = os.getenv("DEEPSEEK_API_KEY2")
github_token = os.getenv("GITHUB_TOKEN")
event_path = os.getenv("GITHUB_EVENT_PATH")

if not api_key or not github_token or not event_path:
    print("Missing required environment variables")
    sys.exit(1)

# 2. Read the GitHub event data
try:
    with open(event_path, 'r') as f:
        event_data = json.load(f)
except Exception as e:
    print(f"Failed to read event data: {e}")
    sys.exit(1)

# Get the comment body, issue/PR number, and repo name
comment_body = event_data.get('comment', {}).get('body', '')
issue_number = event_data.get('issue', {}).get('number')
repo_full_name = os.getenv("GITHUB_REPOSITORY")

if not comment_body or not issue_number:
    print("Could not find comment or issue number in event data.")
    sys.exit(1)

# 3. Initialize DeepSeek and GitHub clients
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"  # This is what points it to DeepSeek instead of OpenAI
)
github = Github(github_token)
repo = github.get_repo(repo_full_name)

# 4. Send the user's comment to DeepSeek
system_prompt = """You are a senior software engineer and code reviewer. 
You are helping a user review code and make decisions. 
Be clear, helpful, and direct in your advice."""

try:
    response = client.chat.completions.create(
        model="deepseek-chat",  # Or use "deepseek-coder" if you prefer
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"The user triggered this action with this comment: '{comment_body}'. Please respond as a helpful coding assistant."}
        ],
        max_tokens=1024
    )
    ai_reply = response.choices[0].message.content
except Exception as e:
    ai_reply = f"Sorry, I encountered an error trying to reach DeepSeek: {e}"

# 5. Post DeepSeek's response back to the GitHub issue/PR comment section
try:
    issue = repo.get_issue(number=issue_number)
    issue.create_comment(ai_reply)
    print(f"Successfully posted reply to issue #{issue_number}")
except Exception as e:
    print(f"Failed to post comment to GitHub: {e}")
