from fastapi import APIRouter, status, HTTPException
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from pathlib import Path
import pandas as pd
from io import BytesIO
from core.schemas.Schema_recursos import Schema_Recursos, Schema_Recursos_Update
from core.db.repo_recursos import (
    registrar_recurso, obtener_recursos, obtener_recursos_de_actividad,
    modificar_recurso, registrar_actividades, eliminar_actividades_many,
    obtener_actividades_por_pme, obtener_actividad, agregar_year_a_actividad,
    agregar_actividades_de_pme_anterior, obtener_actividades)
from core.db.repo_pme import verificar_pme
from datetime import datetime

router = APIRouter()
excel = Path('.') / 'pme_2.xlsx'


@router.post('/register')
def add_recurso(model: Schema_Recursos):
    try:
        encoder_model = jsonable_encoder(model)
        # encoder_model["fecha"] = datetime.today()
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
def add_actividades(hoja: str):
    try:
        df = pd.read_excel(excel, sheet_name=hoja)
        data = df.to_dict('records')
        for x in range(len(data)):
            data[x]['recursos_actividad'] = data[x]['recursos_actividad'].split(',')
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


@router.get('/descargar/pme/{id_pme}')
def descargar_actividad_pme(id_pme: str):
    try:
        data = obtener_actividades_por_pme(id_pme=id_pme)
        df = pd.DataFrame(data)

        # Crear un objeto BytesIO en lugar de guardar el archivo en disco
        excel_file = BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(
            0)  # Asegurarse de que el puntero esté al principio del archivo

        # Configurar la respuesta HTTP para descargar el archivo
        return StreamingResponse(
            iter([excel_file.getvalue()]),
            media_type=
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                'Content-Disposition': 'attachment;filename=actividades.xlsx'
            })
    except Exception as e:
        print(e)


@router.get('/{id_pme}/{year}')
def get_recursos(id_pme: str, year: int):
    try:
        lista = obtener_recursos(id_pme, year)
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
        model.fecha = str(datetime.now())
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


@router.get('/buscar/actividad/{id_actividad}')
def get_actividad(id_actividad: str):
    try:
        data = obtener_actividad(id_actividad)
        if data:
            return JSONResponse(status_code=200,
                                content={
                                    "msg": "Actividad",
                                    "data": data
                                })
        return JSONResponse(status_code=400,
                            content={
                                "msg": "No se encontró la actividad",
                                "data": data
                            })
    except Exception as e:
        print(e)


@router.put('/add_year')
def add_year_actividad_pme(id_pme: str, year: int):
    try:
        data = agregar_year_a_actividad(id_pme, year)
        if data:
            return JSONResponse(
                status_code=200,
                content={
                    "msg":
                    "El año fue agregado a las actividades seleccionadas"
                })
        return JSONResponse(
            status_code=400,
            content={
                "msg":
                "El año NO fue agregado en las actividades seleccionadas"
            })
    except Exception as e:
        print(e)


@router.post("/copiar/actividades/{id_pme}/{new_id_pme}/{year}")
def add_actividades_de_pme_anterior(id_pme: str, new_id_pme: str, year: int):
    try:
        if id_pme == new_id_pme:
            return JSONResponse(status_code=400,
                                content={"msg": "Los PME son iguales"})
        actividadesRegistradas = obtener_actividades(new_id_pme)
        if len(actividadesRegistradas) > 1:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"msg": "PME ya tiene Actividades registradas"})
        new_pme = verificar_pme(new_id_pme)
        if new_pme:
            data = obtener_actividades(id_pme)
            new_data = [{
                **x, 'id_pme': new_id_pme,
                'year': year,
                "fecha": datetime.today()
            } for x in data]
            data_json = [
                jsonable_encoder(Schema_Recursos(**y)) for y in new_data
            ]
            new_data_register = agregar_actividades_de_pme_anterior(data_json)
            if new_data_register:
                return JSONResponse(
                    status_code=201,
                    content={
                        "msg":
                        "Las Actividades fueron creadas para este nuevo año",
                        "data": new_data_register
                    })
            return JSONResponse(
                status_code=400,
                content={"msg": "No se pudo crear las nuevas Actividades"})
        else:
            return JSONResponse(
                status_code=400,
                content={"msg": "La id del nuevo pme no existe"})
    except Exception as e:
        print(e)
