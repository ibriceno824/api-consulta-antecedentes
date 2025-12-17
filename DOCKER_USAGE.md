# 🐳 Guía de Uso con Dockerfile (Sin Docker Compose)

Esta guía explica cómo construir y ejecutar el contenedor usando solo Dockerfile, sin necesidad de docker-compose.

## 📋 Requisitos Previos

- Docker instalado y funcionando
- Cookies configuradas (ver opciones abajo):
  - **Opción A**: Variable de entorno `COOKIES_BASE64` (recomendado)
  - **Opción B**: Archivo `cookies.json` generado (ver README.md)

## 🔨 Construcción de la Imagen

### Construir la imagen Docker:

```bash
docker build -t consulta-antecedentes-api .
```

Esto creará una imagen llamada `consulta-antecedentes-api`.

## 🚀 Ejecutar el Contenedor

### Opción 1: Ejecución básica (sin persistencia)

```bash
docker run -d \
  --name consulta-api \
  -p 8000:8000 \
  consulta-antecedentes-api
```

### Opción 2: Con variable de entorno COOKIES_BASE64 (RECOMENDADO para producción)

Primero, codifica tus cookies a base64:
```bash
python scripts/codificar_cookies.py cookies.json
```

Luego ejecuta el contenedor:
```bash
docker run -d \
  --name consulta-api \
  -p 8000:8000 \
  -e COOKIES_BASE64='<valor_base64_aquí>' \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/capturas:/app/capturas" \
  -v "$(pwd)/html:/app/html" \
  --restart unless-stopped \
  consulta-antecedentes-api
```

### Opción 3: Con persistencia de datos (usando archivo cookies.json)

```bash
docker run -d \
  --name consulta-api \
  -p 8000:8000 \
  -v "$(pwd)/cookies.json:/app/cookies.json" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/capturas:/app/capturas" \
  -v "$(pwd)/html:/app/html" \
  --restart unless-stopped \
  consulta-antecedentes-api
```

**En Windows (PowerShell) - Con variable de entorno:**
```powershell
docker run -d `
  --name consulta-api `
  -p 8000:8000 `
  -e COOKIES_BASE64='<valor_base64_aquí>' `
  -v "${PWD}/logs:/app/logs" `
  -v "${PWD}/capturas:/app/capturas" `
  -v "${PWD}/html:/app/html" `
  --restart unless-stopped `
  consulta-antecedentes-api
```

**En Windows (PowerShell) - Con archivo:**
```powershell
docker run -d `
  --name consulta-api `
  -p 8000:8000 `
  -v "${PWD}/cookies.json:/app/cookies.json" `
  -v "${PWD}/logs:/app/logs" `
  -v "${PWD}/capturas:/app/capturas" `
  -v "${PWD}/html:/app/html" `
  --restart unless-stopped `
  consulta-antecedentes-api
```

**En Windows (CMD) - Con variable de entorno:**
```cmd
docker run -d ^
  --name consulta-api ^
  -p 8000:8000 ^
  -e COOKIES_BASE64=<valor_base64_aquí> ^
  -v "%CD%/logs:/app/logs" ^
  -v "%CD%/capturas:/app/capturas" ^
  -v "%CD%/html:/app/html" ^
  --restart unless-stopped ^
  consulta-antecedentes-api
```

**En Windows (CMD) - Con archivo:**
```cmd
docker run -d ^
  --name consulta-api ^
  -p 8000:8000 ^
  -v "%CD%/cookies.json:/app/cookies.json" ^
  -v "%CD%/logs:/app/logs" ^
  -v "%CD%/capturas:/app/capturas" ^
  -v "%CD%/html:/app/html" ^
  --restart unless-stopped ^
  consulta-antecedentes-api
```

## 📊 Verificar que está funcionando

### Ver logs del contenedor:

```bash
docker logs consulta-api
```

### Ver logs en tiempo real:

```bash
docker logs -f consulta-api
```

### Verificar salud del contenedor:

```bash
docker ps
```

### Acceder a la API:

- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc
- **Healthcheck**: http://localhost:8000/docs (debe responder 200)

## 🛠️ Comandos Útiles

### Detener el contenedor:

```bash
docker stop consulta-api
```

### Iniciar el contenedor:

```bash
docker start consulta-api
```

### Reiniciar el contenedor:

```bash
docker restart consulta-api
```

### Eliminar el contenedor:

```bash
docker rm -f consulta-api
```

### Eliminar la imagen:

```bash
docker rmi consulta-antecedentes-api
```

### Reconstruir la imagen (después de cambios):

```bash
docker build -t consulta-antecedentes-api .
docker rm -f consulta-api
docker run -d \
  --name consulta-api \
  -p 8000:8000 \
  -v "$(pwd)/cookies.json:/app/cookies.json" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/capturas:/app/capturas" \
  -v "$(pwd)/html:/app/html" \
  --restart unless-stopped \
  consulta-antecedentes-api
```

## 🔍 Solución de Problemas

### El contenedor se detiene inmediatamente:

```bash
docker logs consulta-api
```

Revisa los logs para ver el error.

### Las cookies no persisten:

Asegúrate de que el volumen esté montado correctamente:
```bash
docker inspect consulta-api | grep Mounts
```

### El puerto 8000 está ocupado:

Cambia el puerto en el comando run:
```bash
docker run -d --name consulta-api -p 8080:8000 consulta-antecedentes-api
```

Luego accede a http://localhost:8080/docs

### Regenerar cookies dentro del contenedor:

```bash
docker exec -it consulta-api python core/cookies.py
```

**Nota**: Esto requiere modo visual, así que puede no funcionar en contenedor headless. Mejor regenera cookies en tu máquina local y luego reinicia el contenedor.

## 📝 Notas Importantes

1. **Cookies**: 
   - **Opción A (Recomendado)**: Usa la variable de entorno `COOKIES_BASE64`. Obtén el valor ejecutando `python scripts/codificar_cookies.py cookies.json`
   - **Opción B**: El archivo `cookies.json` debe existir antes de ejecutar el contenedor. Si no existe, créalo ejecutando `python core/cookies.py` en tu máquina local.

2. **Persistencia**: Usa volúmenes (`-v`) para que los datos (cookies, logs, capturas) persistan después de reiniciar el contenedor.

3. **Restart Policy**: `--restart unless-stopped` hace que el contenedor se reinicie automáticamente si se detiene inesperadamente.

4. **Recursos**: Por defecto, Docker usa todos los recursos disponibles. Para limitar recursos, usa:
   ```bash
   docker run -d \
     --name consulta-api \
     --memory="2g" \
     --cpus="2" \
     -p 8000:8000 \
     consulta-antecedentes-api
   ```

5. **Modo Headless**: El contenedor ejecuta Chrome en modo headless automáticamente, no necesitas configuración adicional.

## 🎯 Ejemplo Completo de Despliegue

### Con Variable de Entorno (Recomendado):

```bash
# 1. Construir la imagen
docker build -t consulta-antecedentes-api .

# 2. Crear directorios necesarios (si no existen)
mkdir -p logs capturas html

# 3. Generar cookies (si no existen)
python core/cookies.py

# 4. Codificar cookies a base64
python scripts/codificar_cookies.py cookies.json
# Copia el valor de COOKIES_BASE64 que se muestra

# 5. Ejecutar el contenedor con variable de entorno
docker run -d \
  --name consulta-api \
  -p 8000:8000 \
  -e COOKIES_BASE64='<pega_el_valor_base64_aquí>' \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/capturas:/app/capturas" \
  -v "$(pwd)/html:/app/html" \
  --restart unless-stopped \
  consulta-antecedentes-api

# 6. Verificar que está funcionando
docker logs -f consulta-api

# 7. Acceder a la API
# Abre http://localhost:8000/docs en tu navegador
```

### Con Archivo cookies.json:

```bash
# 1. Construir la imagen
docker build -t consulta-antecedentes-api .

# 2. Crear directorios necesarios (si no existen)
mkdir -p logs capturas html

# 3. Generar cookies (si no existen)
python core/cookies.py

# 4. Ejecutar el contenedor con persistencia
docker run -d \
  --name consulta-api \
  -p 8000:8000 \
  -v "$(pwd)/cookies.json:/app/cookies.json" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/capturas:/app/capturas" \
  -v "$(pwd)/html:/app/html" \
  --restart unless-stopped \
  consulta-antecedentes-api

# 5. Verificar que está funcionando
docker logs -f consulta-api

# 6. Acceder a la API
# Abre http://localhost:8000/docs en tu navegador
```

## 📚 Más Información

Para más detalles sobre el uso de cookies con variable de entorno, consulta [COOKIES_ENV.md](COOKIES_ENV.md).

