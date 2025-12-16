from fastapi import FastAPI
from models.schemas import (
    ConsultaAntecedentesInput,
    ConsultaCertificadoInput,
    ConsultaInput,
    Resultado
)
from controllers.consulta_controller import procesar_consulta
from controllers.consulta_controller_certificado import procesar_consulta_cert
from core.sesion import iniciar_ping_sesion
import uvicorn

app = FastAPI(
    title="API Consulta de Antecedentes y Certificados",
    version="1.0"
)

# Iniciar sistema automático de mantenimiento de cookies al arrancar la API
@app.on_event("startup")
async def startup_event():
    print("🚀 Iniciando sistema automático de mantenimiento de cookies...")
    iniciar_ping_sesion()
    print("✅ Sistema automático activado. Las cookies se renovarán automáticamente cada 3 horas.")


@app.post("/consultar-antecedentes", response_model=Resultado, response_model_exclude_none=True)
def consultar_antecedentes(data: ConsultaAntecedentesInput):
    resultado = procesar_consulta(
        cedula=data.cedula,
        motivo=data.motivo
    )

    return Resultado(
        cedula=data.cedula,
        antecedentes=resultado
    )



@app.post("/consultar-certificado", response_model=Resultado, response_model_exclude_none=True)
def consultar_certificado(data: ConsultaCertificadoInput):

    resultado = procesar_consulta_cert(
        cedula=data.cedula,
        fecha_nacimiento=data.fecha_nacimiento
    )

    return Resultado(
        cedula=data.cedula,
        certificado_pdf=resultado.get("ruta_pdf"),
        estado_certificado=resultado.get("mensaje_certificado")
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)