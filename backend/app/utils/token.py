from itsdangerous import URLSafeTimedSerializer
from app.core.config import settings

serializer = URLSafeTimedSerializer(settings.JWT_SECRET_KEY)


def create_email_token(email: str) -> str:
    return serializer.dumps(email, salt="email-confirm")


def verify_email_token(token: str, max_age: int = 3600) -> str | None:
    try:
        return serializer.loads(token, salt="email-confirm", max_age=max_age)
    except Exception:
        return None


def create_password_reset_token(email: str) -> str:
    return serializer.dumps(email, salt="password-reset")


def verify_password_reset_token(token: str, max_age: int = 3600) -> str | None:
    try:
        return serializer.loads(token, salt="password-reset", max_age=max_age)
    except Exception:
        return None
