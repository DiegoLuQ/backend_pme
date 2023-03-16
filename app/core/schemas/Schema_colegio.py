from pydantic import BaseModel, Field
from typing import List, Optional
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


class SchemaColegio(BaseModel):
    id:PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombre:str
    direccion:str
    telefono:str
    rbd:str
    rut:str
    director: str
    imagen:Optional[dict] = None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example':{
                'nombre':'Colegio Macaya',
                'direccion':'Av. Pampa 3755',
                'telefono': '+5698225599',
                'rbd': '985',
                'rut': '18899479-2',
                'director': 'nombre directo',
                'imagen':{}
            }
        }

class SchemaColegioUpdate(BaseModel):
    nombre:str = None
    direccion:str = None
    telefono:str = None
    rbd:str = None
    rut:str = None
    director:str =None
    imagen:Optional[dict] = None