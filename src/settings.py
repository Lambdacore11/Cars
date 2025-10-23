import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL:str = os.getenv('DATABASE_URL')
    model_config = ConfigDict(extra='ignore')

settings = Settings()