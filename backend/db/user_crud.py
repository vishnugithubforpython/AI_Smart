from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models import User


# ----------------------------------------
# Create User
# ----------------------------------------

def create_user(
    username: str,
    email: str,
    password_hash: str,
    role: str = "USER"
):

    db: Session = SessionLocal()

    try:

        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()


# ----------------------------------------
# Get User By Email
# ----------------------------------------

def get_user_by_email(email: str):

    db: Session = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    finally:
        db.close()


# ----------------------------------------
# Get User By Username
# ----------------------------------------

def get_user_by_username(username: str):

    db: Session = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

    finally:
        db.close()


# ----------------------------------------
# Get User By ID
# ----------------------------------------

def get_user_by_id(user_id: int):

    db: Session = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    finally:
        db.close()