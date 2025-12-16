import time
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://certificados.ministeriodelinterior.gob.ec/gestorcertificados/antecedentes/"

options = uc.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-blink-features=AutomationControlled')

# Deshabilitar proxy del sistema para evitar detección de Cloudflare
options.add_argument('--no-proxy-server')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')

driver = uc.Chrome(options=options)
driver.get(URL)

print("🔐 Paso 1: Resuelve manualmente el CAPTCHA si aparece.")
input("⏸️ Presiona ENTER cuando hayas terminado el CAPTCHA...\n")

print("🔐 Paso 2: Si aparece el modal de Políticas o Términos, acéptalo.")
input("⏸️ Presiona ENTER cuando veas el campo de cédula (id='txtCi')...\n")

formulario_visible = False
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "txtCi"))
    )
    print("🟢 Campo 'txtCi' detectado. Guardando cookies...")
    formulario_visible = True
except:
    print("⚠️ No se detectó el campo de cédula. Se guardarán las cookies igual por si acaso.")

# Guardar cookies, incluidas las de sesión
try:
    cookies = driver.get_cookies()
    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=4, ensure_ascii=False)
    print(f"🍪 Se guardaron {len(cookies)} cookies en 'cookies.json'.")
except Exception as e:
    print(f"❌ Error al guardar cookies: {e}")

# Captura de pantalla de respaldo
try:
    driver.save_screenshot("capturas/cookies_guardadas.png")
    print("📸 Captura guardada como 'cookies_guardadas.png'.")
except:
    print("⚠️ No se pudo guardar la captura.")

if formulario_visible:
    print("✅ Puedes cerrar el navegador. Cookies listas para automatización.")
else:
    print("ℹ️ Puede que debas repetir este paso si los datos no funcionan bien en la próxima sesión.")

driver.quit()
driver = None
