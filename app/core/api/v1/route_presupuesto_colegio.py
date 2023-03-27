from fastapi import APIRouter, status, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from core.schemas.Schema_presupuesto_colegio import Schema_Presupuesto_Colegio
from core.db.repo_presupuesto_colegio import insertar_presupuesto, listar_presupuesto
from pathlib import Path
import pandas as pd
from io import BytesIO
excel = Path('.') / 'pme_2.xlsx'

router = APIRouter()

@router.post('/registrar_lista')
def importar_excel_presupuesto():
    try:
        df = pd.read_excel(excel, sheet_name='pre_mc_2023')
        presupuesto = df.to_dict('records')
        data_presupuesto = [
            jsonable_encoder(Schema_Presupuesto_Colegio(**x)) for x in presupuesto
        ]
        data = insertar_presupuesto(data_presupuesto)
        if data:
            return JSONResponse(status_code=200,
                                content={
                                    "msg": "Presupuesto registrado",
                                    "data": data
                                })

        return JSONResponse(status_code=400,
                                content={
                                    "msg": "Presupuesto no registrado",
                                    "data": []
                                })
    except Exception as e:
        print(e)

@router.get('/{id_presupuesto}')
def get_presupuesto_x_id(id_presupuesto:str):
    try:
      data = listar_presupuesto(id_presupuesto)
      return data
    except Exception as e:
      print(e)


@router.post('/uploadfile/')
async def registrar_execl_presupuesto(id:str, file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_excel(BytesIO(content), sheet_name='prueba')
    pre = df.to_dict('records')
    # for x in pre:
    #     x['id_presupuesto'] = id
    new_data = [{**x, 'id_presupuesto':id} for x in pre]
    return {"nombre":file.filename, 'data': new_data}
