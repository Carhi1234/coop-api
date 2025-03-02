import os
import json
import gspread
from fastapi import FastAPI, Query
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
creds = creds.with_scopes(SCOPES)
client = gspread.authorize(creds)

# Open the Google Sheet
SPREADSHEET_ID = "1ohAvRaQbmlCkXNtC4QFEMT0HdYxy5uFNPGujrAoooD8"  # Replace with your Google Sheet ID
worksheet = client.open_by_key(SPREADSHEET_ID).sheet1  # Open first sheet

# Initialize FastAPI
app = FastAPI()

# Define field names based on the spreadsheet headers
FIELD_NAMES = [
    "Company Name", "Industry", "Location", "Contact Name", "Contact Email",
    "Contact Phone", "Company Website", "Number of Open Positions",
    "Job Description", "Required Skills", "Preferred Skills",
    "Salary", "Application Deadline", "Internship Duration", "Additional Notes"
]

# Endpoint to Read All Companies from the Sheet
@app.get("/companies")
def get_companies():
    try:
        data = worksheet.get_all_records()
        return {"companies": data}
    except Exception as e:
        return {"error": str(e)}

# Endpoint to Search for Companies (By Industry, Location, or Salary)
@app.get("/search")
def search_companies(
    industry: str = Query(None, description="Filter by industry"),
    location: str = Query(None, description="Filter by location"),
    min_salary: float = Query(None, description="Filter by minimum salary")
):
    try:
        all_data = worksheet.get_all_records()
        filtered_data = [
            company for company in all_data
            if (not industry or company.get("Industry") == industry)
            and (not location or company.get("Location") == location)
            and (not min_salary or float(company.get("Salary", 0)) >= min_salary)
        ]
        return {"results": filtered_data}
    except Exception as e:
        return {"error": str(e)}

# Endpoint to Add a New Company
@app.post("/companies")
def add_company(
    company_name: str, industry: str, location: str, contact_name: str,
    contact_email: str, contact_phone: str, company_website: str,
    open_positions: int, job_description: str, required_skills: str,
    preferred_skills: str, salary: float, application_deadline: str,
    internship_duration: str, additional_notes: str
):
    try:
        new_entry = [
            company_name, industry, location, contact_name, contact_email,
            contact_phone, company_website, open_positions, job_description,
            required_skills, preferred_skills, salary, application_deadline,
            internship_duration, additional_notes
        ]
        worksheet.append_row(new_entry)  # Add row to sheet
        return {"message": f"Company '{company_name}' added successfully!"}
    except Exception as e:
        return {"error": str(e)}
