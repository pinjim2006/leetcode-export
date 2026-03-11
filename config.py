import os
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRF_TOKEN = os.getenv("CSRF_TOKEN")

if not LEETCODE_SESSION or not CSRF_TOKEN:
    print("ERROR: Please set LEETCODE_SESSION and CSRF_TOKEN in the .env file.")
    exit(1)

HEADERS = {
    'Content-Type': 'application/json',
    'x-csrftoken': CSRF_TOKEN,
    'Cookie': f'LEETCODE_SESSION={LEETCODE_SESSION}; csrftoken={CSRF_TOKEN};'
}
API_URL = "https://leetcode.com/graphql"

EXTENSION_MAP = {
    "c": ".c",
    "cpp": ".cpp",
    "java": ".java",
    "python": ".py",
    "python3": ".py",
    "golang": ".go",
    "javascript": ".js",
    "typescript": ".ts",
    "csharp": ".cs",
    "ruby": ".rb",
    "swift": ".swift",
    "scala": ".scala",
    "kotlin": ".kt",
    "rust": ".rs",
    "php": ".php",
    "mysql": ".sql",
    "mssql": ".sql",
    "oraclesql": ".sql"
}

def commit_to_git(file_path, code, timestamp, message):
    """Write to file and perform time-travel commit"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    
    dt = datetime.fromtimestamp(int(timestamp))
    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    subprocess.run(["git", "add", file_path], check=True)
    
    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = date_str
    
    commit_cmd = ["git", "commit", "--date", date_str, "-m", message]
    subprocess.run(commit_cmd, env=env, stdout=subprocess.DEVNULL)
    print(f"Committed: {file_path} (Time: {date_str})")