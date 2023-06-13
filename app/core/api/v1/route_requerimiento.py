from fastapi import APIRouter
from core.schemas.Schema_requerimiento import Schema_Requerimiento
from core.db.repo_requerimiento import (get_requerimiento, post_requerimiento, get_requerimientos)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post('/registrar')
def registrar_requerimiento(model: Schema_Requerimiento):
    try:

        data = post_requerimiento(jsonable_encoder(model))
        if data:
            return JSONResponse(status_code=201,
                                content={
                                    "msg":
                                    "El requerimiento se creo con exito",
                                    "data": data
                                })
        return JSONResponse(status_code=400,
                            content={
                                "msg": "Acta de requerimiento no creado",
                                "data": data
                            })
    except Exception as e:
        print(e)


@router.get('/{codigo_req}')
def obtener_requerimiento(codigo_req: str):
    try:
        data = get_requerimiento(codigo_req)
        if data:
            return JSONResponse(status_code=200,
                                content={
                                    "msg":
                                    "El requerimiento recuperado con exito",
                                    "data": data
                                })
        return JSONResponse(status_code=404,
                            content={
                                "msg": "El requerimiento no se encontró",
                                "data": data
                            })
    except Exception as e:
        print(e)

@router.get('/buscar_area/{area}')
def obtener_requerimientos(area:str):
    try:
      data = get_requerimientos(area)
      if data:
          return JSONResponse(status_code=200, content={"msg":"Lista de requerimientos", "data":data})
      return JSONResponse(status_code=400, content={"msg":"No se obtuvo los requerimientos"})
    except Exception as e:
      print(e)