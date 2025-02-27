from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from config import settings
from database import get_database

router = APIRouter(
    prefix="/contact",
    tags=["contact"]
)

class ContactRequest(BaseModel):
    first_name: str
    last_name: str
    company: str
    email: str  # Changed from EmailStr to str to avoid the dependency
    message: str

async def send_admin_notification_email(contact_data: ContactRequest) -> tuple[bool, str]:
    """Send notification email to admin about new contact form submission"""
    try:
        login_email = settings.GOOGLE_LOGIN_EMAIL
        sender_email = settings.PROJECT_EMAIL
        sender_name = settings.PROJECT_NAME
        admin_email = "juan.otalvaro@samanagroup.co"  # Admin email address
        
        msg = MIMEMultipart('alternative')
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = admin_email
        msg['Subject'] = f"New Contact Form Submission from {contact_data.first_name} {contact_data.last_name}"
        msg['Reply-To'] = contact_data.email

        # Create HTML version of the email
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <img src="https://scp.samana.cloud/public/samana-logo.png" alt="CareerPath Logo" style="max-width: 200px;">
            </div>
            
            <div style="background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h1 style="color: #333; font-size: 24px; margin-bottom: 20px; text-align: center;">New Contact Form Submission</h1>
                
                <div style="margin-bottom: 20px;">
                    <p style="color: #666; font-size: 16px; margin-bottom: 5px;"><strong>Name:</strong> {contact_data.first_name} {contact_data.last_name}</p>
                    <p style="color: #666; font-size: 16px; margin-bottom: 5px;"><strong>Company:</strong> {contact_data.company}</p>
                    <p style="color: #666; font-size: 16px; margin-bottom: 5px;"><strong>Email:</strong> {contact_data.email}</p>
                </div>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <p style="color: #666; font-size: 16px; line-height: 1.5; margin: 0;"><strong>Message:</strong></p>
                    <p style="color: #666; font-size: 16px; line-height: 1.5; margin-top: 10px;">{contact_data.message}</p>
                </div>
                
                <p style="color: #666; font-size: 14px; text-align: center; margin-bottom: 0;">
                    This message was sent from the CareerPath contact form at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC.
                </p>
            </div>
            
            <div style="text-align: center; margin-top: 20px; color: #999; font-size: 12px;">
                © {datetime.utcnow().year} CareerPath by Samana Group. All rights reserved.
            </div>
        </div>
        """
        
        msg.attach(MIMEText(html, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(login_email, settings.EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, "Admin notification email sent successfully"

    except Exception as e:
        return False, f"Error sending admin notification email: {str(e)}"

async def send_confirmation_email(contact_data: ContactRequest) -> tuple[bool, str]:
    """Send confirmation email to the person who submitted the contact form"""
    try:
        login_email = settings.GOOGLE_LOGIN_EMAIL
        sender_email = settings.PROJECT_EMAIL
        sender_name = settings.PROJECT_NAME
        
        msg = MIMEMultipart('alternative')
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = contact_data.email
        msg['Subject'] = "Thank you for contacting CareerPath"
        msg['Reply-To'] = sender_email

        # Create HTML version of the email
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <img src="https://scp.samana.cloud/public/samana-logo.png" alt="CareerPath Logo" style="max-width: 200px;">
            </div>
            
            <div style="background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h1 style="color: #333; font-size: 24px; margin-bottom: 20px; text-align: center;">Thank You for Contacting Us!</h1>
                
                <p style="color: #666; font-size: 16px; line-height: 1.5; margin-bottom: 20px;">
                    Dear {contact_data.first_name},
                </p>
                
                <p style="color: #666; font-size: 16px; line-height: 1.5; margin-bottom: 20px;">
                    Thank you for reaching out to CareerPath. We have received your message and will get back to you as soon as possible.
                </p>
                
                <p style="color: #666; font-size: 16px; line-height: 1.5; margin-bottom: 20px;">
                    For your reference, here's a copy of your message:
                </p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <p style="color: #666; font-size: 16px; line-height: 1.5; margin: 0;">{contact_data.message}</p>
                </div>
                
                <p style="color: #666; font-size: 16px; line-height: 1.5; margin-bottom: 20px;">
                    If you have any additional questions or information to provide, please don't hesitate to reply to this email.
                </p>
                
                <p style="color: #666; font-size: 16px; line-height: 1.5; margin-bottom: 0;">
                    Best regards,<br>
                    The CareerPath Team
                </p>
            </div>
            
            <div style="text-align: center; margin-top: 20px; color: #999; font-size: 12px;">
                © {datetime.utcnow().year} CareerPath by Samana Group. All rights reserved.
            </div>
        </div>
        """
        
        msg.attach(MIMEText(html, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(login_email, settings.EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, "Confirmation email sent successfully"

    except Exception as e:
        return False, f"Error sending confirmation email: {str(e)}"

@router.post("/send")
async def send_contact_form(contact_data: ContactRequest):
    """Handle contact form submission"""
    try:
        # Store contact form submission in database
        db = await get_database()
        
        contact_record = {
            "firstName": contact_data.first_name,
            "lastName": contact_data.last_name,
            "company": contact_data.company,
            "email": contact_data.email,
            "message": contact_data.message,
            "createdAt": datetime.utcnow(),
            "status": "new"
        }
        
        result = await db.contact_submissions.insert_one(contact_record)
        
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store contact form submission"
            )
        
        # Send notification email to admin
        admin_email_success, admin_email_message = await send_admin_notification_email(contact_data)
        
        # Send confirmation email to user
        user_email_success, user_email_message = await send_confirmation_email(contact_data)
        
        if not admin_email_success:
            print(f"Warning: Failed to send admin notification email: {admin_email_message}")
        
        if not user_email_success:
            print(f"Warning: Failed to send user confirmation email: {user_email_message}")
        
        return {
            "message": "Contact form submitted successfully",
            "id": str(result.inserted_id)
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 