from core.config.db import db
from core.schemas.Schema_acciones import Schema_Acciones_Update
coleccion_accion = db.acciones
from datetime import datetime

def crear_accion(model: str):
    try:
        data = coleccion_accion.insert_one(model)
        if data:
            new_data = coleccion_accion.find_one({'_id': data.inserted_id})
            return new_data
    except Exception as e:
        print(e)


def crear_acciones(lista_de_acciones_excel: list):
    try:
        coleccion_accion.insert_many(lista_de_acciones_excel)
        return True
    except Exception as e:
        print(e)


def listar_acciones():
    try:
        data = [x for x in coleccion_accion.find()]
        if data:
            return data
        return False
    except Exception as e:
        print(e)


def patch_accion(id:str, model: Schema_Acciones_Update):
    try:
        data_accion = coleccion_accion.find_one({'_id':id})
        data_accion['fecha_actualizacion'] = datetime.today()
        if data_accion:
            data_obj = dict(Schema_Acciones_Update(**data_accion))
            data_obj.update(model.dict(exclude_unset=True))
            data_update = coleccion_accion.update_one({'_id':id}, {'$set':data_obj})
            if data_update:
                return True
            return False
    except Exception as e:
        print(e)


def get_actividades(id: str):
    try:
        result = coleccion_accion.aggregate([{
            "$match": {
                "_id": id
            }
        }, {
            "$lookup": {
                "from": "actividades",
                "localField": "_id",
                "foreignField": "id_accion",
                "as": "actividades"
            }
        }, {
            "$project": {
                "_id": 0
            }
        }])

        return list(result)
    except Exception as e:
        print(e)
