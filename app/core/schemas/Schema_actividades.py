from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from bson import ObjectId
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


class Schema_Actividades(BaseModel):
    id:PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombre: str 
    detalle: str
    detallt_lista: List[str]
    id_accion:str
    id_pme:str
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example':{
                'nombre':'Grandes Eventos',
                'detalle':'Eventos tales como: dia de la madre, del padre, dia del niño...',
                'detallt_lista':["Dia del niño", "Fiesta Patrias", "Aniversario"],
                'id_accion':'159966332211',
                'id_pme':'640b3e57434fbf409d0dd85c'
            }
        }
    
class Schema_Actividades_Update(BaseModel):
    nombre: str = None
    detalle: str = None
    detallt_lista: List[str] = None
    id_accion:str = None
    id_pme:str = None