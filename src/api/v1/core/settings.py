from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from src.api.v1.database import init_db

BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" /  "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expires_minutes: int = 60 * 60 * 24 * 365