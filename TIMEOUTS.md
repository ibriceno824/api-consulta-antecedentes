# ⏱️ Resumen de Timeouts Configurados (OPTIMIZADOS)

## 📊 Timeouts en `consulta_core.py` (OPTIMIZADOS)

### 1. Carga inicial de página raíz
- **Línea 29**: `WebDriverWait(3)` - Espera inteligente que la página esté lista (reemplazó `time.sleep(2)`)

### 2. Carga de página principal
- **Línea 37**: `WebDriverWait(3)` - Espera inteligente que la página cargue (reemplazó `time.sleep(5)`, reducido de 5 a 3 segundos)

### 3. Espera de campo de motivo
- **Línea 101**: `timeout=25` - Espera para campo de motivo (OPTIMIZADO: reducido de 35 a 25 segundos)
- **Línea 111**: `time.sleep(1)` - Después de reintentar click (OPTIMIZADO: reducido de 2 a 1 segundo)

### 4. Espera de resultado
- **Línea 131**: `WebDriverWait(8)` - Espera inteligente del resultado (reemplazó `time.sleep(7)`, ahora espera hasta que aparezca)

## 📊 Timeouts en `utils.py` (cookies_aun_sirven) (OPTIMIZADOS)

### 1. Carga de página
- **Línea 94**: `WebDriverWait(3)` - Espera inteligente que la página cargue (OPTIMIZADO: reemplazó `time.sleep(5)`, reducido de 5 a 3 segundos)

### 2. Cierre de modal
- **Línea 112**: `time.sleep(1)` - Después de cerrar modal (OPTIMIZADO: reducido de 2 a 1 segundo)

### 3. Búsqueda de campo
- **Línea 119**: `WebDriverWait(8)` - Espera inteligente del campo de cédula (OPTIMIZADO: reemplazó múltiples intentos con `time.sleep(2)`, ahora espera hasta que aparezca)

## 📊 Timeouts en `navegador.py` (OPTIMIZADOS)

### 1. Espera de elementos
- **Línea 84**: `timeout=15` (por defecto) - Espera de elementos visibles
- **Línea 90**: `timeout=15` (por defecto) - Espera de botones

### 2. Después de clicks
- **Línea 99**: `time.sleep(0.5)` - Después de hacer click en botón (OPTIMIZADO: reducido de 1 a 0.5 segundos)

## 📊 Timeouts en `sesion.py` (renovación automática)

### 1. Ping de sesión
- **Línea 38**: `time.sleep(2)` - Después de cargar página
- **Línea 56**: `time.sleep(3)` - Después de cargar cookies
- **Línea 63**: `timeout=10` - Espera de campo txtCi
- **Línea 109**: `time.sleep(2)` - Después de cargar página en ping
- **Línea 125**: `time.sleep(3)` - Después de cargar cookies en ping
- **Línea 126**: `timeout=8` - Espera de campo txtCi en ping

## 📊 Timeouts en `certificado_core.py`

- **Línea 14**: `time.sleep(2)` - Después de cargar página
- **Línea 19**: `time.sleep(2)` - Después de click en link
- **Línea 29**: `time.sleep(2)` - Después de enviar cédula
- **Línea 33**: `time.sleep(2)` - Después de cargar página validación
- **Línea 51**: `time.sleep(4)` - Después de enviar fecha
- **Línea 62**: `timeout=20` - Espera de descarga de PDF

## 📊 Timeouts en `utils.py` (esperar_descarga)

- **Línea 150**: `timeout=8` (por defecto) - Espera de descarga de archivo
- **Línea 169**: `time.sleep(1)` - Entre verificaciones de descarga

## 📊 Timeouts en `utils.py` (verificar_advertencia)

- **Línea 175**: `delay=1.5` (por defecto) - Espera antes de verificar advertencia

## 📊 Resumen Total (OPTIMIZADO)

### Optimizaciones realizadas:

1. ✅ **Reemplazado `time.sleep(2)`** por `WebDriverWait(3)` - Espera inteligente en carga inicial
2. ✅ **Reemplazado `time.sleep(5)`** por `WebDriverWait(3)` - Reducción de 5 a 3 segundos en carga principal
3. ✅ **Reducido `timeout=35` a `timeout=25`** - Campo de motivo (ahorra hasta 10 segundos)
4. ✅ **Reducido `time.sleep(2)` a `time.sleep(1)`** - Después de cerrar modal y reintentos
5. ✅ **Reemplazado múltiples `time.sleep(2)`** por `WebDriverWait(8)` - Búsqueda de campo más eficiente
6. ✅ **Reemplazado `time.sleep(7)`** por `WebDriverWait(8)` - Espera inteligente del resultado
7. ✅ **Reducido `time.sleep(1)` a `time.sleep(0.5)`** - Después de clicks

### Mejoras de rendimiento:

- **WebDriverWait** reemplaza sleeps fijos: espera hasta que el elemento aparezca (más rápido cuando la página carga rápido)
- **Reducción de tiempos fijos**: ~15-20 segundos menos en casos normales
- **Mejor eficiencia**: Los elementos que aparecen rápido no esperan tiempos innecesarios
- **Mantiene confiabilidad**: Los timeouts máximos siguen siendo suficientes para casos lentos

### Tiempo estimado por consulta (optimizado):
- Carga inicial: ~1-3 segundos (antes: 2 segundos fijos)
- Carga página principal: ~1-3 segundos (antes: 5 segundos fijos)
- Validación cookies: ~1-3 segundos (antes: 5 segundos fijos)
- Campo de motivo: hasta 25 segundos (antes: hasta 35 segundos)
- Espera resultado: hasta 8 segundos (antes: 7 segundos fijos)
- **Total aproximado: ~5-15 segundos menos en casos normales**

## 🎯 Objetivo de los timeouts

Los timeouts adicionales fueron agregados para:
1. **Evitar detección de Cloudflare** - Dar más tiempo para que la página cargue completamente
2. **Manejar sitios lentos** - El sitio puede tardar en responder
3. **Permitir que JavaScript ejecute** - Dar tiempo para que los elementos aparezcan dinámicamente
4. **Simular comportamiento humano** - Evitar acciones demasiado rápidas

