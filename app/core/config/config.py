from pathlib import Path
from dotenv import load_dotenv
from os import environ

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    RUTA_MONGO=environ.get('RUTA_MONGO')

settings = Settings()