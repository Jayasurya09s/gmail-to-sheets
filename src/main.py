from src.sync_service import run_email_sync


if __name__ == "__main__":
    result = run_email_sync()
    print("Email sync completed successfully.")
    print(result)
