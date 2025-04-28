from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from config import settings
from security.verification import router as verification_router, send_verification, RegistrationData
import strawberry
from strawberry.fastapi import GraphQLRouter
from gql.queries import Query
from gql.mutations import Mutation
from security import auth  # Import the auth module
from security.graphql_auth import verify_graphql_auth
from modules.ai.aitest import router as ai_test_router
from utils.googlesheets import router as googlesheets_router
from contact.contact import router as contact_router
from pydantic import BaseModel
from database import get_database
from datetime import datetime

app = FastAPI(title="Hello World API")

# Set up templates with absolute path
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Create GraphQL Schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)

# Create GraphQL Router
graphql_app = GraphQLRouter(schema)

# Add GraphQL endpoint with middleware
app.include_router(graphql_app, prefix="/graphql")
app.middleware("http")(verify_graphql_auth)

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the verification router without the /core prefix
app.include_router(verification_router)

# Include the auth router
app.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Include the AI test router
app.include_router(ai_test_router, prefix="/api/ai")

# Include the Google Sheets router
app.include_router(googlesheets_router)

# Include the contact router
app.include_router(contact_router)

class CodeRequest(BaseModel):
    code: str

@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    try:
        return templates.TemplateResponse("code_share.html", {"request": request})
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        raise

@app.post("/test/save")
async def save_code(code_request: CodeRequest):
    try:
        print("Attempting to save code...")
        print(f"Code length: {len(code_request.code)}")
        
        db = await get_database()
        print("Database connection established")
        
        # Update or insert the code in the temporal collection
        update_result = await db.temporal.update_one(
            {"_id": "shared_code"},
            {
                "$set": {
                    "code": code_request.code,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        print(f"Update result: {update_result.modified_count} modified, {update_result.upserted_id} upserted")
        return {"message": "Code saved successfully"}
    except Exception as e:
        print(f"Error saving code: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return {"error": f"Failed to save code: {str(e)}"}, 500

@app.get("/test/load")
async def load_code():
    try:
        print("Attempting to load code...")
        db = await get_database()
        print("Database connection established")
        
        # Get the latest code from the temporal collection
        result = await db.temporal.find_one({"_id": "shared_code"})
        print(f"Query result: {result}")
        return {"code": result.get("code", "") if result else ""}
    except Exception as e:
        print(f"Error loading code: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return {"error": f"Failed to load code: {str(e)}"}, 500

@app.post("/test/clear")
async def clear_code():
    try:
        print("Attempting to clear code...")
        db = await get_database()
        print("Database connection established")
        
        # Clear the code from the temporal collection
        delete_result = await db.temporal.delete_one({"_id": "shared_code"})
        print(f"Delete result: {delete_result.deleted_count} documents deleted")
        return {"message": "Code cleared successfully"}
    except Exception as e:
        print(f"Error clearing code: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return {"error": f"Failed to clear code: {str(e)}"}, 500

async def send_test_email(to_email: str, subject: str, body: str) -> tuple[bool, str]:
    try:
        login_email = settings.GOOGLE_LOGIN_EMAIL  # From env
        sender_email = settings.PROJECT_EMAIL      # From env
        sender_name = settings.PROJECT_NAME        # From env
        
        # Debug: Print email settings
        print(f"Logging in with: {login_email}")
        print(f"Sending from: {formataddr((sender_name, sender_email))}")
        print(f"Sending to: {to_email}")
        
        msg = MIMEMultipart()
        msg['From'] = formataddr((sender_name, sender_email))  # Format with display name
        msg['To'] = to_email
        msg['Subject'] = subject
        msg['Reply-To'] = sender_email  # Add reply-to header
        
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(login_email, settings.EMAIL_APP_PASSWORD)  # Login with main email
        
        server.send_message(msg)
        server.quit()
        
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

@app.post("/test-email")
async def test_email():
    return await send_test_email(
        to_email="otalvaroj@gmail.com",
        subject="Test Email from CareerPath",
        body="This is a test email from the CareerPath Team."
    )

@app.post("/auth/verify/send")
async def verify_registration(registration_data: RegistrationData):
    """Handle company registration verification"""
    return await send_verification(registration_data)

    