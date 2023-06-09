from pymongo import MongoClient
from core.config.config import settings

client = MongoClient(settings.RUTA_CLUSTER)

db = settings.DB_MONGO
coleccion_colegio = client[f'{db}'].colegios
coleccion_accion = client[f'{db}'].acciones
coleccion_actividades = client[f'{db}'].actividades
coleccion_pme = client[f'{db}'].pme
coleccion_presupuesto_colegio = client[f'{db}'].presupuesto_colegio
coleccion_presupuesto = client[f'{db}'].presupuesto
coleccion_recursos = client[f'{db}'].recursos
coleccion_user = client[f'{db}'].user
colecion_requerimiento = client[f'{db}'].requerimiento