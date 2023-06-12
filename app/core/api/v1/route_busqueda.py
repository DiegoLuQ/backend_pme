from fastapi import APIRouter
from core.schemas.Schema_buscar import Schema_Buscar
from core.db.repo_busqueda import get_busquedas, post_recurso_en_busqueda
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post('/')
def agregar_busqueda(model: Schema_Buscar):
    try:
        data = post_recurso_en_busqueda(jsonable_encoder(model))
        if data:
            return JSONResponse(status_code=201,
                                content={"msg": "busqueda registrada"})
        return JSONResponse(status_code=400,
                            content={"msg": "busqueda NO registrada"})

    except Exception as e:
        print(e)

@router.get('/')
def obtener_busquedas():
    try:
      data = get_busquedas()
      if data:
         return JSONResponse(status_code=200, content={"data":data})
      return JSONResponse(status_code=400, content={"data":data})
    except Exception as e:
      print(e)