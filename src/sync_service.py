import json
import os
from datetime import datetime

from src.gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from src.sheets_service import get_sheets_service, append_row
from src.email_parser import parse_email
from src.config import SPREADSHEET_ID, MAX_CELL_LENGTH


STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"processed_ids": []}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def run_email_sync():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    state = load_state()
    processed_ids = set(state.get("processed_ids", []))

    messages = fetch_unread_emails(gmail_service)

    processed_count = 0

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

            processed_count += 1

        except Exception as e:
            print(f"Error processing message {msg_id}: {e}")

        finally:
            mark_as_read(gmail_service, msg_id)
            processed_ids.add(msg_id)

    save_state({"processed_ids": list(processed_ids)})

    return {
        "status": "success",
        "processed_emails": processed_count,
        "timestamp": datetime.utcnow().isoformat()
    }
