from core.config.db import coleccion_user

def registar_usuario(model: dict):
    try:

        data = coleccion_user.insert_one(model)
        if data:
            new_data = coleccion_user.find_one({"_id": data.inserted_id})
            return new_data
    except Exception as e:
        print(e)


def buscar_usuarios() -> list:
    try:
        data = [x for x in coleccion_user.find()]
        if len(data) > 0:

            return data
        return []
    except Exception as e:
        print(e)


def buscar_usuario_x_correo(correo: str) -> dict:
    try:
        data = coleccion_user.find_one({'correo': correo})
        if not data:
            return False
        return data
    except Exception as e:
        print(e)

def registrar_usuarios(model:list):
    try:
      data = coleccion_user.insert_many(model)
      if data:
          return True
      return False
    except Exception as e:
      print(e)