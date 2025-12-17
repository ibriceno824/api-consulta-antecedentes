import time
import traceback
from core.navegador import (
    inicializar_driver, cargar_cookies,
    cerrar_modal, esperar_elemento,
    click_boton_por_texto
)
from core.utils import verificar_expiracion_cookies, cookies_aun_sirven
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def consultar_antecedentes(cedula: str, motivo: str):

    if not cedula.isdigit() or len(cedula) != 10:
        raise ValueError("❌ La cédula ingresada no es válida. Debe contener exactamente 10 dígitos numéricos.")

    if not verificar_expiracion_cookies():
        print("🚫 Las cookies han expirado o no existen.")
        print("📢 Por favor, vuelve a generarlas para evitar bloqueos por IP.")
        raise RuntimeError("Cookies caducadas. Regenera antes de continuar.")

    driver = inicializar_driver(headless=True)
    try:
        print("🌐 Cargando sitio web...")
        
        # IMPORTANTE: Cargar cookies ANTES del primer GET, igual que en cookies.py
        # Primero navegar a cualquier página del dominio para establecer el contexto
        driver.get("https://certificados.ministeriodelinterior.gob.ec/")
        # Esperar que la página esté lista (más rápido que sleep fijo)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Cargar cookies ANTES de ir a la página principal
        print("🔄 Cargando cookies ANTES de acceder a la página principal...")
        cargar_cookies(driver)
        
        # Ahora sí, ir a la página principal CON las cookies ya cargadas
        driver.get("https://certificados.ministeriodelinterior.gob.ec/gestorcertificados/antecedentes/")
        # Esperar que la página cargue (reducido de 5 a 3 segundos, pero espera inteligente)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Verificar si hay bloqueo de Cloudflare
        page_source_lower = driver.page_source.lower()
        if "error 17" in page_source_lower or "incapsula" in page_source_lower or "access denied" in page_source_lower:
            import os
            os.makedirs("html", exist_ok=True)
            os.makedirs("capturas", exist_ok=True)
            driver.save_screenshot("capturas/cloudflare_bloqueo.png")
            with open("html/html_cloudflare_bloqueo.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            
            # Mensaje más claro con instrucciones
            mensaje_error = (
                "❌ Cloudflare bloqueó el acceso (Error 17).\n"
                "📋 Posibles causas:\n"
                "   1. Las cookies fueron generadas con proxy y están asociadas a esa IP\n"
                "   2. Hay un proxy/VPN activo que Cloudflare detecta\n"
                "   3. La IP está temporalmente bloqueada\n\n"
                "🔧 Solución:\n"
                "   Ejecuta: python core/cookies.py\n"
                "   Esto regenerará las cookies SIN proxy (ya configurado)"
            )
            raise RuntimeError(mensaje_error)

        if not cookies_aun_sirven(driver):
            # Guardar HTML para diagnóstico
            import os
            os.makedirs("html", exist_ok=True)
            os.makedirs("capturas", exist_ok=True)
            driver.save_screenshot("capturas/cookies_invalidas.png")
            with open("html/html_cookies_invalidas.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            raise RuntimeError("Las cookies parecen no ser válidas. Vuelve a generarlas.")

        # Validar CAPTCHA o redirección por sesión expirada
        if "captcha" in driver.page_source.lower() or "su sesión ha expirado" in driver.page_source.lower():
            driver.save_screenshot("capturas/captcha_detectado.png")
            with open("html/html_captcha.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            raise Exception("❌ CAPTCHA o sesión expirada detectada. Las cookies pueden haber caducado.")

        cerrar_modal(driver)

        print("⏳ Esperando campo de cédula...")
        try:
            esperar_elemento(driver, "txtCi")
        except Exception:
            driver.save_screenshot("capturas/cedula_no_aparece.png")
            with open("html/html_debug_cedula.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            raise Exception("❌ Campo de cédula no apareció. Posiblemente las cookies han vencido.")

        input_ci = driver.find_element(By.ID, "txtCi")
        input_ci.clear()
        input_ci.send_keys(cedula)

        click_boton_por_texto(driver, "Siguiente")

        max_reintentos = 3
        reintento = 0
        while reintento < max_reintentos:
            try:
                print(f"⏳ Esperando campo de motivo... (intento {reintento + 1})")
                esperar_elemento(driver, "txtMotivo", timeout=25)  # Reducido de 35 a 25 segundos
                break
            except:
                reintento += 1
                print("⚠️ Campo de motivo no apareció aún.")
                try:
                    boton = next(b for b in driver.find_elements(By.TAG_NAME, "button") if "siguiente" in b.text.lower())
                    if boton.is_displayed() and boton.is_enabled():
                        boton.click()
                        print("🔁 Reintentando click en 'Siguiente' (motivo)")
                        time.sleep(1)  # Reducido de 2 a 1 segundo
                    else:
                        print("❌ Botón 'Siguiente' no está disponible para nuevo clic.")
                except:
                    print("⚠️ No se pudo encontrar o hacer clic en el botón nuevamente.")
        else:
            driver.save_screenshot("capturas/motivo_no_aparece_reintentos.png")
            with open("html/html_debug_motivo.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            raise Exception("❌ No se cargó el campo de motivo después de varios intentos... Intentelo después de unos minutos, problemas en el servicio")

        input_motivo = driver.find_element(By.ID, "txtMotivo")
        input_motivo.clear()
        input_motivo.send_keys(motivo)

        max_reintentos = 3
        reintento = 0
        while reintento < max_reintentos:
            click_boton_por_texto(driver, "Siguiente")
            print(f"⌛ Esperando resultado... (intento {reintento + 1})")
            # Usar WebDriverWait en lugar de sleep fijo - más rápido cuando el elemento aparece antes
            try:
                WebDriverWait(driver, 8).until(
                    lambda d: d.find_element(By.ID, "hdAntecedent").get_attribute("value")
                )
                resultado = driver.find_element(By.ID, "hdAntecedent").get_attribute("value")
                if resultado:
                    print(f"📄 Resultado obtenido: {resultado}")
                    return resultado.strip()
            except:
                print("⚠️ Resultado no encontrado aún.")
            reintento += 1
            print("🔁 Reintentando enviar motivo y obtener resultado...")

        driver.save_screenshot("capturas/resultado_no_obtenido.png")
        with open("html/html_debug_resultado.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise Exception("❌ No se obtuvo resultado después de varios intentos.")

    except Exception as e:
        driver.save_screenshot("capturas/fallo_general.png")
        with open("html/html_error_general.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("❌ Error en ejecución:\n", traceback.format_exc())
        raise RuntimeError(f"❌ Error en consulta: {str(e)}")
    finally:
        driver.quit()
        driver = None
