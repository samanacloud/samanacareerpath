from fastapi import HTTPException, Security, Depends, APIRouter, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from google.oauth2 import id_token
from google.auth.transport import requests
import httpx
from database import get_database

router = APIRouter()
security = HTTPBearer()

# Get JWT and Google OAuth settings from environment
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Match verification.py expiry time
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("exp") < datetime.utcnow().timestamp():
            raise HTTPException(status_code=401, detail="Token has expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/google")
async def google_auth(token: str):
    try:
        # Verify the Google ID token
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            GOOGLE_CLIENT_ID
        )

        # Check if the token is issued by Google
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise HTTPException(status_code=401, detail="Invalid issuer")

        # Extract user information
        user_data = {
            "email": idinfo['email'],
            "name": idinfo['name'],
            "picture": idinfo.get('picture'),
            "given_name": idinfo.get('given_name'),
            "family_name": idinfo.get('family_name'),
        }

        # Create JWT token for our application
        access_token = create_access_token(user_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_redirect_uri(request: Request) -> str:
    """Construct redirect URI using PROJECT_URL environment variable"""
    project_url = os.getenv('PROJECT_URL', 'scp.samana.cloud')
    return f"https://{project_url}/core/auth/google/callback"

@router.post("/google/url")
async def get_google_auth_url(request: Request):
    """Generate Google OAuth2 authorization URL"""
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": get_redirect_uri(request),
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    
    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    auth_url = f"{base_url}?{query_string}"
    
    return {"url": auth_url}

def create_session_token(user_data: dict) -> str:
    """Create session token with user data - matching verification.py format"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "companyName": user_data["companyName"],
        "userName": user_data["userName"],
        "email": user_data["email"],
        "companyId": user_data["companyId"],
        "exp": expire
    }
    
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

@router.get("/google/callback")
async def google_auth_callback(request: Request, code: str):
    """Handle Google OAuth2 callback"""
    try:
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "redirect_uri": get_redirect_uri(request),
            "grant_type": "authorization_code",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=token_data)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get token from Google")
            
            tokens = response.json()
            id_token_jwt = tokens["id_token"]
            
            # Verify the Google ID token
            idinfo = id_token.verify_oauth2_token(
                id_token_jwt,
                requests.Request(),
                GOOGLE_CLIENT_ID
            )

            # Get user from database
            db = await get_database()
            user = await db.users.find_one({"email": idinfo['email']})
            
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found. Please register first."
                )

            # Create session token with user data
            session_token = create_session_token({
                "companyName": user["companyName"],
                "userName": user["name"],
                "email": user["email"],
                "companyId": user["companyId"]
            })

            # Create HTML response that sets the cookie and redirects
            html_content = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Authentication Successful</title>
                </head>
                <body>
                    <script>
                        // Store the session token
                        localStorage.setItem('session_token', '{session_token}');
                        
                        // Show success message and redirect to home
                        const message = 'Authentication successful';
                        window.location.href = '/?success=true&message=' + encodeURIComponent(message);
                    </script>
                </body>
            </html>
            """
            
            # Create response with both HTML and cookie
            response = HTMLResponse(content=html_content)
            
            # Set secure cookie
            response.set_cookie(
                key="session_token",
                value=session_token,
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=3600,
                path="/"
            )
            
            return response

    except Exception as e:
        # Create error HTML response that redirects to login on error
        error_html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Authentication Failed</title>
            </head>
            <body>
                <script>
                    window.location.href = '/auth/login?error=true&message={str(e)}';
                </script>
            </body>
        </html>
        """
        return HTMLResponse(content=error_html)

@router.post("/logout")
async def logout():
    """Handle user logout by clearing session cookie"""
    response = JSONResponse(content={
        "message": "Logged out successfully"
    })
    
    # Delete the session cookie by setting its expiry to the past
    response.delete_cookie(
        key="session_token",
        path="/",
        secure=True,
        httponly=True,
        samesite="lax"
    )
    
    return response 