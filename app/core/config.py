
from typing import Optional
import os
from dotenv import load_dotenv

from pydantic import BaseSettings, EmailStr


load_dotenv()


class Settings(BaseSettings):
    title: str = os.getenv('TITLE')
    description: str = os.getenv('DESCRIPTION')
    database: str = os.getenv('DATABASE')
    secret: str = os.getenv('SECRET')
    first_superuser_email: Optional[EmailStr] = os.getenv('FIRST_SUPERUSER_EMAIL', default=None)
    first_superuser_password: Optional[str] = os.getenv('FIRST_SUPERUSER_PASSWORD', default=None)


settings = Settings()