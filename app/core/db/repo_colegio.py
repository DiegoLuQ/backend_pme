from core.config.db import db
from core.schemas.Schema_colegio import SchemaColegio, SchemaColegioUpdate

coleccion_colegio = db.colegios


def registrar_colegio(model: dict):
    try:
        if coleccion_colegio.find_one({"nombre": model['nombre']}):
            return False
        if coleccion_colegio.find({'rbd': model['rbd']}):
            return False

        colegio = coleccion_colegio.insert_one(model)
        if colegio:
            new_colegio = coleccion_colegio.find_one(
                {"_id": colegio.inserted_id})
            return new_colegio
        return False

    except Exception as e:
        print(e)


def buscar_colegio(nombre: str):
    try:
        data = coleccion_colegio.find_one({"nombre": nombre})

        if data is None:
            return False
        if data:
            return data
        return False
    except Exception as e:
        print(e)


def eliminar_colegio(id: str) -> bool:
    try:
        colegio = coleccion_colegio.find_one({'_id': id})
        if colegio:
            coleccion_colegio.find_one_and_delete({'_id': id})
            return True
        return False
    except Exception as e:
        print(e)


def mostrar_colegios():
    try:
        colegios = [x for x in coleccion_colegio.find()]
        return colegios
    except Exception as e:
        print(e)


def patch_colegio(model: SchemaColegioUpdate, id: str):
    try:
        dato_colegio = coleccion_colegio.find_one({'_id': id})
        if dato_colegio:
            data_obj = dict(SchemaColegioUpdate(**dato_colegio))
            data_obj.update(model.dict(exclude_unset=True))
            data_update = coleccion_colegio.update_one({'_id': id},
                                                       {'$set': data_obj})
            if data_update:
                return True
            return False
        return False
    except Exception as e:
        print(e)


def eliminar_colegio(id: str) -> bool:
    try:
        colegio = coleccion_colegio.find_one({'_id': id})
        if colegio:
            coleccion_colegio.delete_one({'_id': id})
            return True
        return False
    except Exception as e:
        print(e)


def obtener_pme_colegio():
    try:
        result = coleccion_colegio.aggregate([ {
            "$lookup": {
            "from":"pme",
            "localField":"_id",
            "foreignField":'id_colegio',
            "as":"pme_colegio"
            }
        }])
        return list(result)
    except Exception as e:
        print(e)
