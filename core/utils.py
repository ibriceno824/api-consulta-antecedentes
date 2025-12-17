import csv
from datetime import datetime
import json
import os
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from core.cookies_utils import obtener_cookies_desde_env_o_archivo

def guardar_log_csv(cedula: str, motivo: str, resultado: str, exito: bool, archivo="logs/log_consultas.csv"):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fila = [ahora, cedula, motivo, resultado, "Éxito" if exito else "Error"]
    try:
        existe = False
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                existe = True
        except FileNotFoundError:
            pass

        with open(archivo, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            if not existe:
                writer.writerow(["FechaHora", "Cédula", "Motivo", "Resultado", "Estado"])
            writer.writerow(fila)
        print("📝 Log guardado en CSV.")
    except Exception as e:
        print(f"⚠️ No se pudo guardar el log: {e}")

def validar_cedula_ecuatoriana(cedula: str) -> bool:
    if len(cedula) != 10 or not cedula.isdigit():
        return False

    digitos = list(map(int, cedula))
    provincia = int(cedula[:2])
    tercer_digito = digitos[2]

    if provincia < 1 or provincia > 24 or tercer_digito > 6:
        return False

    suma = 0
    for i in range(9):
        if i % 2 == 0:
            val = digitos[i] * 2
            if val > 9:
                val -= 9
        else:
            val = digitos[i]
        suma += val

    verificador = 10 - (suma % 10) if (suma % 10) != 0 else 0
    return verificador == digitos[9]

def verificar_expiracion_cookies(path="cookies.json"):
    """
    Verifica si las cookies existen y están vigentes.
    Lee desde variable de entorno COOKIES_BASE64 o desde archivo.
    Retorna True si están válidas, False si han expirado o no existen.
    """
    try:
        # Usar la función utilitaria que lee de variable de entorno o archivo
        cookies = obtener_cookies_desde_env_o_archivo(path)
        
        ahora = int(time.time())
        expiradas = []

        for cookie in cookies:
            if "expiry" in cookie and cookie["expiry"] < ahora:
                expiradas.append(cookie["name"])

        if expiradas:
            print(f"⏰ Cookies expiradas detectadas: {expiradas}")
            return False
        else:
            print("🟢 Cookies válidas y vigentes.")
            return True

    except FileNotFoundError:
        print("⚠️ No se encontraron cookies (ni en variable de entorno ni en archivo).")
        return False
    except Exception as e:
        print(f"❌ Error al verificar cookies: {e}")
        return False
    
def cookies_aun_sirven(driver):
    """
    Verifica si las cookies cargadas permiten acceder al formulario.
    Recarga la página, cierra modales y busca el campo de cédula.
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    driver.get("https://certificados.ministeriodelinterior.gob.ec/gestorcertificados/antecedentes/")
    # Esperar que la página cargue (reducido de 5 a 3 segundos, pero espera inteligente)
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Verificar si hay bloqueo de Cloudflare
    if "error 17" in driver.page_source.lower() or "incapsula" in driver.page_source.lower() or "access denied" in driver.page_source.lower():
        print("🚫 Cloudflare bloqueó el acceso (Error 17). El proxy está siendo detectado.")
        return False

    if "captcha" in driver.page_source.lower() or "su sesión ha expirado" in driver.page_source.lower():
        print("🚫 CAPTCHA o sesión expirada detectada.")
        return False

    # Intentar cerrar modal si existe antes de buscar el campo
    try:
        botones = driver.find_elements(By.XPATH, '//button')
        for boton in botones:
            if boton.text.strip().lower() == "aceptar":
                boton.click()
                print("✅ Modal cerrado durante validación de cookies.")
                time.sleep(1)  # Reducido de 2 a 1 segundo
                break
    except:
        pass  # Si no hay modal, continuar

    # Buscar el campo de cédula con WebDriverWait (más eficiente que múltiples intentos con sleep)
    try:
        WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located((By.ID, "txtCi"))
        )
        print("✅ Campo de cédula detectado. Cookies válidas.")
        return True
    except:
        print("❌ No se encontró el campo de cédula después de esperar.")
        return False


def log_descarga_certificado(exito: bool, mensaje: str = "", archivo="logs/log_consultas.csv"):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    estado = "Descarga exitosa" if exito else "Descarga fallida"

    try:
        existe = os.path.exists(archivo)

        with open(archivo, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            if not existe:
                writer.writerow(["FechaHora", "Cédula", "Motivo", "Resultado", "Estado"])

            writer.writerow([ahora, "-", "-", mensaje, estado])

    except Exception as e:
        print(f"Error escribiendo log_certificado: {e}")


def esperar_descarga(extension=".pdf", timeout=8):
    carpeta = os.path.join(os.path.expanduser("~"), "Downloads")
    tiempo_inicial = time.time()

    archivo_descargado = None

    while time.time() - tiempo_inicial < timeout:
        archivos = [
            f for f in os.listdir(carpeta)
            if f.endswith(extension) and not f.endswith(".crdownload")
        ]

        if archivos:
            archivo_descargado = max(
                archivos,
                key=lambda f: os.path.getctime(os.path.join(carpeta, f))
            )
            return os.path.join(carpeta, archivo_descargado)

        time.sleep(1)

    return None


def verificar_advertencia(driver, delay: float = 1.5):
    time.sleep(delay)
    try:
        advertencia = driver.find_element(By.CSS_SELECTOR, ".mensaje_advertencia")
        texto = advertencia.text.strip()
        if texto:
            return texto
    except NoSuchElementException:
        return None