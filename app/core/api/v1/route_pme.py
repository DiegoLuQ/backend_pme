from fastapi import APIRouter, status, HTTPException
from core.schemas.Schema_PME import Schema_PME, Schema_PME_Upedate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from core.db.repo_pme import (listar_pme, buscar_pme_por_anio, eliminar_pme,
                              patch_pme, registrar_pme, acciones_pme,
                              actividades_del_colegio_x_accion,
                              actividades_del_colegio_x_pme)

router = APIRouter()


@router.post('/registrar_pme')
def crear_pme(model: Schema_PME):
    try:
        new_model = jsonable_encoder(model)
        data = registrar_pme(new_model)
        if data:
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content={'data': data})
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={"msg": "PME ya esta registrado"})
    except Exception as e:
        print(e)


@router.get('/pme_colegio/{id_colegio}')
def pme_x_colegio_id(id_colegio: str):
    try:
        data = buscar_pme_por_anio(id_colegio)
        return JSONResponse(status_code=status.HTTP_200_OK, content=data)
    except Exception as e:
        print(e)


@router.get('/')
def obtener_pmes():
    try:
        data = listar_pme()
        if data == []:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={
                                    "msg": "No hay PME registrados",
                                    "data": data
                                })
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={
                                "msg": "PME de Colegios",
                                "data": data
                            })
    except Exception as e:
        print(e)


@router.delete('/{id}')
def eliminar_pme(id: str):
    try:
        data = eliminar_pme(id)
        if data is False:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                                content={"msg": "PME no se encontró"})
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'msg': 'PME Eliminado'})
    except Exception as e:
        print(e)


@router.patch('/{id}')
def editar_pme(id: str, model: Schema_PME_Upedate):
    try:
        data = patch_pme(id, model)
        if data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"msg": "PME Modificado"})
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": "Hubo un error. Comuniquese con el Administrador"})
    except Exception as e:
        print(e)


@router.get('/acciones/{id_pme}')
def get_acciones_pme(id_pme: str):
    try:

        data = acciones_pme(id_pme)
        return data
    except Exception as e:
        print(e)

@router.get('/actividades/{id_pme}')
def get_actividades_pme(id: str):
    try:
        data = actividades_del_colegio_x_accion(id)
        act_data = data[0]
        lista_detalle = []
        [
            lista_detalle.extend(x["detallt_lista"])
            for x in data[0]["actividades"]
        ]

        return act_data
    except Exception as e:
        print(e)

