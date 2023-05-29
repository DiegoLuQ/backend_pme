from core.config.db import coleccion_pme
from core.schemas.Schema_PME import Schema_PME, Schema_PME_Upedate


def verificar_pme(id_pme):
    try:
      verify = coleccion_pme.find_one({'_id':id_pme})
      if verify:
          return True
      return False
    except Exception as e:
      print(e)

def registrar_pme(model: dict):
    try:
        data = coleccion_pme.find_one({
            'id_colegio': model["id_colegio"],
            'year': model['year']
        })
        if data:
            return False
        data = coleccion_pme.insert_one(model)
        if data:
            new_data = coleccion_pme.find_one({'_id': data.inserted_id})
            return new_data
        return False
    except Exception as e:
        print(e)


def buscar_pme_por_anio(id_colegio: str):
    try:
        data = [x for x in coleccion_pme.find({'id_colegio': id_colegio})]
        if data is None:
            return None
        if data:
            return data
        return False
    except Exception as e:
        print(e)


def listar_pme():
    try:
        #   data = [x for x in coleccion_pme.find()]
        result = coleccion_pme.aggregate([{
            '$lookup': {
                'from': 'colegios',
                'localField': 'id_colegio',
                'foreignField': '_id',
                'as': 'colegio'
            }
        }, {
            '$project': {
                "colegio.direccion": 0,
                "colegio.imagen": 0,
                "colegio.rut": 0,
                "colegio.telefono": 0,
                "colegio._id": 0,
            }
        }])

        return list(result)
    except Exception as e:
        print(e)


def eliminar_pme(id: str):
    try:
        data = coleccion_pme.find_one({'_id': id})
        if data:
            return True
        return False
    except Exception as e:
        print(e)


def patch_pme(id: str, model: Schema_PME_Upedate):
    try:
        data_pme = coleccion_pme.find_one({'_id': id})
        if data_pme:
            data_obj = dict(Schema_PME_Upedate(**data_pme))
            data_obj.update(model.dict(exclude_unset=True))
            data_update = coleccion_pme.update_one({'_id': id},
                                                   {'$set': data_obj})
            if data_update:
                return True
            return False
    except Exception as e:
        print(e)


def acciones_pme(id: str):
    try:
        result = coleccion_pme.aggregate([{
            "$match": {
                "_id": id
            }
        }, {
            "$lookup": {
                "from": "acciones",
                "localField": "_id",
                "foreignField": "id_pme",
                "as": "acciones_pme"
            }
        }, {
            "$project": {
                "_id": 0
            }
        }])
        # print(list(result))
        return list(result)
    except Exception as e:
        print(e)


def actividades_del_colegio_x_accion(id: str):
    try:
        result = coleccion_pme.aggregate([{
            "$match": {
                "_id": id
            }
        }, {
            "$lookup": {
                "from": "actividades",
                "localField": "_id",
                "foreignField": "id_pme",
                "as": "actividades"
            }
        }])
        return list(result)
    except Exception as e:
        print(e)



#sin repo pero sirve de ejemplo
def actividades_del_colegio_x_pme(id: str):
    try:
        result = coleccion_pme.aggregate([{
            "$match": {
                "_id": id
            }
        }, {
            "$lookup": {
                "from": "acciones",
                "localField": "_id",
                "foreignField": "id_pme",
                "as": "acciones"
            }
        }, {
            "$lookup": {
                "from": "actividades",
                "localField": "_id",
                "foreignField": "id_pme",
                "as": "detalles"
            }
        }, {
            "$unwind": "$detalles"
        }, {
            "$group": {
                "_id": "$acciones.nombre_accion",
                "acciones": {
                    "$push": "$acciones.nombre_accion"
                },
                "detalles": {
                    "$push": "$detalles"
                }
            }
        }])
        return list(result)
    except Exception as e:
        print(e)


"""
https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/
result = coleccion_pme.aggregate([
            {
                "$match": {
                    "_id": id
                }
            },
            {
                "$lookup": {
                    "from": "acciones",
                    "localField": "_id",
                    "foreignField": "id_pme",
                    "as": "acciones"
                }
            },
            {
                "$unwind": "$acciones"
            },
            {
                "$replaceRoot": {
                    "newRoot": {
                        "$mergeObjects": [{
                            "$arrayElemAt": ["$acciones", 0]
                        }, "$$ROOT"]
                    }
                }
            },{ "$project": { "fromItems": 0 } }
                    ])
"""
