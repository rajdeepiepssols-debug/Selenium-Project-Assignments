"""
data_reader.py
--------------
Satisfies capstone requirement #8: "Read test data from Excel/JSON".
Both readers are implemented; tests default to JSON but can switch
to Excel by changing DATA_SOURCE below or passing source="excel".
"""

import json
import os

import openpyxl

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def read_json_data(filename: str = "test_data.json") -> dict:
    path = os.path.join(TEST_DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_excel_data(filename: str = "test_data.xlsx", sheet_name: str = "TestData") -> list:
    """
    Reads tabular test cases from an Excel sheet and returns a list of dicts,
    using row 1 as headers. Example row -> {"case_id": "TC01", "search_term": "Blue Top", "quantity": "3"}
    """
    path = os.path.join(TEST_DATA_DIR, filename)
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.active

    rows = list(ws.iter_rows(values_only=True))
    headers = rows[0]
    records = []
    for row in rows[1:]:
        record = {headers[i]: row[i] for i in range(len(headers))}
        records.append(record)
    return records


def get_test_cases(source: str = "json") -> list:
    """
    Unified accessor used by the test suite. Returns a list of test case dicts
    regardless of whether the underlying source is JSON or Excel.
    """
    if source == "excel":
        return read_excel_data()
    data = read_json_data()
    return data["test_cases"]


def get_user_data() -> dict:
    """User/account fields always come from JSON (kept out of the tabular Excel sheet)."""
    data = read_json_data()
    return data["user"]


def get_payment_data() -> dict:
    """Dummy card details used to complete checkout (this demo site accepts any values)."""
    data = read_json_data()
    return data["payment"]
