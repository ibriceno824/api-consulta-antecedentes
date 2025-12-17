"""
Utilidades para manejar cookies desde variable de entorno (base64) o archivo.
"""
import os
import json
import base64
import time


def obtener_cookies_desde_env_o_archivo(path_default="cookies.json"):
    """
    Obtiene cookies desde variable de entorno COOKIES_BASE64 (codificadas en base64)
    o desde un archivo si la variable no está definida.
    
    Args:
        path_default: Ruta al archivo de cookies por defecto
        
    Returns:
        list: Lista de cookies (dict)
        
    Raises:
        FileNotFoundError: Si no hay variable de entorno ni archivo
        ValueError: Si las cookies en base64 son inválidas
    """
    # Intentar leer desde variable de entorno primero
    cookies_base64 = os.getenv("COOKIES_BASE64")
    
    if cookies_base64:
        try:
            # Decodificar base64
            cookies_json = base64.b64decode(cookies_base64).decode('utf-8')
            cookies = json.loads(cookies_json)
            print("🍪 Cookies cargadas desde variable de entorno COOKIES_BASE64")
            return cookies
        except Exception as e:
            raise ValueError(f"❌ Error al decodificar cookies desde COOKIES_BASE64: {e}")
    
    # Si no hay variable de entorno, intentar leer desde archivo
    if os.path.exists(path_default):
        try:
            with open(path_default, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            print(f"🍪 Cookies cargadas desde archivo: {path_default}")
            return cookies
        except Exception as e:
            raise ValueError(f"❌ Error al leer cookies desde archivo {path_default}: {e}")
    
    # Si no hay ni variable ni archivo
    raise FileNotFoundError(
        f"❌ No se encontraron cookies. "
        f"Define la variable de entorno COOKIES_BASE64 o crea el archivo {path_default}"
    )


def filtrar_cookies_expiradas(cookies):
    """
    Filtra las cookies expiradas y retorna solo las válidas.
    
    Args:
        cookies: Lista de cookies (dict)
        
    Returns:
        tuple: (cookies_validas, cookies_expiradas)
    """
    ahora = int(time.time())
    cookies_validas = []
    cookies_expiradas = []
    
    for cookie in cookies:
        if "expiry" in cookie:
            if cookie["expiry"] < ahora:
                cookies_expiradas.append(cookie["name"])
                continue  # Saltar esta cookie expirada
        # Cookie válida (sin expiry o expiry futuro)
        cookies_validas.append(cookie)
    
    return cookies_validas, cookies_expiradas


def guardar_cookies_a_archivo(cookies, path="cookies.json"):
    """
    Guarda cookies a un archivo JSON.
    
    Args:
        cookies: Lista de cookies (dict)
        path: Ruta donde guardar el archivo
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=4, ensure_ascii=False)
        print(f"🍪 Cookies guardadas en: {path}")
    except Exception as e:
        raise ValueError(f"❌ Error al guardar cookies en {path}: {e}")

