from fastapi import APIRouter

from auth.schemas import SignupRequest
from auth.service import signup
from auth.schemas import LoginRequest
from auth.service import login

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup")
def signup_user(request: SignupRequest):

    return signup(request)

@router.post("/login")
def login_user(request: LoginRequest):

    return login(request)