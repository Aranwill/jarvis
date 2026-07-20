"""
Malāk Config Manager
Gestiona la configuración del sistema de forma agnística al proveedor.
"""
import os
from dataclasses import dataclass
from typing import Optional
from malak.shared.logger import logger

@dataclass
class AppConfig:
    """Objeto inmutable que contiene la configuración validada por el Kernel."""
    runtime_type: str  # "mock", "local-llm", "remote-api" (agnóstico a proveedor)
    model_id: str       # Identificador del modelo seleccionado para este runtime
    service_endpoint: str  # Punto de acceso al servicio (URL base)
    log_level: str = "INFO"

class ConfigManager:
    """
    Gestiona la lógica de carga y validación de parámetros.
    Cumple con el principio de que el Kernel no debe conocer proveedores externos,
    solo capacidades necesarias para su ejecución.
    """
    def __init__(self):
        self._config: AppConfig = self._load_config()

    def _load_config(self) -> AppConfig:
        # 1. Determinar tipo de Runtime
        raw_runtime = os.getenv("MALAK_RUNTIME", "mock").lower()
        valid_runtimes = ["mock", "local-llm", "remote-api"]
        
        if raw_runtime not in valid_runtimes:
            logger.error(f"Runtime inválido detectado: '{raw_runtime}'. Debe ser uno de {valid_runtimes}")
            raise ValueError(f"Configuración fallida: MALAK_RUNTIME debe ser un tipo válido.")

        # 2. Obtener ID del Modelo (Independiente del provider)
        model_id = os.getenv("MALAK_MODEL_ID")
        if not model_id and raw_runtime != "mock":
            logger.warning(f"Advertencia: Runtime '{raw_runtime}' requiere un MALAK_MODEL_ID.")

        # 3. Obtener punto de acceso (Endpoint del servicio)
        service_endpoint = os.getenv("MALAK_SERVICE_ENDPOINT", "http://localhost:11434")

        return AppConfig(
            runtime_type=raw_runtime,
            model_id=model_id or "default-model" if raw_runtime != "mock" else "dummy-mock",
            service_endpoint=service_endpoint
        )

    @property
    def current(self) -> AppConfig:
        """Acceso al objeto de configuración validado."""
        return self._config

# Instancia única para uso como Singleton en el sistema de componentes.
config_manager = ConfigManager()