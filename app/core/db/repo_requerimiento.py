from core.config.db import colecion_requerimiento
from core.schemas.Schema_requerimiento import Schema_Requerimiento


def post_requerimiento(model: dict) -> dict:
    try:
        data = colecion_requerimiento.insert_one(model)
        if data:
            return colecion_requerimiento.find_one(data.inserted_id)
        return False
    except Exception as e:
        print(e)


def get_requerimiento(codigo_req: str) -> dict:
    try:
        data = colecion_requerimiento.find_one({'codigo_req': codigo_req})
        if data:
            return data
        return False
    except Exception as e:
        print(e)


def get_requerimientos() -> list:
    try:
        data = [x for x in colecion_requerimiento.find()]
        if len(data) > 0:
            return data
        return False
    except Exception as e:
        print(e)
