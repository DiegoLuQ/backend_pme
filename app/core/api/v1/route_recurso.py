from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pathlib import Path
import pandas as pd
from core.schemas.Schema_recursos import Schema_Recursos, Schema_Recursos_Update
from core.db.repo_recursos import (registrar_recurso, obtener_recursos,
                                   obtener_recursos_de_actividad,
                                   modificar_recurso, registrar_actividades,
                                   eliminar_actividades_many)

router = APIRouter()

excel = Path('.') / 'pme_2.xlsx'


@router.post('/register')
def add_recurso(model: Schema_Recursos):
    try:
        encoder_model = jsonable_encoder(model)
        data = registrar_recurso(encoder_model)
        if data:
            return JSONResponse(status_code=201,
                                content={
                                    "msg": "Recurso creado",
                                    "data": data
                                })
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"msg": "Hubo problemas al registrar el recurso"})
    except Exception as e:
        print(e)


@router.post('/registrar_actividades/{hoja}')
def add_actividades(hoja:str):
    try:
        df = pd.read_excel(excel, sheet_name=hoja)
        data = df.to_dict('records')
        for x in range(len(data)):
            data[x]['recursos_actividad'] = data[x][
                'recursos_actividad'].split(',')
        new_data = [jsonable_encoder(Schema_Recursos(**x)) for x in data]
        data_registrada = registrar_actividades(new_data)
        if data_registrada:
            return JSONResponse(status_code=200,
                                content={
                                    "msg": "Actividades registradas",
                                    "data": data_registrada
                                })
        return JSONResponse(status_code=400,
                            content={
                                "msg": "Actividades no registradas",
                                "data": []
                            })
    except Exception as e:
        print(e)


@router.get('/{id_pme}')
def get_recursos(id_pme: str):
    try:
        lista = obtener_recursos(id_pme)
        return lista
    except Exception as e:
        print(e)


@router.get('/obtener_recursos_de_actividad/')
def get_recursos_de_actividad(uuid_accion: str):
    try:
        data = obtener_recursos_de_actividad(uuid_accion)
        return data
    except Exception as e:
        print(e)


@router.patch('/modificar_recurso/{id}')
def patch_recurso(id: str, model: Schema_Recursos_Update):
    try:
        # return {"id":id, "model":model, "status":200}
        dato_recurso = modificar_recurso(model, id)
        if dato_recurso:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"msg": "Recurso Modificado"})
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": "Hubo un error. Comuniquese con el Administrador"})
    except Exception as e:
        print(e)


@router.delete('/delete/actividades/{id_pme}')
def eliminar_actividades(id_pme: str):
    try:
        data = eliminar_actividades_many(id_pme)
        if data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"msg": "Actividades Eliminadas"})
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"msg": "Actividades NO Eliminadas"})

    except Exception as e:
        print(e)
