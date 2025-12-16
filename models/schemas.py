from pydantic import BaseModel, constr, validator
from datetime import datetime
from typing import Optional

class ConsultaAntecedentesInput(BaseModel):
    cedula: constr(min_length=10, max_length=10, pattern=r'^\d+$')
    motivo: constr(min_length=10)

class ConsultaCertificadoInput(BaseModel):
    cedula: constr(min_length=10, max_length=10, pattern=r'^\d+$')
    fecha_nacimiento: constr(pattern=r'^\d{4}-\d{2}-\d{2}$')

    @validator("fecha_nacimiento")
    def validar_fecha(cls, v):
        datetime.strptime(v, "%Y-%m-%d")
        return v

class ConsultaInput(BaseModel):
    cedula: constr(min_length=10, max_length=10, pattern=r'^\d+$')
    motivo: Optional[constr(min_length=10)] = None
    fecha_nacimiento: Optional[constr(pattern=r'^\d{4}-\d{2}-\d{2}$')] = None

    @validator("fecha_nacimiento")
    def validar_fecha_opcional(cls, v):
        if v:
            datetime.strptime(v, "%Y-%m-%d")
        return v


class Resultado(BaseModel):
    cedula: str
    antecedentes: Optional[str] = None
    certificado_pdf: Optional[str] = None
    estado_certificado: Optional[str] = None

    model_config = {
        "json_encoders": {
            str: lambda v: v
        },
        "extra": "ignore",
        "from_attributes": True,   # reemplaza a orm_mode
    }
