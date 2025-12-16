from fastapi import HTTPException
from core.consulta_core import consultar_antecedentes
from core.utils import guardar_log_csv, validar_cedula_ecuatoriana, log_descarga_certificado

def procesar_consulta(cedula: str, motivo: str):

    if not validar_cedula_ecuatoriana(cedula):
        raise HTTPException(status_code=422, detail="La cédula ingresada no es válida según el Registro Civil.")

    if not motivo or len(motivo.strip()) < 10:
        raise HTTPException(status_code=422, detail="El motivo debe tener al menos 10 caracteres.")

    try:

        resultado = consultar_antecedentes(cedula, motivo)


        guardar_log_csv(cedula, motivo, resultado, exito=True)


        if isinstance(resultado, dict):
            certificado_ok = resultado.get("certificado_exitoso", False)
            mensaje_cert = resultado.get("mensaje_certificado", "")
        else:
            certificado_ok = True
            mensaje_cert = ""

        log_descarga_certificado(exito=certificado_ok, mensaje=mensaje_cert)

        return resultado

    except Exception as e:
        guardar_log_csv(cedula, motivo, str(e), exito=False)
        log_descarga_certificado(exito=False, mensaje=f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
