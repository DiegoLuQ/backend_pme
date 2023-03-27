from fastapi import APIRouter, status, HTTPException
from core.schemas.Schema_actividades import Schema_Actividades
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from core.db.repo_actividades import (eliminar_actividad, mostrar_actividad,
                                       patch_actividad, registrar_actividad,
                                       mostrar_actividades, actividades_accion)

router = APIRouter()


@router.post('/registrar')
def registrar_actividad_deaccion(model: Schema_Actividades):
    try:
        new_model = jsonable_encoder(model)
        data = registrar_actividad(new_model)
        if data:
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content={
                                    "msg": "Sub Acción creado con exito",
                                    "data": data
                                })
        raise HTTPException(
            status_code=400,
            detail={"msg": "Hubo un error, comunicate con el administrador"})
    except Exception as e:
        print(e)


@router.get('/actividades/accion/')
def mostrar_actividades_de_acciones():
    try:
        data = mostrar_actividades()
        if data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={
                                    "msg": "lista de actividades",
                                    "data": data
                                })
        raise HTTPException(
            status_code=400,
            detail={"msg": "Hubo un error, comunicate con el administrador"})
    except Exception as e:
        print(e)

@router.get('/actividad_de_acciones/{id_pme}')
def obtener_actividades_de_acciones(id_pme:str):
    try:
      result =actividades_accion(id_pme)
      return result
    except Exception as e:
      print(e)