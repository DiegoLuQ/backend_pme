from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId
from datetime import datetime


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Schema_Recursos(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    id_pme: str = None
    uuid_accion: str = None

    dimension: str = None
    subdimension: str = None
    nombre_actividad: str = None
    descripcion_actividad: str = None
    medios_ver: str = None
    responsable: str = None
    recursos_actividad: List[str]
    monto: int = None
    year:int = None
    fecha = datetime.today()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id_pme": "string",
                "uuid_accion": "string",
                "dimension": "string",
                "subdimension": "string",
                "nombre_actividad": "string",
                "descripcion_actividad": "string",
                "medios_ver": "string",
                "responsable": "string",
                "recursos_actividad": ["string"],
                "monto": 0,
                "year":2023
            }
        }


class Schema_Recursos_Update(BaseModel):
    nombre_actividad: str = None
    recursos_actividad: List[str] = None
    dimension: str = None
    id_pme: str = None
    subdimension: str = None
    descripcion_actividad: str = None
    medios_ver: str = None
    responsable: str = None
    monto: int = None
    uuid_accion: str = None
    fecha: datetime = None
    year:int = None