from pydantic import BaseModel, Field
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

class Schema_Buscar(BaseModel):
    id:PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    actividad:str
    area:str
    data_length:int
    fecha:str
    hora:str
    recurso_interno:str
    recurso_pme:str
    usuario:str
    colegio:str
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}