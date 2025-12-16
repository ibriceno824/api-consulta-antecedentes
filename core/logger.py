import logging
import os

# Carpeta logs
os.makedirs("logs", exist_ok=True)

# Configurar logger
logger = logging.getLogger("sesion_logger")
logger.setLevel(logging.INFO)

# Formato del log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Archivo de log
file_handler = logging.FileHandler("logs/sesion.log", encoding="utf-8")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
