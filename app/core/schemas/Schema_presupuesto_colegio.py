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


class Schema_Presupuesto_Colegio(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    area:str
    sub_area:str
    descripcion:str
    cantidad :str
    presentacion:str
    mes_compra:str
    motivo_actividad:str
    id_presupuesto: str
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example':{
                "area":"Dirección",
                "sub_area":"Secretaria",	
                "descripcion":"Alfileres",                
                "cantidad":4,
                "presentacion":"Paquetes",
                "mes_compra":"marzo",
                "motivo_actividad":"insumos oficina",
                "id_presupuesto":"id_presupuesto"                
            }
        }