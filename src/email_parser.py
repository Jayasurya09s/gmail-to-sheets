import base64
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime


def extract_headers(headers):
    data = {}
    for h in headers:
        name = h["name"]
        if name in ["From", "Subject", "Date"]:
            data[name] = h["value"]
    return data


def extract_body(payload):
    body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain" and "data" in part["body"]:
                body = base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8", errors="ignore")
                return body

            if part["mimeType"] == "text/html" and "data" in part["body"]:
                html = base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8", errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                return soup.get_text()

    if "data" in payload.get("body", {}):
        body = base64.urlsafe_b64decode(
            payload["body"]["data"]
        ).decode("utf-8", errors="ignore")

    return body


def parse_email(service, message_id):
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    headers = extract_headers(message["payload"]["headers"])
    body = extract_body(message["payload"])

    date = parsedate_to_datetime(headers.get("Date")).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "from": headers.get("From", ""),
        "subject": headers.get("Subject", ""),
        "date": date,
        "content": body.strip()
    }
