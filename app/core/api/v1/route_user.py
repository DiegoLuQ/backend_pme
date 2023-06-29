from datetime import timedelta
from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from core.db.repo_user import *
from core.schemas.Schema_user import Schema_User
from utils.hash import hash_password
from pathlib import Path
import pandas as pd

router = APIRouter()
excel = Path('.') / 'pme_2.xlsx'


@router.post('/registrar')
def add_usuario(model: Schema_User):
    try:
        model.contraseña = hash_password(model.contraseña)
        data = jsonable_encoder(model)

        registered_data = registar_usuario(data)

        if registered_data:
            # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

            # token_data = create_access_token(
            #     data={
            #         "sub": registered_data['correo'],
            #         "perfil": registered_data['perfil'],
            #         "nombre": registered_data['nombre']
            #     }, expires_delta=access_token_expires)
            # print(token_data)
            return JSONResponse(status_code=201,
                                content={
                                    "msg": "Usuario registrado",
                                    "data": registered_data
                                })
        return JSONResponse(status_code=400,
                            content={"msg": "Usuario no creado"})

    except Exception as e:
        print(e)


@router.get("/")
def get_usuarios():
    try:
        data = buscar_usuarios()
        return data
    except Exception as e:
        print(e)


@router.post('/registrar_usuarios')
def post_usuarios(sheetname: str):
    try:
        df = pd.read_excel(excel, sheet_name=sheetname)
        data = df.to_dict('records')
        for x in range(len(data)):
            data[x]['subareas'] = data[x]['subareas'].split(',')
            data[x]['id_colegio'] = data[x]['id_colegio'].split(',')
            data[x]['contraseña'] = hash_password(data[x]['contraseña'])
        new_data = [jsonable_encoder(Schema_User(**x)) for x in data]
        data_registrada = registrar_usuarios(new_data)

        if data_registrada:
            return JSONResponse(status_code=200, content={"msg":"Usuarios Registrados"})
        return JSONResponse(status_code=400, content={"msg":"Los usuarios no fueron registrados"})
    except Exception as e:
        print(e)
