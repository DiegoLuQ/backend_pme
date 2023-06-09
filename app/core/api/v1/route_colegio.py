from fastapi import APIRouter, status, HTTPException
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from core.schemas.Schema_colegio import SchemaColegio, SchemaColegioUpdate
from core.db.repo_colegio import (buscar_colegio, eliminar_colegio,
                                  patch_colegio, registrar_colegio,
                                  mostrar_colegios, obtener_pme_colegio,
                                  buscar_colegio_id)

router = APIRouter()


@router.post('/registrar_colegio')
def add_colegio(model: SchemaColegio):
    """
### Data    
    - nombre: string - 'Macaya - Diego Portales'
    - direccion: string - 'Av. La pampa'
    - telefono: string - '57558558'
    - rbd: string - '12655-7'
    - rut: string - '17488748-2'
    - director: string - 'Andres Saavedra'
    - imagen: Object - "logo":'ruta-imagen', "imagen":"ruta-imagen"
    """
    try:
        model = jsonable_encoder(model)
        data = registrar_colegio(model)
        if data is False:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                                content={"msg": "Colegio ya esta registrado"})
        else:
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content={
                                    "msg": "Colegio creado con exito",
                                    "data": data
                                })
    except Exception as e:
        print(e)


@router.get('/')
def colegios():
    try:
        return mostrar_colegios()
    except Exception as e:
        print(e)


@router.get('/{nombre}')
def obtener_colegio(nombre: str):
    try:
        nombre = nombre.title()
        data = buscar_colegio(nombre)
        if data is False:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={"msg": "Colegio no encontrado"})
        if data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"data": data})
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"msg": "Colegio no encontrado"})


@router.get('/buscar/{id_colegio}')
def obtener_colegio_id(id_colegio: str):
    try:
        data = buscar_colegio_id(id_colegio)
        if data is False:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={"msg": "Colegio no encontrado"})
        if data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"data":[data]})
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"msg": "Colegio no encontrado"})

@router.patch('/modificar/{id}')
def modificar_colegio(model: SchemaColegioUpdate, id: str):
    try:
        data = patch_colegio(model, id)
        if data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"msg": "Colegio Modificado"})
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": "Hubo un error. Comuniquese con el Administrador"})
    except Exception as e:
        print(e)


@router.delete('/eliminar/{id}')
def borrar_colegio(id: str):
    try:
        data = eliminar_colegio(id)
        if data:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"msg": "Colegio Eliminado"})
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": "Hubo un error. Comuniquese con el Administrador"})
    except Exception as e:
        print(e)


@router.get('/pme/')
def buscar_pme_colegio():
    try:

        data = obtener_pme_colegio()
        if data:
            return data
    except Exception as e:
        print(e)
