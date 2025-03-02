import os
import json
import gspread
from fastapi import FastAPI
from google.oauth2.service_account import Credentials

# Load Google Credentials from environment variable
creds_json = os.getenv("GOOGLE_CREDENTIALS")  # Read JSON as a string
if not creds_json:
    raise ValueError("Missing GOOGLE_CREDENTIALS environment variable")

# Convert JSON string to dictionary
try:
    creds_dict = json.loads(creds_json.replace("\n", "\\n"))  # Fix \n issue
    creds = Credentials.from_service_account_info(creds_dict)
except json.JSONDecodeError:
    raise ValueError("Invalid JSON format in GOOGLE_CREDENTIALS!")

# Authenticate with Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(creds)

# Open the Google Sheet
SPREADSHEET_ID = "1ohAvRaQbmlCkXNtC4QFEMT0HdYxy5uFNPGujrAoooD8"  # Replace with your Google Sheet ID
worksheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Initialize FastAPI
app = FastAPI()

# Endpoint to Read All Students from the Sheet
@app.get("/students")
def get_students():
    try:
        data = worksheet.get_all_records()
        return {"students": data}
    except Exception as e:
        return {"error": str(e)}

# Endpoint to Add a New Student
@app.post("/students")
def add_student(name: str, field: str, availability: str):
    try:
        worksheet.append_row([name, field, availability])  # Add row to sheet
        return {"message": f"Student {name} added successfully!"}
    except Exception as e:
        return {"error": str(e)}
