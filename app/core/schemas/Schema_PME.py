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

class Schema_PME(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    year: int
    observacion: str
    id_colegio:str
    director: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example':{
                "year":2022,
                "observacion":"Observacion del PME del año",
                "director":"Director actual",
                "id_colegio": "159632589963254"
            }
        }
        
class Schema_PME_Upedate(BaseModel):
    year: int = None
    observacion: str = None
    id_colegio:str = None
    director: str = None