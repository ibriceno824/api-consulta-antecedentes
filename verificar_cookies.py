#!/usr/bin/env python3
"""
Script para verificar el estado y expiración de las cookies
"""
import json
import os
import time
from datetime import datetime

def verificar_cookies(path="cookies.json"):
    """Verifica y muestra información detallada sobre las cookies"""
    
    if not os.path.exists(path):
        print("❌ El archivo cookies.json no existe.")
        return
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        
        ahora = int(time.time())
        fecha_ahora = datetime.fromtimestamp(ahora)
        
        print("=" * 60)
        print("ANALISIS DE COOKIES")
        print("=" * 60)
        print(f"Fecha actual: {fecha_ahora.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total de cookies: {len(cookies)}\n")
        
        cookies_expiradas = []
        cookies_activas = []
        cookies_sesion = []
        
        for cookie in cookies:
            nombre = cookie.get("name", "Sin nombre")
            dominio = cookie.get("domain", "Sin dominio")
            
            if "expiry" in cookie:
                expiry_timestamp = cookie["expiry"]
                fecha_expiracion = datetime.fromtimestamp(expiry_timestamp)
                segundos_restantes = expiry_timestamp - ahora
                dias_restantes = segundos_restantes / 86400
                horas_restantes = (segundos_restantes % 86400) / 3600
                
                if expiry_timestamp < ahora:
                    estado = "[EXPIRADA]"
                    cookies_expiradas.append(nombre)
                else:
                    estado = "[ACTIVA]"
                    cookies_activas.append(nombre)
                
                print(f"{estado} | {nombre}")
                print(f"   Dominio: {dominio}")
                print(f"   Expira: {fecha_expiracion.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Tiempo restante: {int(dias_restantes)} días, {int(horas_restantes)} horas")
                print()
            else:
                estado = "[SESION]"
                cookies_sesion.append(nombre)
                print(f"{estado} | {nombre}")
                print(f"   Dominio: {dominio}")
                print(f"   Expira: Cuando se cierre el navegador (cookie de sesion)")
                print()
        
        # Resumen
        print("=" * 60)
        print("RESUMEN")
        print("=" * 60)
        print(f"[OK] Cookies activas: {len(cookies_activas)}")
        if cookies_activas:
            print(f"   {', '.join(cookies_activas)}")
        
        print(f"\n[EXPIRADAS] Cookies expiradas: {len(cookies_expiradas)}")
        if cookies_expiradas:
            print(f"   {', '.join(cookies_expiradas)}")
        
        print(f"\n[SESION] Cookies de sesion: {len(cookies_sesion)}")
        if cookies_sesion:
            print(f"   {', '.join(cookies_sesion)}")
        
        print("\n" + "=" * 60)
        
        # Determinar cookie más crítica (la que expira primero)
        cookies_con_expiry = [c for c in cookies if "expiry" in c and c["expiry"] > ahora]
        if cookies_con_expiry:
            cookie_mas_critica = min(cookies_con_expiry, key=lambda x: x["expiry"])
            fecha_critica = datetime.fromtimestamp(cookie_mas_critica["expiry"])
            dias_criticos = (cookie_mas_critica["expiry"] - ahora) / 86400
            
            print(f"[CRITICA] Cookie que expira primero:")
            print(f"   Nombre: {cookie_mas_critica['name']}")
            print(f"   Fecha: {fecha_critica.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Dias restantes: {int(dias_criticos)} dias")
            print("=" * 60)
        
        # Verificación final
        if cookies_expiradas:
            print("\n[ADVERTENCIA] Hay cookies expiradas.")
            print("   Ejecuta: python core/cookies.py")
            print("   Para regenerar las cookies.")
        elif len(cookies_activas) > 0:
            print("\n[OK] Todas las cookies estan activas y validas.")
            print("   El sistema automatico las renovara cada 3 horas.")
        else:
            print("\n[ADVERTENCIA] Solo hay cookies de sesion.")
            print("   Considera regenerar cookies con expiracion.")
        
    except Exception as e:
        print(f"[ERROR] Error al leer cookies: {e}")

if __name__ == "__main__":
    verificar_cookies()

