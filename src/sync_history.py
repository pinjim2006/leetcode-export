import os
import time
import requests
from config import HEADERS, API_URL, EXTENSION_MAP, commit_to_git

def get_all_ac_questions():
    """[Tier 1] Fetch the list of all accepted questions"""
    print("[Tier 1] Scanning the question bank for accepted questions...")
    ac_questions = []
    skip = 0
    limit = 50
    total_num = 1 # Initial assumed value, will be updated in the loop

    query = """
    query userProgressQuestionList($filters: UserProgressQuestionListInput) {
        userProgressQuestionList(filters: $filters) {
            totalNum
            questions {
                frontendId
                titleSlug
                questionStatus
            }
        }
    }
    """

    while skip < total_num:
        payload = {
            "query": query,
            "variables": {"filters": {"skip": skip, "limit": limit}}
        }
        
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        data = response.json()
        
        progress_data = data.get("data", {}).get("userProgressQuestionList", {})
        total_num = progress_data.get("totalNum", 0)
        questions = progress_data.get("questions", [])

        if not questions:
            break

        for q in questions:

            if str(q.get("questionStatus")) == "SOLVED":
                ac_questions.append({
                    "frontendId": q.get("frontendId"),
                    "titleSlug": q.get("titleSlug")
                })

        print(f"   Scanned {skip + len(questions)} / {total_num} questions...")
        skip += limit
        time.sleep(1)

    return ac_questions

def get_submissions_for_question(title_slug, frontend_id):
    """[Tier 2] Fetch all accepted submission IDs for a single question"""
    submissions = []
    offset = 0
    limit = 20

    query = """
    query userProgressSubmissionList($offset: Int!, $limit: Int!, $questionSlug: String!) {
        userProgressSubmissionList(offset: $offset, limit: $limit, questionSlug: $questionSlug) {
            totalNum
            submissions {
                id
                status
                langName
                timestamp
            }
        }
    }
    """

    while True:
        payload = {
            "query": query,
            "variables": {
                "offset": offset,
                "limit": limit,
                "questionSlug": title_slug
            }
        }

        response = requests.post(API_URL, json=payload, headers=HEADERS)
        data = response.json()

        sub_list_data = data.get("data", {}).get("userProgressSubmissionList", {})
        if not sub_list_data:
            break

        subs = sub_list_data.get("submissions", [])
        if not subs:
            break

        for sub in subs:
            if sub.get("status") == 10: # 10 represents Accepted
                submissions.append({
                    "id": sub["id"],
                    "timestamp": sub["timestamp"],
                    "langName": sub.get("langName", "txt").lower(),
                    "titleSlug": title_slug,
                    "frontendId": frontend_id
                })

        total_sub_num = sub_list_data.get("totalNum", 0)
        offset += limit
        if offset >= total_sub_num:
            break
        
        time.sleep(1.5)

    return submissions

def get_submission_code(submission_id):
    """[Tier 3] Fetch the actual code using the submission ID"""
    query = """
    query submissionDetails($submissionId: Int!) {
        submissionDetails(submissionId: $submissionId) {
            code
        }
    }
    """
    payload = {
        "query": query,
        "variables": {"submissionId": int(submission_id)}
    }
    
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    data = response.json()
    return data.get("data", {}).get("submissionDetails", {}).get("code")

def main():
    print("Fetching LeetCode submissions...")

    ac_questions = get_all_ac_questions()
    print(f"[Tier 1 Complete] Found {len(ac_questions)} accepted questions!\n")
    
    # test_q_limit = 2
    # print(f"[Testing mode] Tier 2 reduced to only query the first {test_q_limit} questions...")
    # ac_questions = ac_questions[:test_q_limit]

    print("[Tier 2] Collecting accepted submission records for each question (this may take some time)...")
    all_ac_submissions = []
    for idx, q in enumerate(ac_questions, 1):
        print(f"   ({idx}/{len(ac_questions)}) Querying: {q['titleSlug']}")
        subs = get_submissions_for_question(q['titleSlug'], q['frontendId'])
        all_ac_submissions.extend(subs)
        time.sleep(1.5) # Avoid frequent API requests

    print(f"\n[Tier 2 Complete] Collected {len(all_ac_submissions)} accepted submission records!\n")

    # 3. Sort by time globally (this ensures the Git history is completely correct)
    all_ac_submissions.sort(key=lambda x: int(x['timestamp']))

    # Test brake mechanism: only process the first 3 entries to confirm it's working!
    # Confirm the operation is normal, then delete or comment out the following line,
    # and run again.
    # test_limit = 3
    # print(f"Currently in test mode, only processing the first {test_limit} entries. Please confirm the directory and file creation is correct.")
    # all_ac_submissions = all_ac_submissions[:test_limit]

    # 4. Start downloading code and writing to Git history
    print("[Tier 3] Downloading code and writing to Git history...")
    for sub in all_ac_submissions:
        sub_id = sub['id']
        title_slug = sub['titleSlug']
        frontend_id = str(sub['frontendId'])
        timestamp = sub['timestamp']
        lang_name = sub['langName']

        code = get_submission_code(sub_id)
        if not code:
            print(f"   Failed to fetch code (ID: {sub_id})")
            continue
        
        # Build directory and path
        folder_name = f"{frontend_id.zfill(4)}_{title_slug}"
        os.makedirs(folder_name, exist_ok=True)
        
        ext = EXTENSION_MAP.get(lang_name, f".{lang_name}")
        file_path = os.path.join(folder_name, f"{title_slug}{ext}")
        
        commit_message = f"Add/Update {title_slug} ({lang_name})"
        commit_to_git(file_path, code, timestamp, commit_message)

        time.sleep(2)

if __name__ == "__main__":
    main()