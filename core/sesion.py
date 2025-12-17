import threading
import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.logger import logger
from core.cookies_utils import obtener_cookies_desde_env_o_archivo, guardar_cookies_a_archivo

URL = "https://certificados.ministeriodelinterior.gob.ec/gestorcertificados/antecedentes/"
PING_INTERVALO = 600          # Cada 10 minutos hace ping
RENOVACION_INTERVALO = 10800  # Cada 3 horas renueva cookies


def renovar_cookies():
    """Renueva las cookies usando las existentes como base."""
    logger.info("♻️ Iniciando proceso de renovación automática de cookies...")

    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless=new')
    
    # Deshabilitar proxy del sistema (igual que en navegador.py)
    options.add_argument('--no-proxy-server')
    options.add_argument('--proxy-server=direct://')
    options.add_argument('--proxy-bypass-list=*')

    driver = None
    try:
        driver = uc.Chrome(options=options)
        
        # Usar el mismo flujo exitoso: cargar cookies ANTES del primer GET
        logger.info("🌐 Estableciendo contexto del dominio...")
        driver.get("https://certificados.ministeriodelinterior.gob.ec/")
        time.sleep(2)
        
        # Cargar cookies existentes ANTES de ir a la página principal
        logger.info("🔄 Cargando cookies existentes...")
        cookies = obtener_cookies_desde_env_o_archivo("cookies.json")

        driver.delete_all_cookies()
        for cookie in cookies:
            cookie.pop("sameSite", None)
            cookie.pop("secure", None)
            cookie.pop("httpOnly", None)
            if 'domain' in cookie and 'ministeriodelinterior.gob.ec' not in cookie['domain']:
                continue
            driver.add_cookie(cookie)

        # Ahora ir a la página principal CON las cookies ya cargadas
        driver.get(URL)
        time.sleep(3)
        
        # Verificar si hay bloqueo de Cloudflare
        if "error 17" in driver.page_source.lower() or "incapsula" in driver.page_source.lower():
            logger.warning("⚠️ Cloudflare bloqueó durante renovación. Las cookies pueden haber expirado completamente.")
            return False

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtCi")))

        # Guardar cookies actualizadas
        nuevas = driver.get_cookies()
        guardar_cookies_a_archivo(nuevas, "cookies.json")
        logger.info(f"✅ Cookies renovadas automáticamente. Guardadas {len(nuevas)} nuevas cookies.")
        return True

    except Exception as e:
        logger.warning(f"⚠️ No se pudieron renovar las cookies automáticamente: {e}")
        logger.warning("💡 Ejecuta 'python core/cookies.py' manualmente si el problema persiste.")
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
            driver = None


def iniciar_ping_sesion():
    def mantener_sesion_activa():
        ultimo_renovado = time.time()

        while True:
            try:
                logger.info("🟢 Ejecutando ping de sesión para mantener cookies activas...")

                options = uc.ChromeOptions()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('--headless=new')
                
                # Deshabilitar proxy del sistema (igual que en navegador.py)
                options.add_argument('--no-proxy-server')
                options.add_argument('--proxy-server=direct://')
                options.add_argument('--proxy-bypass-list=*')

                driver = uc.Chrome(options=options)
                
                # Usar el mismo flujo exitoso: cargar cookies ANTES del primer GET
                driver.get("https://certificados.ministeriodelinterior.gob.ec/")
                time.sleep(2)

                cookies = obtener_cookies_desde_env_o_archivo("cookies.json")

                driver.delete_all_cookies()
                for cookie in cookies:
                    cookie.pop("sameSite", None)
                    cookie.pop("secure", None)
                    cookie.pop("httpOnly", None)
                    if 'domain' in cookie and 'ministeriodelinterior.gob.ec' not in cookie['domain']:
                        continue
                    driver.add_cookie(cookie)

                # Ir a la página principal CON las cookies ya cargadas
                driver.get(URL)
                time.sleep(3)
                WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.ID, "txtCi")))
                logger.info("✅ Ping exitoso. Las cookies siguen activas.")

            except Exception as e:
                logger.warning(f"⚠️ Ping fallido o sesión no activa: {e}")

            finally:
                try:
                    driver.quit()
                    driver = None
                except:
                    pass

            # Verificar si ya toca renovar cookies
            if time.time() - ultimo_renovado >= RENOVACION_INTERVALO:
                renovar_cookies()
                ultimo_renovado = time.time()

            time.sleep(PING_INTERVALO)

    hilo = threading.Thread(target=mantener_sesion_activa, daemon=True)
    hilo.start()
    logger.info("🚀 Hilo de ping de sesión iniciado con renovación automática cada 3 h.")
