from core.config.db import coleccion_presupuesto



def validar(*args, **kwargs):
    try:

        data = coleccion_presupuesto.find_one({
            'year': kwargs['year'],
            'id_colegio': kwargs['id_colegio']
        })
        if data:
            return False
        return True

    except Exception as e:
        print(e)


def insertar_presupuesto(model: dict):
    try:
        data = validar(**model)
        if data:
            coleccion_presupuesto.insert_one(model)
            return True
        return False
    except Exception as e:
        print(e)


def obtener_presupuestos(id_colegio):
    try:
        data = [
            x for x in coleccion_presupuesto.find({'id_colegio': id_colegio})
        ]
        return data
    except Exception as e:
        print(e)
