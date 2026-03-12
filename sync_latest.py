import os
import sys
import requests
from config import HEADERS, API_URL
from add_submission import process_submission

def get_latest_ac_submission_id():
    """fetch the latest accepted submission ID for a question"""
    query = """
    query submissionList($offset: Int!, $limit: Int!) {
        submissionList(offset: $offset, limit: $limit) {
            submissions {
                id
                statusDisplay
            }
        }
    }
    """
    payload = {
        "query": query,
        "variables": {"offset": 0, "limit": 20} # Only fetch the most recent 20 submissions
    }
    
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    data = response.json()
    
    submissions = data.get("data", {}).get("submissionList", {}).get("submissions", [])
    
    for sub in submissions:
        if sub.get("statusDisplay") == "Accepted":
            return sub["id"]
            
    return None

def main():
    print("Fetching the latest accepted submission ID...")
    latest_ac_id = get_latest_ac_submission_id()
    
    if not latest_ac_id:
        print("No accepted submissions found.")
        return
    
    print(f"Latest accepted submission ID: {latest_ac_id}")

    process_submission(latest_ac_id)

if __name__ == "__main__":
    main()