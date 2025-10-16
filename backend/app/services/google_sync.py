from pathlib import Path
from typing import List

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from ..core.config import get_settings

settings = get_settings()

def get_client() -> gspread.Client:
    if not settings.google_service_account_json:
        raise ValueError("Google service account JSON not configured")
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(str(Path(settings.google_service_account_json)), scopes)
    return gspread.authorize(credentials)


def fetch_sheet_rows() -> List[List[str]]:
    if not settings.google_sheet_id:
        raise ValueError("Google sheet ID not configured")
    client = get_client()
    sheet = client.open_by_key(settings.google_sheet_id).sheet1
    return sheet.get_all_values()
