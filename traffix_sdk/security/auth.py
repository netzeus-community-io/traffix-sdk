from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

from traffix_sdk.config import settings


def get_pwd_context() -> CryptContext:
    """Returns a Password Context."""
    ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return ctx

def get_password_hash(password: str, ctx: CryptContext = get_pwd_context()) -> str:
    """Hashes a password based on a given password context.
    
    Args:
        password:       Password string
        ctx:            CryptContext Object to use when hasing password
    """
    hashed_password = ctx.hash(password)
    return hashed_password

def verify_password(
    password: str, hashed_password: str, ctx: CryptContext = get_pwd_context()
) -> bool:
    """Verifies if a given password can be hashed and compared to an existing hashed password.
    
    Args:
        password:           Plain text password
        hashed_password:    Hashed Password to compare
        ctx:                CryptContext Object to use when verifying password     
    """
    verified_password = ctx.verify(password, hashed_password)
    return verified_password

def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    """Creates a JSON Web Token (JWT) with a specific expiration time

    Args:
        subject:        Typically the user id
        expires_delta:  timedelta object to overide default expiration timer
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings.ACCESS_TOKEN_EXPIRE)

    payload = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        claims=payload,
        key=settings.JWT_SHARED_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """Decodes a Token

    Args:
        token:      Token string
    """
    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT_SHARED_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as err:
        return None
    except Exception as err:
        return None

    return payload