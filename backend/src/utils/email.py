import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from config import settings

def generate_verification_code(length: int = 6) -> str:
    """Generate a random verification code"""
    return ''.join(random.choices(string.digits, k=length))

async def send_verification_email(to_email: str, company_name: str) -> tuple[bool, str, str]:
    """
    Send verification email and return status, message and the verification code
    """
    try:
        # Generate verification code
        verification_code = generate_verification_code()
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = settings.PROJECT_EMAIL
        msg['To'] = to_email
        msg['Subject'] = f"Verify your company: {company_name}"
        
        body = f"""
        Welcome to CareerPath!
        
        Your verification code for {company_name} is: {verification_code}
        
        Please enter this code to complete your company registration.
        
        Best regards,
        CareerPath Team
        """
        
        msg.attach(MIMEText(body, 'plain'))

        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login with app password
        server.login(settings.PROJECT_EMAIL, settings.EMAIL_APP_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return True, "Verification email sent successfully", verification_code

    except Exception as e:
        return False, f"Error sending email: {str(e)}", None 