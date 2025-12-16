# 🐳 Guía de Despliegue con Docker

Esta guía explica cómo desplegar la API de Consulta de Antecedentes usando Docker.

## 📋 Requisitos Previos

- Docker instalado (versión 20.10 o superior)
- Docker Compose instalado (versión 1.29 o superior)
- Al menos 2GB de RAM disponible
- Al menos 5GB de espacio en disco

## 🚀 Despliegue Rápido

### Opción 1: Usando Docker Compose (Recomendado)

```bash
# Construir y levantar el contenedor
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener el contenedor
docker-compose down
```

### Opción 2: Usando Docker directamente

```bash
# Construir la imagen
docker build -t consulta-antecedentes-api .

# Ejecutar el contenedor
docker run -d \
  --name consulta-antecedentes \
  -p 8000:8000 \
  -v $(pwd)/cookies.json:/app/cookies.json \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/capturas:/app/capturas \
  -v $(pwd)/html:/app/html \
  --restart unless-stopped \
  consulta-antecedentes-api
```

## 🔧 Configuración Inicial

### 1. Generar Cookies Iniciales

**IMPORTANTE:** Antes de usar la API en producción, necesitas generar las cookies iniciales.

#### Opción A: Desde el contenedor (Recomendado para producción)

```bash
# Ejecutar el script de cookies dentro del contenedor
docker exec -it consulta-antecedentes-api python core/cookies.py
```

**Nota:** Esto abrirá Chrome en modo visual. Necesitarás:
- Acceso a X11 display (en Linux)
- O usar VNC/Xvfb para modo headless con display virtual

#### Opción B: Desde tu máquina local

```bash
# Generar cookies localmente
python core/cookies.py

# Copiar cookies al contenedor
docker cp cookies.json consulta-antecedentes-api:/app/cookies.json
```

### 2. Verificar que Funciona

```bash
# Verificar que la API está corriendo
curl http://localhost:8000/docs

# O abrir en navegador
# http://localhost:8000/docs
```

## 📁 Volúmenes Montados

Los siguientes directorios se montan como volúmenes para persistir datos:

- `cookies.json` - Cookies de sesión (CRÍTICO - no perder)
- `logs/` - Logs de la aplicación
- `capturas/` - Capturas de pantalla de debug
- `html/` - HTML de debug cuando hay errores

## 🔍 Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs del contenedor
docker logs -f consulta-antecedentes-api

# Ejecutar comandos dentro del contenedor
docker exec -it consulta-antecedentes-api bash

# Reiniciar el contenedor
docker-compose restart

# Ver estado del contenedor
docker-compose ps

# Ver uso de recursos
docker stats consulta-antecedentes-api
```

## 🛠️ Solución de Problemas

### Problema: Chrome no se inicia en el contenedor

**Solución:** El Dockerfile ya incluye todas las dependencias necesarias. Si persiste:

```bash
# Verificar que Chrome está instalado
docker exec -it consulta-antecedentes-api google-chrome --version

# Verificar permisos
docker exec -it consulta-antecedentes-api ls -la /app
```

### Problema: Cookies no persisten

**Solución:** Verifica que el volumen está montado correctamente:

```bash
# Verificar que cookies.json existe en el contenedor
docker exec -it consulta-antecedentes-api cat /app/cookies.json

# Verificar permisos
docker exec -it consulta-antecedentes-api ls -la /app/cookies.json
```

### Problema: Error 17 de Cloudflare

**Solución:** 
1. Regenera las cookies sin proxy
2. Verifica que no hay proxy configurado en el sistema
3. Espera 10-15 minutos si hay bloqueo temporal

### Problema: Puerto 8000 ya está en uso

**Solución:** Cambia el puerto en `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Cambiar 8001 por el puerto que prefieras
```

## 🔒 Consideraciones de Seguridad

1. **Cookies.json**: Contiene tokens de sesión. No compartas este archivo públicamente.

2. **Puerto**: Considera usar un reverse proxy (nginx, traefik) en producción.

3. **Recursos**: Ajusta los límites de CPU/RAM en `docker-compose.yml` según tus necesidades.

4. **Red**: Considera usar una red Docker personalizada para aislar el servicio.

## 📊 Monitoreo

### Ver logs de sesión automática

```bash
# Ver logs del sistema de renovación automática
docker exec -it consulta-antecedentes-api tail -f logs/sesion.log
```

### Ver logs de consultas

```bash
# Ver CSV de consultas
docker exec -it consulta-antecedentes-api cat logs/log_consultas.csv
```

## 🚀 Despliegue en Producción

### Con Docker Compose

```bash
# Modo producción (sin logs en consola)
docker-compose up -d

# Verificar que está corriendo
docker-compose ps
```

### Con Docker Swarm o Kubernetes

Ajusta el `docker-compose.yml` según las necesidades de tu orquestador.

## 📝 Notas Importantes

1. **Primera vez**: Siempre necesitas generar cookies manualmente la primera vez.

2. **Renovación automática**: El sistema renueva cookies automáticamente cada 3 horas.

3. **Persistencia**: Los volúmenes aseguran que las cookies y logs no se pierdan al reiniciar.

4. **Recursos**: Chrome consume bastante memoria. Asegúrate de tener al menos 2GB disponibles.

5. **Red**: El contenedor necesita acceso a internet para funcionar.

