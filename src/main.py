from gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from sheets_service import get_sheets_service, append_row
from email_parser import parse_email
from config import SPREADSHEET_ID, MAX_CELL_LENGTH
import json
import os

STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"processed_ids": []}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


if __name__ == "__main__":
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    state = load_state()
    processed_ids = set(state.get("processed_ids", []))

    messages = fetch_unread_emails(gmail_service)

    if not messages:
        print("No unread emails found.")
    else:
        print(f"Processing {len(messages)} unread emails...")

    for msg in messages:
        msg_id = msg["id"]

        if msg_id in processed_ids:
            continue

        try:
            email = parse_email(gmail_service, msg_id)

            content = email["content"]
            if len(content) > MAX_CELL_LENGTH:
                content = content[:MAX_CELL_LENGTH] + "\n\n[TRUNCATED]"

            append_row(
                sheets_service,
                SPREADSHEET_ID,
                [
                    email["from"],
                    email["subject"],
                    email["date"],
                    content
                ]
            )

            print(f"✔ Added email: {email['subject']}")

        except Exception as e:
            print(f"⚠ Error processing message {msg_id}: {e}")

        finally:
            # 🔐 Finalize email no matter what
            mark_as_read(gmail_service, msg_id)
            processed_ids.add(msg_id)

    save_state({"processed_ids": list(processed_ids)})

    print("✅ Email sync completed successfully.")
