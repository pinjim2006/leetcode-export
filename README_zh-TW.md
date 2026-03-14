# LeetCode Export Tool

[繁體中文](README_zh-TW.md) | [English](README.md)

這是一個自動化工具，用於抓取 LeetCode 上已通過 (Accepted) 的提交紀錄，並將程式碼與原始的提交時間戳記 (Timestamp) 同步到本地指定的 Git 儲存庫中。這有助於開發者在 GitHub 上完整保留並展示過去的解題歷程。

## 專案結構
本工具與存放解題紀錄的儲存庫是分離的，以確保專案職責清晰。
- `src/sync_history.py`: 批次抓取帳號內所有 AC 題目的提交紀錄。
- `src/add_submission.py`: 根據指定的 Submission ID 抓取單筆紀錄。
- `src/sync_latest.py`: 自動尋找並同步最新一筆 AC 的提交紀錄。

---

## 1. 安裝與虛擬環境設定
建議使用 Python 虛擬環境 (Virtual Environment) 來安裝相依套件，避免干擾系統環境。
1. 複製此專案到本地：
    ```bash
    git clone https://github.com/pinjim2006/leetcode-export.git
    cd leetcode-export
    ```
2. 建立虛擬環境 (Windows 環境)：
    ```
    python -m venv venv
    ```
    (macOS/Linux 使用者: 使用 `python3 -m venv venv`)
3. 啟動虛擬環境：
    ```
    venv\Scripts\activate
    ```
    (macOS/Linux 使用者: 使用 `source venv/bin/activate`)
4. 安裝相依套件：
    ```
    pip install -r requirements.txt
    ```

---

## 2. 環境變數設定 (.env)
本工具依賴環境變數來進行身分驗證與路徑指定。請在專案根目錄下建立一個名為 `.env` 的檔案（可參考 `.env.example`），並填入以下資訊：
```
# LeetCode 驗證資訊 (請登入 LeetCode 後從瀏覽器的 Cookie 中取得)
LEETCODE_SESSION=你的_leetcode_session_值
CSRF_TOKEN=你的_csrf_token_值

# 解題紀錄要輸出的目標 Git 儲存庫路徑 (建議使用絕對路徑，並使用正斜線 /)
TARGET_REPO_PATH=C:/Users/YourName/Documents/leetcode-practice
```

如何取得 Cookie：
1. 登入 LeetCode 網站。
2. 按下 `F12` 打開開發者工具，進入 `Application` (或 `Storage`) 標籤頁。
3. 展開左側的 `Cookies`點擊 `https://leetcode.com`。
4. 在列表中找到 `LEETCODE_SESSION` 與 `csrftoken`，複製其對應的 Value。

注意： 確保目標路徑 (`TARGET_REPO_PATH`) 已經是一個初始化過的 Git 儲存庫 (`git init`)。

---

## 3. 腳本使用方式
請務必在 `leetcode-export` 的專案根目錄下執行以下指令，確保程式能正確讀取 `.env` 檔案。

### 批次同步所有歷史紀錄
用於初次建置，會掃描所有已解決的題目並依序寫入 Git 歷史：
```bash
python src/sync_history.py
```

### 同步單一提交紀錄
若你已知特定提交的 ID（可從 LeetCode 提交紀錄的網址中取得），可直接指定同步：
```bash
python src/add_submission.py <Submission_ID>
```
若未在指令後方加上 ID，程式會以互動式提示要求輸入。

### 一鍵同步最新紀錄
寫完新題目並獲得 Accepted 後，執行此指令即可自動抓取最新一筆 AC 紀錄並提交：
```bash
python src/sync_latest.py
```

---

## 4. 免責與版權聲明
- 本專案為非官方工具，僅供個人學習與備份解題紀錄使用。
- "LeetCode" 及其商標為 LeetCode LLC 所有。本專案與 LeetCode LLC 無任何官方關聯或贊助關係。
- 程式中包含友善的延遲機制 (Polite Delay) 以避免對伺服器造成負擔。請使用者遵守 LeetCode 的服務條款，合理使用本工具，請勿移除延遲設定以避免帳號或 IP 遭受限制。

---
## 5. License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.