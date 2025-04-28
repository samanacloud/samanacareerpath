from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from database import get_database
from bson import ObjectId
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from config import settings
import random
import string
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

class RegistrationData(BaseModel):
    companyName: str
    email: str
    phoneNumber: str
    adminName: str
    website: str
    employeeRange: str
    country: str
    ipAddress: Optional[str] = None

class VerificationResponse(BaseModel):
    email: str
    message: str

# Add constants for timing
VERIFICATION_CODE_EXPIRY = timedelta(minutes=5)  # Code expires in 5 minutes
RESEND_COOLDOWN = timedelta(minutes=5)  # Must wait 5 minutes before resending

# Add constants for JWT
JWT_SECRET = settings.JWT_SECRET
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is not set")
    
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

# Add after the other constants
security = HTTPBearer()

async def send_verification_email(to_email: str, company_name: str) -> tuple[bool, str, str]:
    """Send verification email and return status, message and verification code"""
    try:
        verification_code = ''.join(random.choices(string.digits, k=6))
        
        login_email = settings.GOOGLE_LOGIN_EMAIL
        sender_email = settings.PROJECT_EMAIL
        sender_name = settings.PROJECT_NAME
        
        msg = MIMEMultipart('alternative')
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = to_email
        msg['Subject'] = f"Welcome to CareerPath - Verify Your Company"
        msg['Reply-To'] = sender_email

        # Create HTML version of the email
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <img src="https://scp.samana.cloud/public/samana-logo.png" alt="CareerPath Logo" style="max-width: 200px;">
            </div>
            
            <div style="background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h1 style="color: #333; font-size: 24px; margin-bottom: 20px; text-align: center;">Welcome to CareerPath!</h1>
                
                <p style="color: #666; font-size: 16px; line-height: 1.5; margin-bottom: 30px;">
                    Thank you for registering {company_name}. To complete your registration, please use the following verification code:
                </p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 30px;">
                    <span style="font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #333;">{verification_code}</span>
                </div>
                
                <p style="color: #666; font-size: 14px; text-align: center; margin-bottom: 20px;">
                    This code will expire in 5 minutes.
                </p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p style="color: #999; font-size: 12px; text-align: center;">
                    If you didn't request this verification, please ignore this email.
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
        
        return True, "Verification email sent successfully", verification_code

    except Exception as e:
        return False, f"Error sending email: {str(e)}", None

async def create_verification_record(registration_data: RegistrationData) -> dict:
    """Create a verification record in MongoDB"""
    db = await get_database()
    
    # Check for existing verification that's too recent
    existing_recent = await db.verifications.find_one({
        "email": registration_data.email,
        "status": "pending",
        "lastAttempt": {
            "$gt": datetime.utcnow() - RESEND_COOLDOWN
        }
    })

    if existing_recent:
        time_remaining = (existing_recent["lastAttempt"] + RESEND_COOLDOWN - datetime.utcnow())
        minutes_remaining = int(time_remaining.total_seconds() / 60)
        seconds_remaining = int(time_remaining.total_seconds() % 60)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "type": "rate_limit",
                "message": f"Please wait {minutes_remaining} minutes and {seconds_remaining} seconds before requesting a new code."
            }
        )

    # Check if company already exists by website or email
    existing_company = await db.companies.find_one({
        "$or": [
            {"website": registration_data.website},
            {"email": registration_data.email}
        ]
    })
    
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "type": "company_exists",
                "message": "This company is already registered. Please proceed to login.",
                "action": "login"  # Add action field for frontend handling
            }
        )

    # Check for existing pending verification from same IP
    existing_verification = await db.verifications.find_one({
        "ipAddress": registration_data.ipAddress,
        "status": "pending",
        "expiresAt": {"$gt": datetime.utcnow()}
    })

    if existing_verification:
        if existing_verification["email"] != registration_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "type": "verification_in_progress",
                    "message": f"A verification is already in progress for IP address {registration_data.ipAddress}. Please complete that verification first or wait for it to expire."
                }
            )

    # Send verification email
    success, message, verification_code = await send_verification_email(
        registration_data.email,
        registration_data.companyName
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification email: {message}"
        )

    current_time = datetime.utcnow()
    verification_record = {
        "companyName": registration_data.companyName,
        "email": registration_data.email,
        "phoneNumber": registration_data.phoneNumber,
        "adminName": registration_data.adminName,
        "website": registration_data.website,
        "employeeRange": registration_data.employeeRange,
        "country": registration_data.country,
        "ipAddress": registration_data.ipAddress,
        "verificationCode": verification_code,
        "status": "pending",
        "createdAt": current_time,
        "updatedAt": current_time,
        "verifiedAt": None,
        "attempts": 0,
        "lastAttempt": current_time,
        "expiresAt": current_time + VERIFICATION_CODE_EXPIRY
    }
    
    # Delete any existing expired verifications for this email
    await db.verifications.delete_many({
        "email": registration_data.email,
        "status": "pending",
        "expiresAt": {"$lt": current_time}
    })
    
    result = await db.verifications.insert_one(verification_record)
    
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create verification record"
        )
    
    return {
        "id": str(result.inserted_id),
        "email": registration_data.email,
        "message": "Verification code sent successfully. Code will expire in 5 minutes."
    }

@router.post("/verify/send", response_model=VerificationResponse)
async def send_verification(registration_data: RegistrationData):
    """Handle company registration verification request"""
    try:
        verification = await create_verification_record(registration_data)
        
        return VerificationResponse(
            email=verification["email"],
            message=verification["message"]
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Add new verification request model
class VerificationRequest(BaseModel):
    email: str
    code: str

@router.post("/verify/code")
async def verify_code(verification: VerificationRequest):
    """Verify company registration with code"""
    db = await get_database()
    
    # First, find the verification record
    verification_record = await db.verifications.find_one({
        "email": verification.email,
        "status": "pending"
    })
    
    if not verification_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "not_found",
                "message": "No pending verification found for this email"
            }
        )

    # Check if code matches and is not expired
    current_time = datetime.utcnow()
    if verification_record["expiresAt"] < current_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "type": "code_expired",
                "message": "Verification code has expired. Please request a new code."
            }
        )

    if verification_record["verificationCode"] != verification.code:
        # Update attempts count
        await db.verifications.update_one(
            {"_id": verification_record["_id"]},
            {
                "$inc": {"attempts": 1},
                "$set": {"lastAttempt": current_time}
            }
        )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "type": "invalid_code",
                "message": "Invalid verification code. Please try again."
            }
        )

    # Code is valid - update verification status
    result = await db.verifications.find_one_and_update(
        {"_id": verification_record["_id"]},
        {
            "$set": {
                "status": "verified",
                "verifiedAt": current_time,
                "updatedAt": current_time
            }
        },
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update verification status"
        )

    try:
        # Create company record
        company_id = await create_company_record(verification_record)
        
        # Create user record
        user_id = await create_user_record(verification_record, company_id)
        
        # Update verification record with company and user IDs
        await db.verifications.update_one(
            {"_id": verification_record["_id"]},
            {
                "$set": {
                    "companyId": company_id,
                    "userId": user_id,
                    "updatedAt": current_time
                }
            }
        )
        
        return {
            "message": "Company verified and created successfully",
            "companyName": verification_record["companyName"],
            "email": verification_record["email"],
            "companyId": company_id,
            "userId": user_id
        }
        
    except Exception as e:
        # Rollback on failure
        if 'company_id' in locals():
            await db.companies.delete_one({"_id": ObjectId(company_id)})
        if 'user_id' in locals():
            await db.users.delete_one({"_id": ObjectId(user_id)})
            
        await db.verifications.update_one(
            {"_id": verification_record["_id"]},
            {
                "$set": {
                    "status": "pending",
                    "updatedAt": current_time
                }
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create company and user: {str(e)}"
        )

@router.post("/verify/resend/{email}")
async def resend_verification(email: str):
    """Resend verification email"""
    db = await get_database()
    
    verification = await db.verifications.find_one({
        "email": email,
        "status": "pending"
    })
    
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pending verification found for this email"
        )
    
    # Send new verification email
    success, message, new_code = await send_verification_email(
        email,
        verification["companyName"]
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification email: {message}"
        )
    
    # Update verification record
    await db.verifications.update_one(
        {"_id": verification["_id"]},
        {
            "$set": {
                "verificationCode": new_code,
                "expiresAt": datetime.utcnow() + timedelta(hours=24),
                "updatedAt": datetime.utcnow(),
                "attempts": verification["attempts"] + 1,
                "lastAttempt": datetime.utcnow()
            }
        }
    )
    
    return {
        "message": "Verification email resent successfully",
        "email": email
    }

# Add company creation function
async def create_company_record(verification_data: dict) -> str:
    """Create a company record in the companies collection"""
    db = await get_database()
    
    company_record = {
        "companyName": verification_data["companyName"],
        "email": verification_data["email"],
        "phoneNumber": verification_data["phoneNumber"],
        "adminName": verification_data["adminName"],
        "website": verification_data["website"],
        "employeeRange": verification_data["employeeRange"],
        "country": verification_data["country"],
        "license": "t0",  # Default license tier
        "status": "active",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
        "verifiedAt": datetime.utcnow()
    }
    
    result = await db.companies.insert_one(company_record)
    
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create company record"
        )
    
    return str(result.inserted_id)

# Add user creation function
async def create_user_record(verification_data: dict, company_id: str) -> str:
    """Create a user record in the users collection"""
    db = await get_database()
    
    user_record = {
        "companyId": company_id,
        "companyName": verification_data["companyName"],
        "name": verification_data["adminName"],
        "email": verification_data["email"],
        "country": verification_data["country"],
        "role": "administrator",
        "phone": verification_data["phoneNumber"],
        "license": "t0",
        "status": "active",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_record)
    
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user record"
        )
    
    return str(result.inserted_id)

# Add new models for login verification
class LoginVerificationRequest(BaseModel):
    email: str
    ipAddress: str

class LoginCodeVerification(BaseModel):
    email: str
    code: str
    ipAddress: str

async def send_login_verification_email(to_email: str, company_name: str) -> tuple[bool, str, str]:
    """Send login verification email and return status, message and verification code"""
    try:
        verification_code = ''.join(random.choices(string.digits, k=6))
        
        login_email = settings.GOOGLE_LOGIN_EMAIL
        sender_email = settings.PROJECT_EMAIL
        sender_name = settings.PROJECT_NAME
        
        msg = MIMEMultipart('alternative')
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = to_email
        msg['Subject'] = f"CareerPath - Login Verification Code"
        msg['Reply-To'] = sender_email

        # Create HTML version of the email
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <img src="https://scp.samana.cloud/public/samana-logo.png" alt="CareerPath Logo" style="max-width: 200px;">
            </div>
            
            <div style="background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h1 style="color: #333; font-size: 24px; margin-bottom: 20px; text-align: center;">Login Verification</h1>
                
                <p style="color: #666; font-size: 16px; line-height: 1.5; margin-bottom: 30px;">
                    A login attempt was made for {company_name}. To verify your identity and proceed with the login, please use the following code:
                </p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 30px;">
                    <span style="font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #333;">{verification_code}</span>
                </div>
                
                <p style="color: #666; font-size: 14px; text-align: center; margin-bottom: 20px;">
                    This code will expire in 5 minutes. If you didn't attempt to log in, please ignore this email and consider changing your password.
                </p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p style="color: #999; font-size: 12px; text-align: center;">
                    For security reasons, never share this code with anyone.
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
        
        return True, "Login verification email sent successfully", verification_code

    except Exception as e:
        return False, f"Error sending email: {str(e)}", None

@router.post("/email/send")
async def send_login_verification(verification: LoginVerificationRequest):
    """Send verification code for login"""
    db = await get_database()
    
    # Check for existing recent verification
    existing_recent = await db.login_verifications.find_one({
        "email": verification.email,
        "ipAddress": verification.ipAddress,
        "status": "pending",
        "lastAttempt": {
            "$gt": datetime.utcnow() - RESEND_COOLDOWN
        }
    })

    if existing_recent:
        time_remaining = (existing_recent["lastAttempt"] + RESEND_COOLDOWN - datetime.utcnow())
        minutes_remaining = int(time_remaining.total_seconds() / 60)
        seconds_remaining = int(time_remaining.total_seconds() % 60)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "type": "rate_limit",
                "message": f"Please wait {minutes_remaining} minutes and {seconds_remaining} seconds before requesting a new code."
            }
        )

    # Check if user exists
    user = await db.users.find_one({"email": verification.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "user_not_found",
                "message": "No account found with this email address."
            }
        )

    # Send verification email
    success, message, verification_code = await send_login_verification_email(
        verification.email,
        user["companyName"]
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification email: {message}"
        )

    current_time = datetime.utcnow()
    verification_record = {
        "email": verification.email,
        "ipAddress": verification.ipAddress,
        "verificationCode": verification_code,
        "status": "pending",
        "createdAt": current_time,
        "updatedAt": current_time,
        "verifiedAt": None,
        "attempts": 0,
        "lastAttempt": current_time,
        "expiresAt": current_time + VERIFICATION_CODE_EXPIRY
    }
    
    # Delete any existing expired verifications
    await db.login_verifications.delete_many({
        "email": verification.email,
        "status": "pending",
        "expiresAt": {"$lt": current_time}
    })
    
    result = await db.login_verifications.insert_one(verification_record)
    
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create verification record"
        )
    
    return {
        "message": "Verification code sent successfully. Code will expire in 5 minutes."
    }

def create_session_token(user_data: dict) -> str:
    """Create session token with user data"""
    # Convert JWT_SECRET to bytes if it's not already
    secret_key = JWT_SECRET.encode() if isinstance(JWT_SECRET, str) else JWT_SECRET
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "companyName": user_data["companyName"],
        "userName": user_data["userName"],
        "email": user_data["email"],
        "companyId": user_data["companyId"],
        "role": user_data.get("role", "user"),  # Include role with default
        "ipAddress": user_data.get("ipAddress"),
        "exp": expire
    }
    
    return jwt.encode(to_encode, secret_key, algorithm=JWT_ALGORITHM)

@router.post("/email/code")
async def verify_login_code(verification: LoginCodeVerification):
    """Verify login verification code"""
    db = await get_database()
    
    # Find verification record
    verification_record = await db.login_verifications.find_one({
        "email": verification.email,
        "ipAddress": verification.ipAddress,  # Must match the IP that requested the code
        "status": "pending"
    })
    
    if not verification_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "not_found",
                "message": "No pending verification found for this email and IP address"
            }
        )

    # Check expiration
    current_time = datetime.utcnow()
    if verification_record["expiresAt"] < current_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "type": "code_expired",
                "message": "Verification code has expired. Please request a new code."
            }
        )

    # Verify code
    if verification_record["verificationCode"] != verification.code:
        # Update attempts count
        await db.login_verifications.update_one(
            {"_id": verification_record["_id"]},
            {
                "$inc": {"attempts": 1},
                "$set": {"lastAttempt": current_time}
            }
        )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "type": "invalid_code",
                "message": "Invalid verification code. Please try again."
            }
        )

    # Get user data
    user = await db.users.find_one({
        "email": verification.email
    })
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create session token
    session_token = create_session_token({
        "companyName": user["companyName"],
        "userName": user["name"],
        "email": user["email"],
        "companyId": user["companyId"],
        "role": user["role"],  # Include role in token
        "ipAddress": verification.ipAddress
    })

    # Calculate expiration time for client reference
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Update verification status
    result = await db.login_verifications.find_one_and_update(
        {"_id": verification_record["_id"]},
        {
            "$set": {
                "status": "verified",
                "verifiedAt": current_time,
                "updatedAt": current_time
            }
        },
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update verification status"
        )
    
    # Create response with cookie
    response = JSONResponse(
        content={
            "message": "Email verified successfully",
            "email": verification.email,
            "expiresAt": expire_time.isoformat(),
            "session_token": session_token  # Still including token in response for compatibility
        }
    )
    
    # Set secure cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,  # Prevents JavaScript access
        secure=True,    # Only sent over HTTPS
        samesite="lax", # Protects against CSRF
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert minutes to seconds
        path="/"        # Cookie available for all paths
    )
    
    return response

async def verify_session_token(
    session_token: Optional[str] = Cookie(None, alias="session_token")
) -> dict:
    """
    Verify session token from cookie and return user data if valid.
    Can be used as a FastAPI dependency.
    """
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "type": "unauthorized",
                "message": "No session token provided"
            }
        )
    
    try:
        # Decode and verify the JWT token
        payload = jwt.decode(
            session_token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
        
        # Check if token has required fields
        required_fields = ["email", "companyId", "companyName", "userName"]
        if not all(field in payload for field in required_fields):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "type": "invalid_token",
                    "message": "Invalid session token format"
                }
            )
        
        # Verify user still exists in database
        db = await get_database()
        user = await db.users.find_one({
            "email": payload["email"],
            "companyId": payload["companyId"],
            "status": "active"  # Only allow active users
        })
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "type": "user_not_found",
                    "message": "User no longer exists or is inactive"
                }
            )
        
        return {
            "email": payload["email"],
            "companyId": payload["companyId"],
            "companyName": payload["companyName"],
            "userName": payload["userName"],
            "role": user["role"],  # Include user role from database
            "userId": str(user["_id"])
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "type": "invalid_token",
                "message": "Invalid or expired session token"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "type": "verification_error",
                "message": f"Error verifying session: {str(e)}"
            }
        )

@router.get("/verify/session")
async def verify_session(user_data: dict = Depends(verify_session_token), session_token: Optional[str] = Cookie(None, alias="session_token")):
    """
    Verify if the current session is valid.
    Returns user data if session is valid.
    """
    # Calculate remaining time in the session
    try:
        if session_token:
            # Decode without verification first to extract expiration
            # This is safer in case there are any issues with the signature
            try:
                # First try to decode with verification
                payload = jwt.decode(
                    session_token,
                    JWT_SECRET,
                    algorithms=[JWT_ALGORITHM],
                    options={"verify_signature": True}
                )
            except Exception as e:
                print(f"Error verifying token signature: {str(e)}")
                # If verification fails, try without verification just to extract exp
                payload = jwt.decode(
                    session_token,
                    algorithms=[JWT_ALGORITHM],
                    options={"verify_signature": False}
                )
            
            # Get expiration time from token
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                expires_at = datetime.fromtimestamp(exp_timestamp)
                # Include expiration time in response
                return {
                    "message": "Session is valid",
                    "user": user_data,
                    "expiresAt": expires_at.isoformat()
                }
    except Exception as e:
        print(f"Error extracting expiration time: {str(e)}")
    
    # If we couldn't extract expiration from token, calculate it based on ACCESS_TOKEN_EXPIRE_MINUTES
    # This is a fallback to ensure we always return an expiration time
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "message": "Session is valid",
        "user": user_data,
        "expiresAt": expire_time.isoformat()  # Always include an expiration time
    }

@router.post("/renew-session")
async def renew_session(user_data: dict = Depends(verify_session_token)):
    """
    Renew the user's session by creating a new token with extended expiration time.
    """
    try:
        # Create a new session token with fresh expiration
        new_session_token = create_session_token({
            "companyName": user_data["companyName"],
            "userName": user_data["userName"],
            "email": user_data["email"],
            "companyId": user_data["companyId"],
            "ipAddress": None,  # We don't have IP in the dependency
            "role": user_data["role"]  # Include role in the token
        })
        
        # Calculate expiration time for client reference
        expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Create response with the new token
        response = JSONResponse(
            content={
                "message": "Session renewed successfully",
                "expiresAt": expire_time.isoformat(),
                "expiresIn": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # in seconds
            }
        )
        
        # Set secure cookie with new token
        response.set_cookie(
            key="session_token",
            value=new_session_token,
            httponly=True,  # Prevents JavaScript access
            secure=True,    # Only sent over HTTPS
            samesite="lax", # Protects against CSRF
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert minutes to seconds
            path="/"        # Cookie available for all paths
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error renewing session: {str(e)}"
        )