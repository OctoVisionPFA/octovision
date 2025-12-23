from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId
from jose import JWTError

from models import UserRegister, UserResponse, TokenResponse
from db import connect_db, close_db
import db as db_module
from security import hash_password, verify_password, create_access_token, decode_access_token

app = FastAPI(
    title="OctoVision Auth API",
    description="User authentication with JWT and role-based access control",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@app.on_event("startup")
async def startup():
    await connect_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db()


@app.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserRegister):
    """Register a new user with email and password."""
    existing_user = await db_module.db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(user_data.password)
    user_doc = {
        "email": user_data.email,
        "hashed_password": hashed_password,
        "role": user_data.role
    }
    
    result = await db_module.db.users.insert_one(user_doc)
    return UserResponse(
        id=str(result.inserted_id),
        email=user_data.email,
        role=user_data.role
    )


@app.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token."""
    user = await db_module.db.users.find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user.get("hashed_password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={
            "sub": str(user["_id"]),
            "email": user["email"],
            "role": user.get("role", "user")
        }
    )
    return TokenResponse(access_token=access_token)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to extract and validate current user from JWT token."""
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    try:
        oid = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token"
        )
    
    user = await db_module.db.users.find_one({"_id": oid})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "role": user.get("role", "user")
    }


async def admin_required(current_user: dict = Depends(get_current_user)):
    """Dependency to enforce admin role."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


@app.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return UserResponse(**current_user)


@app.get("/admin-only")
async def admin_only_route(current_user: dict = Depends(admin_required)):
    """Example admin-only endpoint."""
    return {
        "message": "This is an admin-only route",
        "user": current_user
    }
