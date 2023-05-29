from core.schemas.Schema_presupuesto import Schema_Presupuesto
from core.config.db import coleccion_presupuesto_colegio



def insertar_presupuesto(listado_presupuesto: dict):
    try:
        coleccion_presupuesto_colegio.insert_many(listado_presupuesto)
        return True
    except Exception as e:
        print(e)


def listar_presupuesto(id:str):
    try:
        data = [x for x in coleccion_presupuesto_colegio.find({'id_presupuesto':id})]
        return data
    except Exception as e:
        print(e)
