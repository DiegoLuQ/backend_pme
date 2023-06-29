from fastapi import APIRouter, HTTPException, status
from core.schemas.Schema_acciones import Schema_Acciones, Schema_Acciones_Update
from typing import List
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from core.db.repo_acciones import (
    crear_accion, listar_acciones, listar_acciones_id_pme,
    listar_acciones_por_fecha, crear_acciones, get_actividades, patch_accion,
    crear_acciones_anio_anterior, delete_acciones, listar_acciones_user,
    agregar_year_a_accion, obtener_subdimensiones)
from core.db.repo_pme import acciones_pme
from fastapi.encoders import jsonable_encoder
from core.db.repo_pme import verificar_pme
from pathlib import Path
import pandas as pd
from core.helpers.id_random import num_random
from datetime import date, timedelta, datetime
from io import BytesIO

excel = Path('.') / 'pme_2.xlsx'

router = APIRouter()


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


@router.get('/descargar/pme/admin/{id_pme}')
def descargar_pme_admin(id_pme: str):
    
    try:
        data = listar_acciones(id_pme)
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
                'Content-Disposition': 'attachment;filename=accionesPME.xlsx'
            })
    except Exception as e:
        print(e)


@router.get('/descargar/pme/user/{id_pme}')
def descargar_pme_user(id_pme: str):
    
    try:
        data = listar_acciones_user(id_pme)
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
                'Content-Disposition': 'attachment;filename=accionesPME.xlsx'
            })
    except Exception as e:
        print(e)


@router.get('/{id_pme}')
def listando_acciones(id_pme):
    try:
        lista = listar_acciones(id_pme)
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
def obtener_activiades_x_accion(uuid_accion: str, id_pme: str, year:int):
    try:
        data = get_actividades(uuid_accion, id_pme, year)
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


@router.post(
    '/registrar_acciones/',
    description=
    """Solo utilizarlo para una gran registro de acciones + excel + insert_many"""
)
def registrar_acciones_excel():
    try:
        df = pd.read_excel(excel, sheet_name='PME_MC_2023')
        data = df.to_dict('records')
        # data[0]["subdimensiones"] = data[0]["subdimensiones"].split(',')
        # data[0]["planes"] = data[0]["planes"].split(',')

        for x in range(len(data)):
            data[x]["subdimensiones"] = data[x]["subdimensiones"].split(',')
            data[x]["uuid_accion"] = num_random()

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


@router.delete('/delete/{id_pme}')
def eliminar_acciones_por_id_pme(id_pme: str):
    try:
        data = delete_acciones(id_pme=id_pme)
        if data:
            return JSONResponse(status_code=200,
                                content={
                                    "msg": "Acciones Eliminadas",
                                    "data": data
                                })
    except Exception as e:
        print(e)


@router.post('/copiar/acciones/{id_pme}/{new_id_pme}/{year}')
def copiar_acciones_del_anio_anterior(id_pme: str, new_id_pme: str, year:int):
    try:
        if id_pme == new_id_pme:
            return JSONResponse(status_code=400,
                                content={"msg": "Los PME son iguales"})

        comparando_acciones_de_pme = acciones_pme(new_id_pme)
        if len(comparando_acciones_de_pme) > 1:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"msg": "PME ya tiene acciones registradas"})
        new_pme = verificar_pme(new_id_pme)

        if new_pme:
            data = listar_acciones_id_pme(id_pme)
            new_data = [{**x, 'id_pme': new_id_pme, 'year':year,
                "fecha": datetime.today()} for x in data]
            data_json = [
                jsonable_encoder(Schema_Acciones(**y)) for y in new_data
            ]
            new_data_register = crear_acciones_anio_anterior(data_json)
            if new_data_register:
                return JSONResponse(
                    status_code=201,
                    content={
                        "msg":
                        "Las Acciones fueron creadas para este nuevo año",
                        "data": new_data_register
                    })
            return JSONResponse(
                status_code=400,
                content={"msg": "No se pudo crear las nuevas acciones"})
        else:
            return JSONResponse(
                status_code=400,
                content={"msg": "La id del nuevo pme no existe"})

    except Exception as e:
        print(e)


@router.put('/add_year')
def add_year_acciion_pme(id_pme: str, year: int):
    try:
        data = agregar_year_a_accion(id_pme, year)
        if data:
            return JSONResponse(
                status_code=200,
                content={
                    "msg": "El año fue agregado a las acciones seleccionadas"
                })
        return JSONResponse(
            status_code=200,
            content={
                "msg": "El año NO fue agregado en las acciones seleccionadas"
            })

    except Exception as e:
        print(e)


@router.get("/subdimensiones/")
def get_subdimensiones():
    try:
      data = obtener_subdimensiones()
      return data
    except Exception as e:
      print(e)