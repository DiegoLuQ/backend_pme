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



class Schema_User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombre: str
    contraseña: str
    apellido: str
    correo: str
    perfil: str
    is_superuser = False
    id_colegio: List[str]
    cargo:str
    area:str
    subareas: List[str] # esto servira para agregar a los combobox del frontend y rellenar la opcion de areas en el requerimiento
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nombre":"Diego", 
                "apellido":"Luque",
                "correo":"info@gmail.com",
                "contraseña":"123456",
                "perfil":"usuario",
                "id_colegio":"",
                "cargo":"asistente",
                "area":"gestion y control",
                "subareas":["",""]
            }
        }

class Schema_User_Update(BaseModel):
    nombre: str = None
    apellido: str = None
    correo: str = None
    perfil: str = None
    estado = False
    id_colegio: List[str] = None
    cargo:str = None
    area:str = None
    subareas: List[str]

class ShowLogin(BaseModel):
    username:str
    password:str

    class Config:
        orm_mode = True