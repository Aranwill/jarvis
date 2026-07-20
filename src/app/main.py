"""
Punto de entrada de Malāk.
Versión: 0.6.0-alpha
"""
from pathlib import Path
import sys

# Configuración de rutas base
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from malak.shared.logger import logger
# Importamos el nuevo gestor de configuración agnóstico
from malak.kernel.config.manager import config_manager

def main():
    """
    Inicia la aplicación validando primero la infraestructura base.
    """
    try:
        # Validación temprana (Fail-fast)
        cfg = config_manager.current
        logger.info(f"--- Configuración Cargada ---")
        logger.info(f"Tipo de Runtime: {cfg.runtime_type}")
        logger.info(f"ID del Modelo: {cfg.model_id}")
        logger.info(f"Endpoint Servicio: {cfg.service_endpoint}")
        logger.info(f"-----------------------------")

    except ValueError as e:
        # Si la configuración falla, el sistema se detiene antes de intentar 
        # conectar con modelos o iniciar servicios que no están configurados.
        logger.critical(f"ERROR CRÍTICO DE INICIALIZACIÓN: {e}")
        sys.exit(1)

    logger.info("========================================")
    logger.info("Iniciando Malāk...")
    logger.info("========================================")

    # Aquí se integraría el resto del flujo de inicialización (Kernel, etc.)
    # ya que ahora todos los componentes pueden importar 'config_manager' 
    # en lugar de usar os.getenv() directamente.

if __name__ == "__main__":
    main()