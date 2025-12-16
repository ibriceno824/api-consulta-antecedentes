import csv
from datetime import datetime
import json
import os
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

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
    Retorna True si están válidas, False si han expirado o no existen.
    """
    if not os.path.exists(path):
        print("⚠️ El archivo de cookies no existe.")
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        
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

    except Exception as e:
        print(f"❌ Error al verificar cookies: {e}")
        return False
    
def cookies_aun_sirven(driver):
    """
    Verifica si las cookies cargadas permiten acceder al formulario.
    Recarga la página, cierra modales y busca el campo de cédula.
    """
    driver.get("https://certificados.ministeriodelinterior.gob.ec/gestorcertificados/antecedentes/")
    time.sleep(5)  # Esperar más tiempo para que la página cargue completamente

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
                time.sleep(2)  # Esperar después de cerrar modal
                break
    except:
        pass  # Si no hay modal, continuar

    # Buscar el campo de cédula con varios intentos
    max_intentos = 3
    for intento in range(max_intentos):
        try:
            elemento = driver.find_element(By.ID, "txtCi")
            if elemento.is_displayed():
                print("✅ Campo de cédula detectado. Cookies válidas.")
                return True
        except:
            if intento < max_intentos - 1:
                print(f"⏳ Esperando campo de cédula... (intento {intento + 1}/{max_intentos})")
                time.sleep(2)
            else:
                print("❌ No se encontró el campo de cédula después de varios intentos.")
                return False
    
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