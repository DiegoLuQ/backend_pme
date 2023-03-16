from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import date, datetime

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

class Schema_Acciones(BaseModel):
    id:PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    subdimension : str = None
    n_de_accion	: int = None
    nombre_accion : str = None
    descripcion	: str = None
    medio_verificacion : str = None	
    responsable	: str = None
    fecha_inicio : date = None
    fecha_limite : date = None
    recursos : str = None
    monto : int = None
    item : str = None
    dimension : str = None
    fecha_actualizacion= datetime.today()
    id_pme : str = None
    

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra ={
            "example": {
                "subdimension" : "Liderazgo del sostenedor",
                "n_de_accion" : 200,
                "nombre_accion" : "Gestionar y controlar acciones  dadas,  orientadas al logro de los objetivos institucionales",
                "descripcion" : "Es necesario contar con un area de Control de Gestion para realizar un acompañamiento efizaz para determinar los avances en las acciones de trabajo que estan orientadas al logro de los objetivos institucionales",
                "medio_verificacion" : "Acta de reuniones - accountability semestral (anual)"	,
                "responsable": "E.Gestión -Sostenedor",
                "fecha_inicio": "2023-03-03",
                "fecha_limite": "2023-03-30",
                "recursos": "Equipo de gestión - directivos",
                "monto": 500000,
                "item": "Reuniones coordinación directiva",
                "dimension": "Liderazgo",
                "id_pme": "15963214",
            }
        }


class Schema_Acciones_Update(BaseModel):
    subdimension : str = None
    n_de_accion	: int = None
    nombre_accion : str = None
    descripcion	: str = None
    medio_verificacion : str = None
    responsable	: str = None
    fecha_inicio : str = None
    fecha_limite : str = None
    recursos : str = None
    monto : int = None
    item : str = None
    dimension : str = None
    fecha_actualizacion: datetime = None
    id_pme : str = None