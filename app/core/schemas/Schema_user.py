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



class Schema_User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombre: str
    contraseña: str
    apellido: str
    correo: str
    perfil: str
    active = False
    is_superuser = False
    id_colegio: str

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
                "id_colegio":""
            }
        }

class Schema_User_Update(BaseModel):
    nombre: str = None
    apellido: str = None
    correo: str = None
    perfil: str = None
    estado = False
    id_colegio: str = None


class ShowLogin(BaseModel):
    username:str
    password:str

    class Config:
        orm_mode = True