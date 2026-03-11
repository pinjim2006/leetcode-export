import os
import sys
import time
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

def get_submission_data(submission_id):
    """Fetch all details of a submission directly using its ID"""
    query = """
    query submissionDetails($submissionId: Int!) {
        submissionDetails(submissionId: $submissionId) {
            code
            timestamp
            lang {
                name
            }
            question {
                questionId
                titleSlug
            }
        }
    }
    """
    payload = {
        "query": query,
        "variables": {"submissionId": int(submission_id)}
    }
    
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    data = response.json()
    
    if "errors" in data:
        print(f"Failed to fetch submission data, please check the submission ID or token: {data['errors']}")
        return None
        
    return data.get("data", {}).get("submissionDetails")

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

def main():
    if len(sys.argv) > 1:
        submission_id = sys.argv[1]
    else:
        submission_id = input("Enter the submission ID: ").strip()

    if not submission_id.isdigit():
        print("ERROR: Submission ID must be a number.")
        return

    print(f"Fetching details for submission ID: {submission_id}...")
    submission_details = get_submission_data(submission_id)

    code = submission_details["code"]
    timestamp = submission_details["timestamp"]
    lang_name = submission_details["lang"]["name"]
    question_id = str(submission_details["question"]["questionId"])
    title_slug = submission_details["question"]["titleSlug"]

    folder_name = f"{question_id.zfill(4)}_{title_slug}"
    os.makedirs(folder_name, exist_ok=True)
    
    ext = EXTENSION_MAP.get(lang_name, f".{lang_name}")
    file_path = os.path.join(folder_name, f"{title_slug}{ext}")
    
    # Git
    commit_to_git(file_path, code, timestamp, f"Add/Update {title_slug} ({lang_name})")

if __name__ == "__main__":
    main()