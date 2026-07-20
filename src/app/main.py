"""
Punto de entrada de Malāk.

Versión: 0.6.0-alpha
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from malak.shared.logger import logger


def main():
    logger.info("========================================")
    logger.info("Iniciando Malāk...")
    logger.info("========================================")


if __name__ == "__main__":
    main()