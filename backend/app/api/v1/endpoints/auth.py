from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.security import create_access_token
from app.core.config import settings
from app.services.auth_service import AuthService

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    Rate limited to 5 requests per minute per IP address.
    """
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/register")
@limiter.limit("3/minute")
async def register(
    request: Request,
    user_data: dict,
    auth_service: AuthService = Depends()
):
    """
    Register a new user.
    Rate limited to 3 requests per minute per IP address.
    """
    try:
        user = await auth_service.create_user(user_data)
        return {"message": "User created successfully", "user_id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") 