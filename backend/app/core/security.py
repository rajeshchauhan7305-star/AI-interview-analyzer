from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Use pbkdf2_sha256 to avoid bcrypt's 72-byte password limit in this environment
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt limits passwords to 72 bytes; ensure we verify against the same truncated input
    pw = plain_password
    try:
        pw_bytes = pw.encode("utf-8")
    except Exception:
        pw_bytes = str(pw).encode("utf-8", errors="ignore")
    if len(pw_bytes) > 72:
        pw = pw_bytes[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(pw, hashed_password)


def get_password_hash(password: str) -> str:
    # bcrypt has a 72-byte input limit; truncate to bytes to avoid ValueError
    pw = password
    try:
        pw_bytes = pw.encode("utf-8")
    except Exception:
        pw_bytes = str(pw).encode("utf-8", errors="ignore")
    if len(pw_bytes) > 72:
        pw = pw_bytes[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(pw)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return {}


def verify_refresh_token(token: str) -> dict:
    payload = decode_token(token)
    if payload and payload.get("type") == "refresh":
        return payload
    return {}
