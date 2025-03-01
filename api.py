from fastapi import FastAPI
import gspread
import json
import os
from google.oauth2.service_account import Credentials

# Authenticate with Google Sheets API using environment variable
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds_json = os.getenv("GOOGLE_CREDENTIALS")

if creds_json:
    creds_dict = json.loads(creds_json)  # Load JSON string as dictionary
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
else:
    raise FileNotFoundError("GOOGLE_CREDENTIALS environment variable not found")

client = gspread.authorize(creds)

# Open your Google Sheet
SPREADSHEET_ID = "1ohAvRaQbmlCkXNtC4QFEMT0HdYxy5uFNPGujrAoooD8"  # Change this to your actual Google Sheet ID
worksheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Create FastAPI app
app = FastAPI()

# Endpoint to get all students looking for co-ops
@app.get("/students")
def get_students():
    data = worksheet.get_all_records()
    return {"students": data}

# Endpoint to add a new student
@app.post("/students")
def add_student(name: str, field: str, availability: str):
    worksheet.append_row([name, field, availability])
    return {"message": f"Student {name} added successfully!"}

# Run the API (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
