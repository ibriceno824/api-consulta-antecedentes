import time
import json
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from core.cookies_utils import obtener_cookies_desde_env_o_archivo



def inicializar_driver(headless=True):
    options = uc.ChromeOptions()
    
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Deshabilitar proxy del sistema para evitar detección de Cloudflare
    # Múltiples opciones para asegurar que no use proxy
    options.add_argument('--no-proxy-server')
    options.add_argument('--proxy-server=direct://')
    options.add_argument('--proxy-bypass-list=*')
    # Forzar que no use configuración de proxy del sistema
    options.add_argument('--disable-extensions')
    # Deshabilitar detección automática de proxy
    options.add_argument('--no-first-run')
    options.add_argument('--disable-default-apps')
    
    # Preferencias para deshabilitar proxy
    prefs = {
        "profile.default_content_setting_values": {
            "notifications": 2
        },
        "profile.managed_default_content_settings": {
            "images": 1
        }
    }
    options.add_experimental_option("prefs", prefs)

    if headless:
        print("🕶️ Ejecutando en modo HEADLESS")
        options.add_argument('--headless=new')
    else:
        print("🖥️ Ejecutando en modo VISUAL")

    driver = uc.Chrome(options=options)
    return driver

def cargar_cookies(driver, path="cookies.json"):
    """
    Carga cookies desde variable de entorno COOKIES_BASE64 o desde archivo.
    """
    try:
        # Usar la función utilitaria que lee de variable de entorno o archivo
        cookies = obtener_cookies_desde_env_o_archivo(path)
        
        for cookie in cookies:
            cookie.pop('sameSite', None)
            cookie.pop('secure', None)
            cookie.pop('httpOnly', None)
            if 'domain' in cookie and 'ministeriodelinterior.gob.ec' not in cookie['domain']:
                continue
            driver.add_cookie(cookie)
        print("✅ Cookies cargadas al navegador.")
    except Exception as e:
        print(f"⚠️ No se pudieron cargar cookies: {e}")
        raise

def cerrar_modal(driver):
    try:
        print("🧩 Cerrando modal si existe...")
        botones = driver.find_elements(By.XPATH, '//button')
        for boton in botones:
            if boton.text.strip().lower() == "aceptar":
                boton.click()
                print("✅ Modal cerrado.")
                return
        print("ℹ️ Modal no estaba presente.")
    except Exception as e:
        print(f"⚠️ Error cerrando modal: {e}")
        driver.save_screenshot("error_modal.png")
        raise

def esperar_elemento(driver, id_elemento, timeout=15):
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, id_elemento))
    )
    print(f"✅ Elemento '{id_elemento}' está visible.")

def click_boton_por_texto(driver, texto_boton, timeout=15):
    print(f"🔍 Buscando botón: {texto_boton}")
    WebDriverWait(driver, timeout).until(
        lambda d: any(texto_boton.lower() in b.text.lower() for b in d.find_elements(By.TAG_NAME, "button"))
    )
    for boton in driver.find_elements(By.TAG_NAME, "button"):
        if texto_boton.lower() in boton.text.lower():
            boton.click()
            print(f"✅ Click en botón '{texto_boton}'")
            time.sleep(0.5)  # Reducido de 1 a 0.5 segundos
            return
    raise Exception(f"Botón con texto '{texto_boton}' no encontrado")
