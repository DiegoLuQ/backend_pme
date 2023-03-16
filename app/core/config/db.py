from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.RUTA_MONGO)

db = client.db_colegio