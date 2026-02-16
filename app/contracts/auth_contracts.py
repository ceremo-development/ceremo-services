"""Authentication contracts."""

from pydantic import BaseModel, EmailStr


class SignInRequest(BaseModel):
    """Sign in request schema."""

    email: EmailStr
    password: str
    rememberMe: bool = False


class SignUpRequest(BaseModel):
    """Sign up request schema."""

    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    password: str
    confirmPassword: str
    agreeToTerms: bool


class UserData(BaseModel):
    """User data schema."""

    id: str
    email: str
    firstName: str
    lastName: str
    phone: str


class AuthData(BaseModel):
    """Auth response data schema."""

    user: UserData
    token: str
    refreshToken: str


class AuthResponse(BaseModel):
    """Auth response schema."""

    success: bool = True
    data: AuthData
    message: str


class SignOutResponse(BaseModel):
    """Sign out response schema."""

    success: bool = True
    message: str
