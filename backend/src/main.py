from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI(title="Hello World API")

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

    