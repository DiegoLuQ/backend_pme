from core.config.db import coleccion_accion
from core.schemas.Schema_acciones import Schema_Acciones_Update
from datetime import datetime, date
import datetime as dt

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

def crear_acciones_anio_anterior(data:list):
    try:
      coleccion_accion.insert_many(data)
      return True
    except Exception as e:
      print(e)

def listar_acciones(id_pme:str):
    try:
        data = [x for x in coleccion_accion.find({"id_pme":id_pme})]
        if data:
            return data
        return False
    except Exception as e:
        print(e)

def listar_acciones_id_pme(id_pme):
    try:
        data = [x for x in coleccion_accion.find({'id_pme':id_pme}, {'_id':0})]
        if data:
            return data
        return False
    except Exception as e:
        print(e)


def listar_acciones_por_fecha():
    try:
        fecha_desde = datetime.today() - dt.timedelta(days=15)
        fecha_hasta = datetime.today() + dt.timedelta(days=61)
        # print(fecha_desde, fecha_hasta)
        filtro = coleccion_accion.find({
            "fecha_actualizacion": {
                "$gte": fecha_desde,
                "$lte": fecha_hasta,
            }
        })
        data = [x for x in filtro]
        if data:
            return data
        return False
    except Exception as e:
        print(e)


def patch_accion(id: str, model: Schema_Acciones_Update):
    try:
        data_accion = coleccion_accion.find_one({'_id': id})
        data_accion['fecha_actualizacion'] = datetime.today()
        if data_accion:
            data_obj = dict(Schema_Acciones_Update(**data_accion))
            data_obj.update(model.dict(exclude_unset=True))
            data_update = coleccion_accion.update_one({'_id': id},
                                                      {'$set': data_obj})
            if data_update:
                return True
            return False
    except Exception as e:
        print(e)


def get_actividades(uuid_accion: str):
    try:
        result = coleccion_accion.aggregate([{
            "$match": {
                "uuid_accion": uuid_accion
            }
        }, {
            "$lookup": {
                "from": "recursos",
                "localField": "uuid_accion",
                "foreignField": "uuid_accion",
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


def delete_acciones(id_pme:str):
    try:
      if id_pme:
          coleccion_accion.delete_many({'id_pme':id_pme})
          return True
    except Exception as e:
      print(e)