from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_MONGO = os.environ.get('DB_MONGO2')
    RUTA_CLUSTER=os.environ.get('RUTA_CLUSTER')
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    ALGORITHM = os.environ.get('ALGORITHM')
    ORIGINS_MAIN = os.environ.get('ORIGINS_MAIN')

settings = Settings()
