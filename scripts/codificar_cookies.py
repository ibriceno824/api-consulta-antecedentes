#!/usr/bin/env python3
"""
Script para codificar cookies.json a base64 para usar como variable de entorno.
"""
import json
import base64
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def codificar_cookies_a_base64(archivo_cookies="cookies.json"):
    """
    Lee un archivo de cookies JSON y lo codifica a base64.
    
    Args:
        archivo_cookies: Ruta al archivo cookies.json
        
    Returns:
        str: String base64 codificado
    """
    if not os.path.exists(archivo_cookies):
        print(f"❌ Error: El archivo '{archivo_cookies}' no existe.")
        sys.exit(1)
    
    try:
        # Leer el archivo JSON
        with open(archivo_cookies, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        # Convertir a JSON string
        cookies_json = json.dumps(cookies, ensure_ascii=False)
        
        # Codificar a base64
        cookies_base64 = base64.b64encode(cookies_json.encode('utf-8')).decode('utf-8')
        
        return cookies_base64
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: El archivo '{archivo_cookies}' no es un JSON válido: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else "cookies.json"
    
    print("=" * 70)
    print("🔐 CODIFICADOR DE COOKIES A BASE64")
    print("=" * 70)
    print(f"📁 Archivo: {archivo}\n")
    
    try:
        base64_str = codificar_cookies_a_base64(archivo)
        
        print("✅ Cookies codificadas exitosamente!\n")
        print("=" * 70)
        print("📋 VARIABLE DE ENTORNO:")
        print("=" * 70)
        print(f"COOKIES_BASE64={base64_str}\n")
        print("=" * 70)
        print("📝 INSTRUCCIONES:")
        print("=" * 70)
        print("1. Copia el valor de COOKIES_BASE64 mostrado arriba")
        print("2. En Docker, úsalo así:")
        print("   docker run -e COOKIES_BASE64='<valor>' ...")
        print("3. O en docker-compose.yml:")
        print("   environment:")
        print("     - COOKIES_BASE64=<valor>")
        print("=" * 70)
        
    except SystemExit:
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

