"""
Authentication Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt

from app.db.database import get_db
from app.db.models import User
from app.core.config import settings
from app.middleware.security import sanitize_input, validate_email, validate_password_strength

router = APIRouter()

# Password hashing using bcrypt
def hash_password(password: str) -> str:
    """
    Hash password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    # Use bcrypt directly without truncation
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)  # Higher cost factor for security
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    password_bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


class UserCreate(BaseModel):
    """User registration model with validation"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    
    @validator('email')
    def validate_email(cls, v):
        """Validate email format"""
        if not validate_email(v):
            raise ValueError('Invalid email format')
        return v.lower().strip()
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        is_valid, error_msg = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v
    
    @validator('full_name')
    def validate_full_name(cls, v):
        """Sanitize full name"""
        if v:
            return sanitize_input(v, max_length=100)
        return v


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    Args:
        user: User registration data
        db: Database session
        
    Returns:
        Created user
    """
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user - hash password with bcrypt
    hashed_password = hash_password(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Verify password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user



# Gmail OAuth endpoints
@router.get("/gmail/authorize")
async def gmail_authorize():
    """Get Gmail authorization URL"""
    from app.services.gmail_service import GmailService  # Lazy import
    try:
        auth_url = GmailService.get_authorization_url()
        return {"authorization_url": auth_url}
    except Exception as e:
        # Provide a helpful error to the frontend during development
        raise HTTPException(status_code=500, detail=f"Could not build Gmail authorization URL: {str(e)}")

@router.get("/gmail/callback")
async def gmail_callback(
    code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Handle Gmail OAuth callback"""
    from app.services.gmail_service import GmailService  # Lazy import
    try:
        token_data = GmailService.exchange_code_for_token(code)
        # Save tokens to user
        current_user.gmail_access_token = token_data['access_token']
        current_user.gmail_refresh_token = token_data['refresh_token']
        if token_data['expiry']:
            current_user.gmail_token_expiry = datetime.fromisoformat(token_data['expiry'])
        db.commit()
        return {"message": "Gmail connected successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

