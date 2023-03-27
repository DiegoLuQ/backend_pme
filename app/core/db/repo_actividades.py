from core.config.db import db
from core.schemas.Schema_actividades import Schema_Actividades, Schema_Actividades_Update

coleccion_actividades = db.actividades


def registrar_actividad(model: dict):
    try:
        data = coleccion_actividades.insert_one(model)
        if data:
            return coleccion_actividades.find_one({'_id': data.inserted_id})
        return False
    except Exception as e:
        print(e)


def mostrar_actividad(id: str):
    try:
        data = coleccion_actividades.find_one({'_id': id})
        if data is None:
            return False
        return data
    except Exception as e:
        print(e)


def mostrar_actividades():
    try:
        result = coleccion_actividades.aggregate([{
            "$lookup": {
                "from": "pme",
                "localField": "id_pme",
                "foreignField": "_id",
                "as": "pme"
            }
        }, {
            "$unwind": "$pme"
        }, {
            "$project": {
                "_id": 0,
            }
        }])

        datas = [x for x in result]
        return datas
    except Exception as e:
        print(e)


def eliminar_actividad(id: str):
    try:
        data = coleccion_actividades.find_one({'_id': id})
        if data is None:
            return False
        coleccion_actividades.delete_one({'_id': id})
        return True
    except Exception as e:
        print(e)


def patch_actividad(id: str, model: Schema_Actividades_Update):
    try:
        data_subaccion = coleccion_actividades.find_one({'_id': id})
        if data_subaccion:
            data_obj = dict(Schema_Actividades_Update(**data_subaccion))
            data_obj.update(model.dict(exclude_unset=True))
            data_update = coleccion_actividades.update_one({'_id': id},
                                                           {'$set': data_obj})
            if data_update:
                return True
            return False
        return False
    except Exception as e:
        print(e)


def actividades_accion(id_pme: str):
    try:
        result = coleccion_actividades.aggregate([{
            "$match": {
                "id_pme": id_pme
            }
        }, {
            "$lookup": {
                "from": "acciones",
                "localField": "id_accion",
                "foreignField": "_id",
                "as": "acciones"
            }
        }, {
            "$unwind": "$acciones"
        }])
        return list(result)
    except Exception as e:
        print(e)
