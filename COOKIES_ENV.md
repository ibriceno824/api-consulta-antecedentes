# 🍪 Configuración de Cookies mediante Variable de Entorno

Este proyecto ahora soporta cargar cookies desde una variable de entorno codificada en base64, lo cual es ideal para despliegues en Docker sin necesidad de montar archivos.

## 📋 Opciones de Configuración

### Opción 1: Variable de Entorno (Recomendado para Docker)

Las cookies se pueden pasar como variable de entorno `COOKIES_BASE64` codificadas en base64.

### Opción 2: Archivo cookies.json (Fallback)

Si no se define la variable de entorno, el sistema intentará leer desde `cookies.json`.

## 🔧 Cómo Obtener el Valor Base64

### Paso 1: Generar cookies.json

Si aún no tienes cookies, ejecuta:

```bash
python core/cookies.py
```

### Paso 2: Codificar a Base64

Ejecuta el script de codificación:

```bash
python scripts/codificar_cookies.py cookies.json
```

Esto mostrará el valor de `COOKIES_BASE64` que debes usar.

## 🐳 Uso en Docker

### Ejemplo 1: Docker Run

```bash
docker run -d \
  --name consulta-api \
  -p 8000:8000 \
  -e COOKIES_BASE64='W3siZG9tYWluIjogImNlcnRpZmljYWRvcy5taW5pc3RlcmlvZGVsaW50ZXJpb3IuZ29iLmVjIi...' \
  consulta-antecedentes-api
```

### Ejemplo 2: Docker Compose

```yaml
version: "3.8"

services:
  api-antecedentes:
    build: .
    container_name: consulta-antecedentes-api
    ports:
      - "8000:8000"
    environment:
      - COOKIES_BASE64=W3siZG9tYWluIjogImNlcnRpZmljYWRvcy5taW5pc3RlcmlvZGVsaW50ZXJpb3IuZ29iLmVjIi...
    restart: unless-stopped
```

### Ejemplo 3: Archivo .env

Crea un archivo `.env`:

```env
COOKIES_BASE64=W3siZG9tYWluIjogImNlcnRpZmljYWRvcy5taW5pc3RlcmlvZGVsaW50ZXJpb3IuZ29iLmVjIi...
```

Y úsalo con docker-compose:

```bash
docker-compose --env-file .env up
```

## 🔄 Actualizar Cookies

Cuando necesites actualizar las cookies:

1. **Regenera cookies localmente:**
   ```bash
   python core/cookies.py
   ```

2. **Codifica a base64:**
   ```bash
   python scripts/codificar_cookies.py cookies.json
   ```

3. **Actualiza la variable de entorno** en tu sistema de despliegue (Docker, Kubernetes, etc.)

## 📝 Notas Importantes

- ✅ **Prioridad**: Si existe `COOKIES_BASE64`, se usa esa. Si no, se lee desde `cookies.json`.
- ✅ **Seguridad**: Las cookies en base64 siguen siendo sensibles. No las compartas públicamente.
- ✅ **Renovación**: El sistema automático de renovación guardará nuevas cookies en `cookies.json` si no hay variable de entorno.
- ✅ **Compatibilidad**: Si no defines la variable de entorno, el sistema funciona igual que antes con `cookies.json`.

## 🔍 Verificación

Para verificar que las cookies se están cargando correctamente, revisa los logs:

```bash
docker logs consulta-api
```

Deberías ver uno de estos mensajes:
- `🍪 Cookies cargadas desde variable de entorno COOKIES_BASE64`
- `🍪 Cookies cargadas desde archivo: cookies.json`

## 🛠️ Solución de Problemas

### Error: "No se encontraron cookies"

**Causa**: No hay variable de entorno ni archivo.

**Solución**: 
1. Define `COOKIES_BASE64` o
2. Crea `cookies.json` ejecutando `python core/cookies.py`

### Error: "Error al decodificar cookies desde COOKIES_BASE64"

**Causa**: El valor base64 es inválido o está corrupto.

**Solución**: 
1. Regenera el valor ejecutando `python scripts/codificar_cookies.py cookies.json`
2. Asegúrate de copiar el valor completo sin espacios adicionales

### Las cookies expiran frecuentemente

**Causa**: Las cookies pueden estar asociadas a una IP específica.

**Solución**: 
1. Regenera cookies desde la misma IP donde se ejecutará el contenedor
2. O usa el sistema automático de renovación (ya está activado)

