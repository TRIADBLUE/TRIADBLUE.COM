import os
import json
import sys
from anthropic import Anthropic
from github import Github

# 1. Load environment variables
api_key = os.getenv("ANTHROPIC_API_KEY")
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

# 3. Initialize AI and GitHub clients
claude = Anthropic(api_key=api_key)
github = Github(github_token)
repo = github.get_repo(repo_full_name)

# (Optional: If this is a Pull Request, you could fetch the PR diff here to give Claude context!)
# pr = repo.get_pull(issue_number)
# diff = pr.get_files() # ... etc

# 4. Send the user's comment to Claude
system_prompt = """You are a senior software engineer and code reviewer. 
You are helping a user review code and make decisions. 
Be clear, helpful, and direct in your advice."""

try:
    response = claude.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"The user triggered this action with this comment: '{comment_body}'. Please respond as a helpful coding assistant."}
        ]
    )
    ai_reply = response.content[0].text
except Exception as e:
    ai_reply = f"Sorry, I encountered an error trying to reach the AI: {e}"

# 5. Post Claude's response back to the GitHub issue/PR comment section
try:
    issue = repo.get_issue(number=issue_number)
    issue.create_comment(ai_reply)
    print(f"Successfully posted reply to issue #{issue_number}")
except Exception as e:
    print(f"Failed to post comment to GitHub: {e}")
