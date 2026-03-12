import os
import sys
import requests
from config import HEADERS, API_URL, EXTENSION_MAP, TARGET_REPO_PATH, commit_to_git

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

def process_submission(submission_id):
    submission_details = get_submission_data(submission_id)
    if not submission_details:
        return

    code = submission_details["code"]
    timestamp = submission_details["timestamp"]
    lang_name = submission_details["lang"]["name"]
    question_id = str(submission_details["question"]["questionId"])
    title_slug = submission_details["question"]["titleSlug"]

    folder_name = f"{question_id.zfill(4)}_{title_slug}"
    os.makedirs(os.path.join(TARGET_REPO_PATH, folder_name), exist_ok=True)
    
    ext = EXTENSION_MAP.get(lang_name, f".{lang_name}")
    file_path = os.path.join(TARGET_REPO_PATH, folder_name, f"{title_slug}{ext}")
    
    # Git
    commit_to_git(file_path, code, timestamp, f"Add/Update {title_slug} ({lang_name})")

def main():
    if len(sys.argv) > 1:
        submission_id = sys.argv[1]
    else:
        submission_id = input("Enter the submission ID: ").strip()

    if not submission_id.isdigit():
        print("ERROR: Submission ID must be a number.")
        return

    print(f"Fetching details for submission ID: {submission_id}...")
    process_submission(submission_id)

    print("submission processing complete!")


if __name__ == "__main__":
    main()