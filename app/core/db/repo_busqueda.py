from core.config.db import coleccion_busqueda

def post_recurso_en_busqueda(model:dict):
    try:
      data = coleccion_busqueda.insert_one(model)
      if data:
         return True
      return False
    except Exception as e:
      print(e)
    
def get_busquedas():
   try:
     data = [x for x in coleccion_busqueda.find()]
     if len(data) > 0:
        return data
     return False
   except Exception as e:
     print(e)