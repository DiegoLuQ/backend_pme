from fastapi import APIRouter, HTTPException
from core.config.db import coleccion_pme, coleccion_accion, coleccion_actividades

router = APIRouter()

@router.delete('/delete')
def delete_all_pme_data(id_pme: str, year: int, id_colegio: str):
    try:
        # Verificar si el PME existe
        pme = coleccion_pme.find_one({"_id": id_pme, "year": year, "id_colegio": id_colegio})
        if not pme:
            raise HTTPException(status_code=404, detail="PME not found")

        # Eliminar acciones, actividades y PME
        coleccion_accion.delete_many({"id_pme": id_pme})
        coleccion_actividades.delete_many({"id_pme": id_pme})
        coleccion_pme.delete_one({"_id": id_pme})

        return {"message": "PME, actions, and activities deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
