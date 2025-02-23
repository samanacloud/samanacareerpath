from fastapi import Request
from fastapi.responses import JSONResponse

async def verify_graphql_auth(request: Request, call_next):
    """Middleware to verify session token exists for GraphQL endpoint"""
    
    # Only check auth for GraphQL endpoint
    if not request.url.path.endswith('/graphql'):
        return await call_next(request)
        
    # Get session token from cookie
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"}
        )
            
    # Token exists, proceed with the request
    return await call_next(request)