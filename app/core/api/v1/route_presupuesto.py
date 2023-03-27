from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from core.schemas.Schema_presupuesto import Schema_Presupuesto
import core.db.repo_presupuesto as repo

router = APIRouter()


@router.post('/registrar')
def registrar_presupuesto(model: Schema_Presupuesto):
    try:
        new_data = repo.insertar_presupuesto(jsonable_encoder(model))
        if new_data:
            return JSONResponse(status_code=201,
                                content={
                                    'msg': 'Presupuesto Registrado'
                                })
    except Exception as e:
        print(e)

@router.get('/{id_colegio}')
def listar_presupuestos(id_colegio):
    try:
      data = repo.obtener_presupuestos(id_colegio)
      return JSONResponse(status_code=200, content=data)
    except Exception as e:
      print(e)