# API de Consulta de Antecedentes Penales 🇪🇨

Esta API permite automatizar la consulta de antecedentes penales desde el portal del Ministerio del Interior de Ecuador mediante `FastAPI` y `Selenium`, utilizando cookies de sesión para evitar bloqueos por CAPTCHA.


---
## 🚀 Funcionalidad

- Consulta automatizada de antecedentes penales.
- Automatización de navegación web con `Selenium` + `undetected_chromedriver`.
- Carga de cookies previamente guardadas para evitar CAPTCHA.
- Mantenimiento automático de sesión con un "ping" periódico.
- Descarga automática del certificado del IESS (PDF).
- Registro de consultas exitosas en un archivo `.csv`.
- Validación de expiración de cookies antes de cada consulta.
- Documentación interactiva con Swagger (`/docs`).


## 🚀 ¿Cómo funciona?

    1. **Carga inicial de cookies** (`core/cookies.py`):
   - Abre el sitio web, resuelves manualmente el CAPTCHA y aceptas el modal de términos.
        En el primer modal resulve:
            - No soy un robot
            - Acepta politicas 
        En el segundo modal resulve:
            - Acepta terminos y condiciones
   - Luego, las cookies activas se guardan para uso futuro.

    2. **Consulta automática**:
   - La API expone un endpoint `//consultar-antecedentes` donde puedes enviar una cédula, motivo.
   - Si las cookies son válidas, la consulta se ejecuta automáticamente en segundo plano con Selenium.

   - La API expone un endpoint `///consultar-certificado` donde puedes enviar una cédula, fecha de nacimiento.
   - Si la cédula y la fecha de nacimiento es validad, la consulta se ejecuta automáticamente en segundo plano con Selenium.

    3. **Mantenimiento de sesión**:
   - Al iniciar la API, se lanza un **hilo en segundo plano** que cada 10 minutos realiza un “ping” al sitio para mantener las cookies activas.
   - Esto evita que la sesión expire y reduce el riesgo de bloqueos.


---
## 🧰 Requisitos

- Python 3.10 o superior (preferentemente 3.10.11)
- Google Chrome (versión 108 o superior instalada)
- ChromeDriver compatible (colocado en `drivers/chromedriver.exe`)
- Sistema operativo Windows


---
## 📦 Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tuusuario/proyecto-antecedentes.git
cd proyecto-antecedentes

2. Crea y activa un entorno virtual:
python -m venv venv
venv\Scripts\activate

3. Instala las dependencias
pip install -r requirements.txt


---
📌Uso

1. Ejecuta cookies.py para abrir el navegador, resolver manualmente el CAPTCHA y guardar las cookies:
python core/cookies.py

2. Inicia la API:
uvicorn main:app --reload

3. Abre tu navegador en (Desde allí puedes usar Swagger para probar los endpoint):
http://127.0.0.1:8000/docs

4. Ejemplo de entrada JSON (colocar identificación valida)
{
  "cedula": "0926099532",
  "motivo": "Trámite legal"
}

{
  "cedula": "0926099532",
  "fecha_nacimiento": "1994-0656-10"
}


---
## 🚀 Estructura del Proyecto

proyecto/
├── core/
│   ├── cookies.py                                  # Generación manual de cookies
│   ├── consulta_core.py                            # Lógica de automatización antecedentes penales
│   ├── certificado_core.py                         # Lógica de automatización certificado iess
│   ├── navegador.py                                # Configuración del navegador
│   ├── utils.py                                    # Validaciones y logs
│   ├── sesion.py                                   # Ping de sesión en segundo plano
│   └── logger.py                                   # Logging en archivo
├── controllers/
│   └── consulta_controller.py                      # Controlador de lógica de API antecedentes penales
│   └── consulta_controller_certificado.py          # Controlador de lógica de API certificado iess
├── models/
│   └── schemas.py                                  # Esquemas de entrada/salida (Pydantic)
├── logs/                                           # Se genera automáticamente
├── capturas/                                       # Se genera automáticamente
├── html/                                           # Se genera automáticamente
├── main.py                                         # Punto de entrada de la API
└── requirements.txt                                # Dependencias


---
🧠 Notas importantes
El navegador corre en modo "headless" (sin interfaz gráfica) para las consultas automáticas.

El archivo cookies.json debe mantenerse actualizado. Si caducan, vuelve a ejecutar cookies.py.

El ping automático mantiene viva la sesión sin interrumpir las consultas. (Si se suspende o apaga la maquina, se corre el riesgo de cauducidad de cookies)


---
🔒 Recomendaciones
No compartas las cookies.json públicamente, contienen tokens de sesión.
Ejecuta el sistema en servidores confiables o en tu entorno local.
Si Chrome o Selenium actualizan, reinstala undetected_chromedriver.