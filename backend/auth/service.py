from fastapi import HTTPException

from auth.schemas import SignupRequest
from auth.utils import hash_password

from auth.schemas import LoginRequest
from auth.utils import verify_password, create_access_token

from db.user_crud import (
    create_user,
    get_user_by_email,
    get_user_by_username
)


def signup(request: SignupRequest):

    # -----------------------------
    # Check Username
    # -----------------------------
    existing_user = get_user_by_username(request.username)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username already exists."
        )

    # -----------------------------
    # Check Email
    # -----------------------------
    existing_email = get_user_by_email(request.email)

    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="Email already registered."
        )

    # -----------------------------
    # Hash Password
    # -----------------------------
    hashed_password = hash_password(request.password)

    # -----------------------------
    # Create User
    # -----------------------------
    user = create_user(
        username=request.username,
        email=request.email,
        password_hash=hashed_password
    )

    return {
        "message": "User registered successfully.",
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }


def login(request: LoginRequest):

    # Find user by email
    user = get_user_by_email(request.email)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    # Create JWT token
    token = create_access_token(
        {
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }