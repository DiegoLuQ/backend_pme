from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import date, datetime
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


class Schema_Acciones(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    dimension: str = None
    subdimensiones: List[str]
    nombre_accion: str = None
    descripcion: str = None
    fecha_inicio: date = None
    recursos_necesarios_ejecucion: str = None
    fecha_termino: date = None
    planes: str = None
    monto_sep: int = None
    monto_total: int = None
    id_pme: str = None
    fecha_actualizacion = datetime.today()
    # medio_de_verificacion: str = None
    # monto_subvencion_general: int = None
    # objetivo_estrategico: str = None
    # estrategia: str = None
    # responsable: str = None
    # programa_asociado: str = None
    # ate: str = None
    # tic: str = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "dimension":
                "Gestión Pedagógica",
                "objetivo_estrategico":
                "Implementar la reflexión y análisis de prácticas y resultados en función de metas, a partir de un trabajo colaborativo que promuevan una cultura de equipo (por ejemplo con sesiones entre docentes para ver focos y hallazgos en observación de clases, reuniones entre especialistas PIE) de manera tal de promover el desarrollo profesional de cada integrante de la comunidad educativa.",
                "estrategia":
                "Colaboración entre docentes y capacitación/perfeccionamiento para incorporar herramientas digitales en propuestas de enseñanza y aprendizaje.",
                "subdimensiones": [
                    "Gestión Curricular", "Enseñanza y aprendizaje en el aula",
                    "Apoyo al desarrollo de los estudiantes"
                ],
                "nombre_accion":
                "refuerzo escolar",
                "descripcion":
                "Reforzamiento escolar a estudiantes , con la finalidad de mejorar los niveles de aprendizaje, asegurando los resultados y continuidad escolar",
                "fecha_inicio":
                "2022-03-14",
                "fecha_termino":
                "2022-11-30",
                "programa_asociado":
                "SEP",
                "responsable":
                "Jefe técnico",
                "recursos_necesarios_ejecucion":
                "Asignación de horas Asistentes de aula, horas docentes, resmas de papel, fotocopias, recursos de aprendizajes, útiles escolares, colaciones, material didáctico, impresora, tv o monitor de proyección",
                "ate":
                "No",
                "tic":
                "Sala de clases",
                "planes": 
                    "Plan de Gestión de la Convivencia Escolar, Plan de Apoyo a la Inclusión"
                ,
                "medio_de_verificacion":
                "informe de evaluación de impacto, Planificación y registro de las actividades de reforzamiento,     Registro de asistencia a talleres de reforzamiento",
                "monto_subvencion_general":
                0,
                "monto_sep":
                10000000,
                "monto_total":
                1000000000,
                "id_pme":
                "id_pme",
            }
        }


class Schema_Acciones_Update(BaseModel):
    dimension: str = None
    subdimensiones: List[str] = None
    nombre_accion: str = None
    descripcion: str = None
    fecha_inicio: str = None
    fecha_termino: str = None
    recursos_necesarios_ejecucion: str = None
    planes: str = None
    monto_sep: str = None
    monto_total: str = None
    id_pme: str = None
    fecha_actualizacion: datetime = None
    id_pme: str = None