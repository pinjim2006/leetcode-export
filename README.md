# LeetCode Export Tool

[繁體中文](README_zh-TW.md) | [English](README.md)

This is an automated tool designed to fetch Accepted (AC) submissions from LeetCode and synchronize the source code along with its original submission timestamps to a specified local Git repository. This helps developers fully preserve and showcase their problem-solving history on GitHub.

## Project Structure
This tool is intentionally separated from the repository where the actual problem-solving records are stored to ensure a clear separation of concerns.
* `src/sync_history.py`: Batch fetches submission records for all Accepted (AC) problems under the account.
* `src/add_submission.py`: Fetches a single submission record based on a specific Submission ID.
* `src/sync_latest.py`: Automatically finds and syncs the latest Accepted submission record.

---

## 1. Installation and Virtual Environment Setup
It is highly recommended to use a Python Virtual Environment to install dependencies, avoiding conflicts with your system environment.
1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/pinjim2006/leetcode-export.git
    cd leetcode-export
    ```
2. Create a virtual environment (Windows environment):
    ```
    python -m venv venv
    ```
    (Note for macOS/Linux users: Use `python3 -m venv venv`)
3. Activate the virtual environment:
    ```
    venv\Scripts\activate
    ```
    (Note for macOS/Linux users: Use `source venv/bin/activate`)
4. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

---

## 2. Environment Variables Configuration (.env)
This tool relies on environment variables for authentication and path specification. Please create a file named `.env` in the project root directory (you can refer to `.env.example`) and fill in the following information:
```
# LeetCode authentication info (obtain from browser cookies after logging into LeetCode)
LEETCODE_SESSION=your_leetcode_session_value
CSRF_TOKEN=your_csrf_token_value

# Target Git repository path for outputting the submission records (Absolute path with forward slashes / is recommended)
TARGET_REPO_PATH=C:/Users/YourName/Documents/leetcode-practice
```

How to obtain Cookies:
1. Log in to the LeetCode website.
2. Press `F12` to open Developer Tools and navigate to the `Application` (or `Storage`) tab.
3. Expand `Cookies` on the left panel and click on `https://leetcode.com`.
4. Find `LEETCODE_SESSION` and `csrftoken` in the list and copy their corresponding Values.

Note: Ensure that the target path (`TARGET_REPO_PATH`) is an already initialized Git repository (e.g., it has a `.git` folder).

---

## 3. Script Usage
Please make sure to execute the following commands from the project root directory of `leetcode-export` so the scripts can properly read the `.env` file.

### Batch Sync All Historical Records
Used for initial setup. It scans all solved problems and commits them to the Git history sequentially:
```bash
python src/sync_history.py
```

### Sync a Single Submission Record
If you know the specific submission ID (which can be found in the URL of the LeetCode submission record), you can sync it directly:
```bash
python src/add_submission.py <Submission_ID>
```
If the ID is not appended to the command, the program will prompt you for an interactive input.

### One-Click Sync Latest Record (Daily Use)
After solving a new problem and getting an "Accepted" status, run this command to automatically fetch and commit the latest AC record:
```bash
python src/sync_latest.py
```

---

## 4. Disclaimer and Copyright
- This project is an unofficial tool intended solely for personal learning and backing up problem-solving records.
- "LeetCode" and its trademarks are owned by LeetCode LLC. This project has no official affiliation with or sponsorship from LeetCode LLC.
- The scripts include a polite delay mechanism to avoid overloading the servers. Users are advised to comply with LeetCode's Terms of Service and use this tool reasonably. Please do not remove the delay settings to prevent your account or IP from being restricted.

---
## 5. License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.