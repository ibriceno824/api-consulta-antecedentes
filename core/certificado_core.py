import time
from selenium.webdriver.common.by import By
from core.navegador import inicializar_driver
from core.utils import esperar_descarga, verificar_advertencia


def consultar_certificado_iess(cedula: str, fecha_nacimiento: str):

    driver = inicializar_driver(headless=True)

    try:

        driver.get("https://www.iess.gob.ec/afiliado-web/pages/opcionesGenerales/seleccionCertificadoDeAfiliacion.jsf")
        time.sleep(2)


        link = driver.find_element(By.XPATH, "//a[contains(text(), 'Certificado de Afiliación')]")
        link.click()
        time.sleep(2)


        input_ced = driver.find_element(By.NAME, "frmCertificadoAfiliacion:j_id10")
        input_ced.clear()
        input_ced.send_keys(cedula)


        boton = driver.find_element(By.NAME, "frmCertificadoAfiliacion:j_id12")
        boton.click()
        time.sleep(2)

  
        driver.get("https://www.iess.gob.ec/afiliado-web/pages/opcionesGenerales/validarUsuarioSinAportes.jsf")
        time.sleep(2)

        ced_val = driver.find_element(By.NAME, "frmCertificadoAfiliacion:j_id9").get_attribute("value")

        if ced_val != cedula:
            return {
                "certificado_exitoso": False,
                "mensaje_certificado": "La cédula mostrada en el IESS no coincide.",
                "ruta_pdf": None
            }

        input_fecha = driver.find_element(By.NAME, "frmCertificadoAfiliacion:j_id13")
        input_fecha.clear()
        input_fecha.send_keys(fecha_nacimiento)

   
        boton_ing = driver.find_element(By.NAME, "frmCertificadoAfiliacion:j_id15")
        boton_ing.click()
        time.sleep(4)

        advertencia = verificar_advertencia(driver)

        if advertencia:
            return {
                "certificado_exitoso": False,
                "mensaje_certificado": advertencia,
                "ruta_pdf": None
            }

        ruta_pdf = esperar_descarga(".pdf", timeout=20)

        if ruta_pdf:
            return {
                "certificado_exitoso": True,
                "mensaje_certificado": "Certificado generado correctamente.",
                "ruta_pdf": ruta_pdf
            }

        return {
            "certificado_exitoso": False,
            "mensaje_certificado": "No se descargó ningún PDF.",
            "ruta_pdf": None
        }

    except Exception as e:
        return {
            "certificado_exitoso": False,
            "mensaje_certificado": f"Error interno: {str(e)}",
            "ruta_pdf": None
        }

    finally:
        try:
            driver.quit()
        except:
            pass


        # EL PFF SE COLOCA EN DESCARGAS, EN CASO DE REQUERIR RUTA USAR ESTO
        #carpeta_descargas = os.path.abspath("proyecto/certificados")
        #os.makedirs(carpeta_descargas, exist_ok=True)

        #archivos = sorted(
        #    [f for f in os.listdir(carpeta_descargas) if f.endswith(".pdf")],
        #    key=lambda x: os.path.getctime(os.path.join(carpeta_descargas, x)),
        #    reverse=True
        #)

        #if archivos:
        #    return os.path.join(carpeta_descargas, archivos[0])

        #return None

