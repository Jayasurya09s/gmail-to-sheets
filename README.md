# 📧 Gmail to Google Sheets Automation

**Author:** Midde Jayanth

## 📖 Project Overview

This project is a Python-based automation system that connects to the Gmail API and Google Sheets API to automatically read real incoming emails from a Gmail account and log them into a Google Sheet.

The system processes only unread emails from the inbox, extracts relevant information, appends it to a Google Sheet, and then marks the emails as read. It is designed to be idempotent, meaning re-running the script does not create duplicate entries.

## 🎯 Objective

Each qualifying email is added as a new row in a Google Sheet with the following columns:

| Column | Description |
|--------|-------------|
| From | Sender email address |
| Subject | Email subject |
| Date | Date & time received |
| Content | Email body (plain text) |

## 🏗️ High-Level Architecture

```
┌────────────┐
│   Gmail    │
│  (Inbox)   │
└─────┬──────┘
      │  Gmail API (OAuth 2.0)
      ▼
┌────────────┐
│  Python    │
│ Automation │
│  Script    │
│ (Parsing +│
│  State)   │
└─────┬──────┘
      │  Google Sheets API
      ▼
┌────────────┐
│ Google     │
│ Sheets     │
│ (Rows)     │
└────────────┘
```

## 🛠️ Technologies Used

- **Language:** Python 3.8+
- **APIs:**
  - Google Gmail API
  - Google Sheets API
- **Authentication:** OAuth 2.0 (Installed App Flow)
- **Libraries:**
  - `google-api-python-client` - Interface for Gmail and Sheets APIs
  - `google-auth` - Google authentication library
  - `google-auth-oauthlib` - OAuth 2.0 flow implementation
  - `google-auth-httplib2` - HTTP transport for Google Auth
  - `beautifulsoup4` - HTML email content parsing
  - `python-dateutil` - Date parsing and manipulation

## 📋 Prerequisites

- **Python 3.8 or higher** installed on your system
- A **Google Account** with Gmail access
- A **Google Cloud Platform** account (free tier works)
- Basic knowledge of Python and command-line operations
- Internet connection for API calls

## 📂 Project Structure

```
gmail-to-sheets/
│
├── src/
│   ├── gmail_service.py
│   ├── sheets_service.py
│   ├── email_parser.py
│   └── main.py
│
├── credentials/
│   └── credentials.json   (DO NOT COMMIT)
│
├── proof/
│   ├── gmail_unread.png
│   ├── google_sheet_rows.png
│   └── oauth_consent.png
│
├── .gitignore
├── requirements.txt
├── README.md
└── state.json
```

## ⚙️ Setup Instructions (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-link>
cd gmail-to-sheets
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Google Cloud Configuration

1. **Create a Google Cloud project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click "New Project"
   - Name your project (e.g., "Gmail to Sheets")

2. **Enable APIs:**
   - Navigate to "APIs & Services" → "Library"
   - Search and enable:
     - Gmail API
     - Google Sheets API

3. **Configure OAuth Consent Screen:**
   - Go to "APIs & Services" → "OAuth consent screen"
   - User type: **External**
   - App name: Your choice
   - Add your email as test user
   - Required scopes are added automatically

4. **Create OAuth Client ID:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: **Desktop app**
   - Download the JSON file

5. **Place credentials:**
   - Rename downloaded file to `credentials.json`
   - Create `credentials/` folder if it doesn't exist
   - Move file to: `credentials/credentials.json`

### 5️⃣ Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new blank spreadsheet
3. Add headers in the first row:
   ```
   From | Subject | Date | Content
   ```
4. Copy the **Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
   ```
5. Open `src/config.py` and update:
   ```python
   SPREADSHEET_ID = "your-spreadsheet-id-here"
   ```

### 6️⃣ Run the Script

```bash
python src/main.py
```

On first run, a browser window opens for OAuth authentication.

## 🔐 OAuth 2.0 Flow Explanation

This project uses Google OAuth 2.0 Installed App Flow:

- The user authenticates via a browser consent screen.
- Required scopes:
  - `https://www.googleapis.com/auth/gmail.modify`
  - `https://www.googleapis.com/auth/spreadsheets`
- After successful login, Google issues access and refresh tokens.
- Tokens are stored locally in `token.json` (ignored via `.gitignore`).

This approach is secure and avoids exposing passwords or API keys.

**Token Management:**

- `token.json` is automatically created after first successful authentication
- Contains access token (short-lived) and refresh token (long-lived)
- Access tokens expire after ~1 hour, but are automatically refreshed
- Delete `token.json` to re-authenticate if issues arise

## 🔁 Duplicate Prevention Logic

To prevent duplicate rows:

- Each Gmail message has a unique **message ID**
- Processed message IDs are stored in a local file:
  ```
  state.json
  ```
- Before processing an email, the script checks:
  - If the message ID already exists in `state.json`
  - If yes → it is skipped

This ensures idempotent execution.

## 🧠 State Persistence Method

State is stored locally in `state.json` as a list of processed Gmail message IDs.

**Why this approach?**

- Simple and reliable
- Independent of Gmail read/unread state
- Prevents duplicates even if Gmail re-flags emails as unread
- Works across multiple script runs

## ⚠️ Error Handling & Edge Cases

- **Google Sheets has a 50,000 character cell limit**  
  → Long email bodies are safely truncated
- Each email is processed inside a `try / except / finally` block
- Emails are always marked as read and saved to state, even if partial failures occur

This makes the system fault-tolerant.

## 🚧 Challenges Faced & Solutions

**Challenge:**

Some marketing emails exceeded Google Sheets' maximum cell size, causing API errors.

**Solution:**

Implemented a content length check and safely truncated long email bodies before insertion, preventing runtime failures.

## ⚠️ Limitations

- Processes only inbox emails
- Depends on Gmail API quota limits (250 quota units per user per second)
- State is stored locally (not shared across machines)
- Does not currently filter by email category (Promotions/Social)
- Maximum 50,000 characters per cell in Google Sheets

## 🔒 Security Best Practices

**Never commit sensitive files:**

- `credentials/credentials.json` - Contains OAuth client secrets
- `token.json` - Contains your personal access tokens
- `state.json` - May contain message IDs (privacy concern)

**The `.gitignore` file already excludes these files.**

To verify:
```bash
git status
```

Ensure no sensitive files appear in the staging area.

## 📊 API Quotas & Rate Limits

**Gmail API:**
- Daily quota: 1,000,000,000 quota units
- Per-user rate limit: 250 quota units/second
- Reading a message: ~5 quota units
- Modifying a message: ~5 quota units

**Google Sheets API:**
- Read requests: 300 per minute per project
- Write requests: 300 per minute per project

**This script stays well within these limits for normal usage.**

## 🔧 Troubleshooting

### Issue: "File not found: credentials.json"
**Solution:** Ensure `credentials.json` is in the `credentials/` folder.

### Issue: "Invalid grant" or "Token expired"
**Solution:** Delete `token.json` and re-authenticate:
```bash
del token.json
python src/main.py
```

### Issue: "HttpError 403: Request had insufficient authentication scopes"
**Solution:** Delete `token.json`, update scopes in `config.py`, then re-run.

### Issue: "PERMISSION_DENIED: The caller does not have permission"
**Solution:** Make sure you're logged into the correct Google account and the Sheet is accessible.

### Issue: Script hangs or times out
**Solution:** Check your internet connection and Gmail API status at [Google Workspace Status](https://www.google.com/appsstatus).

### Issue: Empty or malformed email content
**Solution:** Some emails may have complex MIME structures. The parser handles most cases, but edge cases may occur.

## ⏰ Scheduling Automation

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily (or your preferred frequency)
4. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `src/main.py`
   - Start in: `C:\Users\jayan\Desktop\gmail-to-sheets`

### Linux/macOS (Cron)

Add to crontab:
```bash
# Run every hour
0 * * * * cd /path/to/gmail-to-sheets && /path/to/venv/bin/python src/main.py
```

## 🧪 Testing the Setup

1. Send yourself a test email
2. Run the script:
   ```bash
   python src/main.py
   ```
3. Check your Google Sheet for the new row
4. Run the script again - verify no duplicate appears
5. Send another test email and repeat

## ❓ FAQ

**Q: Can I use this with multiple Gmail accounts?**  
A: Yes, but you need separate `token.json` files for each account. Consider using different directories.

**Q: Will this work with G Suite/Google Workspace accounts?**  
A: Yes, but your workspace admin must allow API access.

**Q: Can I filter emails by sender or subject?**  
A: Yes! Modify the `list_unread_emails()` function in `gmail_service.py` to add Gmail query filters.

**Q: What happens if I delete `state.json`?**  
A: The script will re-process all unread emails, potentially creating duplicates. Keep this file safe.

**Q: Can I run this on a server?**  
A: Yes, but the OAuth flow requires a browser for first-time setup. Use a machine with a GUI first, then copy `token.json` to your server.

**Q: How do I process emails from specific labels?**  
A: Modify the Gmail API query in `gmail_service.py` to include `labelIds` parameter.

## 📸 Proof of Execution

All proofs are available in the `/proof` folder:

- Gmail inbox with unread emails
- Google Sheet populated with email data
- OAuth consent screen
- Screen recording (2–3 minutes) explaining:
  - Project flow
  - Gmail → Sheets integration
  - Duplicate prevention
  - Re-run behavior

## 🔄 Re-run Behavior

- **First run:** unread emails are logged and marked as read
- **Subsequent runs:** no duplicate rows are added
- **New unread emails** are processed automatically

## ⭐ Bonus Features Implemented

- HTML → Plain text email parsing
- Robust error handling
- Content truncation for large emails

## 📦 Dependencies Explained

| Package | Purpose |
|---------|----------|
| `google-api-python-client` | Core library for interacting with Google APIs |
| `google-auth` | Authentication library for Google services |
| `google-auth-oauthlib` | OAuth 2.0 authorization flow implementation |
| `google-auth-httplib2` | HTTP transport adapter for Google Auth |
| `beautifulsoup4` | Parses HTML email content into plain text |
| `python-dateutil` | Handles date parsing from email headers |

## 🎯 Key Features Summary

✅ **Automatic Email Processing** - Reads unread emails without manual intervention  
✅ **Duplicate Prevention** - Message ID tracking ensures no duplicate rows  
✅ **OAuth 2.0 Security** - Industry-standard authentication  
✅ **Error Resilient** - Handles API failures and malformed emails gracefully  
✅ **Content Sanitization** - Converts HTML to plain text and truncates long content  
✅ **State Persistence** - Tracks processed emails across runs  
✅ **Idempotent Design** - Safe to run multiple times  

## ✅ Final Notes

This project demonstrates:

- Real-world API integration
- Secure OAuth authentication
- Stateful automation design
- Production-grade error handling
- Idempotent execution patterns
- API quota management

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [FAQ](#-faq)
3. Verify your setup against [Setup Instructions](#-setup-instructions-step-by-step)

---

**📌 Author:** Midde Jayanth
