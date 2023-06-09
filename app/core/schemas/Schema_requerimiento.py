from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List
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

class Accion(BaseModel):
    accion:str
    actividad:str
    dimension:str
    subdimension:str

class Info(BaseModel):
    req_para:str
    req_tipo:str

class ItemRequerimiento(BaseModel):
    cantidad:int
    descripcion:str
    detalle:str
    justificacion:str
    lugar_instalacion:str
    prioridad:str
    recurso:str

class Schema_Requerimiento(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    area:str
    cargo:str
    codigo_req:str
    fecha:str
    hora:str
    id_pme:str
    nombre_colegio:str
    usuario:str
    info:Info
    requerimientos:List[ItemRequerimiento]
    accion: Accion

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}