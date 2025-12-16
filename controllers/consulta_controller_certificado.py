from fastapi import HTTPException
from core.certificado_core import consultar_certificado_iess
from core.utils import guardar_log_csv, validar_cedula_ecuatoriana, log_descarga_certificado
from datetime import datetime

def procesar_consulta_cert(cedula: str, fecha_nacimiento: str):
    if not validar_cedula_ecuatoriana(cedula):
        raise HTTPException(status_code=422, detail="La cédula ingresada no es válida según el Registro Civil.")

    try:
        datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=422, detail="Fecha inválida (use YYYY-MM-DD).")

    try:
        resultado = consultar_certificado_iess(cedula, fecha_nacimiento)

        # resultado debe ser dict con keys certificado_exitoso, mensaje_certificado, ruta_pdf
        guardar_log_csv(cedula, "certificado IESS", resultado, exito=resultado.get("certificado_exitoso", False))

        log_descarga_certificado(
            exito=resultado.get("certificado_exitoso", False),
            mensaje=resultado.get("mensaje_certificado", "")
        )

        return resultado

    except Exception as e:
        guardar_log_csv(cedula, "certificado IESS", str(e), exito=False)
        log_descarga_certificado(exito=False, mensaje=f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
