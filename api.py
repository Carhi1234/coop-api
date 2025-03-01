from fastapi import FastAPI
import gspread
from google.oauth2.service_account import Credentials

# Authenticate with Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open your Google Sheet
SPREADSHEET_ID = "your_google_sheet_id_here"  # Change this to your actual Google Sheet ID
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
