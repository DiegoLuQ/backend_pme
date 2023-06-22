from core.schemas.Schema_recursos import Schema_Recursos, Schema_Recursos_Update
from core.config.db import coleccion_recursos


def registrar_recurso(model: dict):
    try:
        data = coleccion_recursos.insert_one(model)

        if data:
            new_data = coleccion_recursos.find_one({'_id': data.inserted_id})

            return new_data
        return False

    except Exception as e:
        print(e)


def registrar_actividades(lista_actividades_pme_interno: list):
    try:
        coleccion_recursos.insert_many(lista_actividades_pme_interno)
        return True
    except Exception as e:
        print(e)


def obtener_recursos(id_pme):
    try:
        result = coleccion_recursos.aggregate([{
            "$match": {
                "id_pme": id_pme
            }
        }, {
            "$lookup": {
                "from": "acciones",
                "localField": "uuid_accion",
                "foreignField": "uuid_accion",
                "as": "accion"
            }
        }, {
            "$unwind": "$accion"
        }, {
            "$project": {
                "accion.monto_sep": 0,
                "accion.monto_total": 0,
                "accion.fecha_inicio": 0,
                "accion.fecha_termino": 0,
                "accion.fecha_actualizacion": 0,
                "accion.planes": 0,
            }
        }])
        return list(result)
    except Exception as e:
        print(e)


def obtener_actividades_por_pme(id_pme):
    try:
        result = coleccion_recursos.find({'id_pme': id_pme}, {
            '_id': 0,
            'id_pme': 0,
            'fecha': 0,
            'monto': 0
        })

        data = [{
            **x, "recursos_actividad": ", ".join(x['recursos_actividad'])
        } for x in result]
        return data
    except Exception as e:
        print(e)


def obtener_recursos_de_actividad(uuid_accion: str):
    try:
        result = coleccion_recursos.aggregate([{
            "$match": {
                "uuid_accion": uuid_accion
            }
        }, {
            "$lookup": {
                "from": "actividades",
                "localField": "uuid_accion",
                "foreignField": "uuid_accion",
                "as": "actividad"
            }
        }, {
            "$lookup": {
                "from": "acciones",
                "localField": "uuid_accion",
                "foreignField": "uuid_accion",
                "as": "accion"
            }
        }, {
            "$project": {
                "_id": 0,
                "accion.monto_sep": 0,
                "accion.monto_total": 0,
                "accion.fecha_inicio": 0,
                "accion.fecha_termino": 0,
                "accion.fecha_actualizacion": 0,
                "accion.planes": 0,
            }
        }])
        return list(result)
    except Exception as e:
        print(e)


def modificar_recurso(model: Schema_Recursos_Update, id: str):
    try:
        dato_recurso = coleccion_recursos.find_one({'_id': id})
        if dato_recurso:
            data_obj = dict(Schema_Recursos_Update(**dato_recurso))
            data_obj.update(model.dict(exclude_unset=True))
            data_update = coleccion_recursos.update_one({'_id': id},
                                                        {'$set': data_obj})

            if data_update:
                return True
            return False
        return False
    except Exception as e:
        print(e)


def eliminar_actividades_many(id_pme: str):
    try:
        if id_pme:
            coleccion_recursos.delete_many({'id_pme': id_pme})
            return True
        return False

    except Exception as e:
        print(e)


def obtener_actividad(id_actividad: str) -> dict:
    try:
        print(id_actividad)
        data =  coleccion_recursos.find_one({"_id":id_actividad})
        if data:
            return data
        else:
            return False
    except Exception as e:
        print(e)
