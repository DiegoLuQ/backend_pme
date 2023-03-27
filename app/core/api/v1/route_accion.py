from fastapi import APIRouter, HTTPException, status
from core.schemas.Schema_acciones import Schema_Acciones, Schema_Acciones_Update
from typing import List
from fastapi.responses import JSONResponse
from core.db.repo_acciones import (crear_accion, listar_acciones,listar_acciones_por_fecha,
                                   crear_acciones, get_actividades,
                                   patch_accion)
from fastapi.encoders import jsonable_encoder
from pathlib import Path
import pandas as pd

excel = Path('.') / 'pme_2.xlsx'

router = APIRouter()


@router.get(
    '/excel/',
    description=
    """ Lectura de contenido en excel para posteriormente registrarlos los datos obtenidos """
)
def pme_excel():
    try:
        df = pd.read_excel(excel, sheet_name='PME')
        data = df.to_dict('records')
        print(data[0])
        return data
    except Exception as e:
        print(e)


@router.post(
    '/registrar_acciones/',
    description=
    """Solo utilizarlo para una gran registro de acciones + excel + insert_many"""
)
def registrar_acciones_excel():
    try:
        df = pd.read_excel(excel, sheet_name='pme_dp')
        data = df.to_dict('records')
        print(data)
        # data[0]["subdimensiones"] = data[0]["subdimensiones"].split(',')
        # data[0]["planes"] = data[0]["planes"].split(',')

        for x in range(len(data)):
            data[x]["subdimensiones"] = data[x]["subdimensiones"].split(',')
        new_data = [jsonable_encoder(Schema_Acciones(**x)) for x in data]
        data = crear_acciones(new_data)

        if data:
            return JSONResponse(status_code=200,
                                content={
                                    "msg": "Acciones registradas",
                                    "data": data
                                })
        return JSONResponse(status_code=400,
                            content={
                                "msg": "Acciones no registradas",
                                "data": []
                            })
    except Exception as e:
        print(e)


@router.post('/')
def registrar_accion(model: Schema_Acciones):
    try:
        new_model = jsonable_encoder(model)
        data = crear_accion(new_model)
        if data:
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content={
                                    "msg": "Accion creada",
                                    "data": data
                                })
        return HTTPException(detail={"msg": "Accion no creada"},
                             status_code=400)
    except Exception as e:
        print(e)


@router.get('/')
def listando_acciones():
    try:
        lista = listar_acciones()
        return lista
    except Exception as e:
        print(e)

@router.get('/update_acciones/')
def listando_acciones_entre_fecha():
    try:
        lista = listar_acciones_por_fecha()
        return lista
    except Exception as e:
        print(e)


@router.get('/actividades/')
def obtener_activiades_x_accion(id: str):
    try:
        data = get_actividades(id)
        if data:
            return data
    except Exception as e:
        print(e)


@router.patch('/accion/{id}')
def patch_accion_pme(id: str, model: Schema_Acciones_Update):
    try:
        data = patch_accion(id, model)
        if data is False:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={"msg": "Accion no se encontro"})

        if data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"msg": "Accion Actualizada"})

        return HTTPException(detail={"msg": "Error con el sistema"},
                             status_code=500)
    except Exception as e:
        print(e)
