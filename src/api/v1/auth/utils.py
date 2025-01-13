from datetime import datetime, timedelta

import bcrypt
import jwt

from src.api.v1.core.settings import AuthJWT

AuthJWT = AuthJWT()

def encode_jwt(
        payload: dict,
        private_key: str = AuthJWT.private_key_path.read_text(),
        algorithm: str = AuthJWT.algorithm,
        expire_minutes: int = AuthJWT.access_token_expires_minutes,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token : str | bytes,
        public_key: str = AuthJWT.public_key_path.read_text(),
        algorithm: str = AuthJWT.algorithm,
):
    decode = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decode



def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
