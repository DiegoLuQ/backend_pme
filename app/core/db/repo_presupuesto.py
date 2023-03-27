from core.config.db import db



coleccion_presupuesto = db.presupuesto


def insertar_presupuesto(model:dict):
    try:
        coleccion_presupuesto.insert_one(model)
        return True
    except Exception as e:
      print(e)
    
def obtener_presupuestos(id_colegio):
   try:
     data = [x for x in coleccion_presupuesto.find({'id_colegio':id_colegio})]
     return data
   except Exception as e:
     print(e)