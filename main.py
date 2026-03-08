import os
import time
from turtle import title
import requests
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

def get_all_accepted_submissions():
    submissions = []
    # TODO: graphql query to fetch all accepted submissions
    return submissions

def get_submission_code(submission_id):
    # TODO: graphql query to fetch code for a given submission_id
    return ""

def commit_to_git(filename, code, timestamp, message):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code)
    
    dt = datetime.fromtimestamp(int(timestamp))
    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    subprocess.run(["git", "add", filename], check=True)
    
    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = date_str
    
    commit_cmd = ["git", "commit", "--date", date_str, "-m", message]
    subprocess.run(commit_cmd, env=env, stdout=subprocess.DEVNULL)
    print(f"commit: {filename} at {date_str}")

def main():
    print("Fetching LeetCode submissions...")
    submissions = get_all_accepted_submissions()

    if not submissions:
        print("No accepted submissions found.")
        return
    
    submissions.sort(key=lambda x: x['timestamp'])

    print(f"Found {len(submissions)} accepted submissions. Processing...")

    for submission in submissions:
        submission_id = submission['id']
        title_slug = submission['titleSlug']
        timestamp = submission['timestamp']
        lang_slug = submission['langSlug']

        question_id = str(submission.get('questionFrontendId', '0'))

        folder_name = f"{question_id.zfill(4)}_{title_slug}"

        os.makedirs(folder_name, exist_ok=True)
        
        ext = EXTENSION_MAP.get(lang_slug, f".{lang_slug}")
        file_name = f"{title_slug}{ext}"
        file_path = os.path.join(folder_name, file_name)
        
        code = get_submission_code(submission_id)
        if not code:
            print(f"Failed to retrieve code for submission {submission_id}. Skipping.")
            continue
        
        commit_message = f"Add/Update {title_slug}"
        commit_to_git(file_path, code, timestamp, commit_message)

        time.sleep(2)

if __name__ == "__main__":
    main()