from fastapi import APIRouter, Request, Form
from config import settings
import base64
import json
from google.oauth2 import service_account
import gspread
from fastapi.responses import HTMLResponse

# Initialize FastAPI router
router = APIRouter(prefix="/googlesheets", tags=["Google Sheets"])

def get_google_sheets_client():
    """Create and return a Google Sheets client using the service account."""
    try:
        # Decode the base64 service account JSON
        decoded_bytes = base64.b64decode(settings.GOOGLE_SHEET_SERVICE_ACCOUNT_SHEETS)
        service_account_info = json.loads(decoded_bytes.decode('utf-8'))
        
        # Create credentials and authorize client
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        return gspread.authorize(credentials)
    except Exception as e:
        print(f"Error creating Google Sheets client: {e}")
        return None

def is_valid_base64_json(encoded_string: str) -> bool:
    """Validate if the base64-encoded string is a valid JSON."""
    try:
        # Decode the base64 string
        decoded_bytes = base64.b64decode(encoded_string)
        # Convert bytes to string
        decoded_str = decoded_bytes.decode('utf-8')
        # Parse the string as JSON
        json.loads(decoded_str)
        return True
    except (base64.binascii.Error, UnicodeDecodeError, json.JSONDecodeError):
        return False

@router.get("/", response_class=HTMLResponse)
async def google_sheets_interface():
    """Render the Google Sheets interface with form and view button"""
    html_content = """
    <html>
        <head>
            <title>Google Sheets Viewer</title>
            <style>
                .container { max-width: 800px; margin: 0 auto; padding: 20px; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; }
                input[type="text"] { width: 100%; padding: 8px; }
                button { padding: 8px 15px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Google Sheets Viewer</h1>
                <form method="post" action="/googlesheets/view">
                    <div class="form-group">
                        <label for="sheet_url">Google Sheet URL:</label>
                        <input type="text" id="sheet_url" name="sheet_url" required>
                    </div>
                    <button type="submit">View Sheet</button>
                </form>
                <div id="sheet-content"></div>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.post("/view", response_class=HTMLResponse)
async def view_google_sheet(request: Request, sheet_url: str = Form(...)):
    """Fetch and display Google Sheet content"""
    try:
        client = get_google_sheets_client()
        if not client:
            return HTMLResponse(content="<p>Error: Unable to authenticate with Google Sheets</p>")
        
        # Open the sheet by URL
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.get_worksheet(0)  # Get the first worksheet
        
        # Get all values
        data = worksheet.get_all_values()
        
        # Generate HTML table
        table_html = "<table>"
        for i, row in enumerate(data):
            table_html += "<tr>"
            for cell in row:
                if i == 0:
                    table_html += f"<th>{cell}</th>"
                else:
                    table_html += f"<td>{cell}</td>"
            table_html += "</tr>"
        table_html += "</table>"
        
        # Return the form with the table
        return HTMLResponse(content=f"""
            <html>
                <body>
                    <div class="container">
                        <form method="post" action="/googlesheets/view">
                            <div class="form-group">
                                <label for="sheet_url">Google Sheet URL:</label>
                                <input type="text" id="sheet_url" name="sheet_url" value="{sheet_url}" required>
                            </div>
                            <button type="submit">View Sheet</button>
                        </form>
                        {table_html}
                    </div>
                </body>
            </html>
        """)
    except Exception as e:
        return HTMLResponse(content=f"<p>Error: {str(e)}</p>")
