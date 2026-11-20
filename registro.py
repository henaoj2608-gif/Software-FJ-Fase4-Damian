
# Registro de eventos y errores del sistema Software FJ

import logging
import os


def configurar_registro():
    carpeta_logs = "logs"

    os.makedirs(carpeta_logs, exist_ok=True)

    ruta_archivo = os.path.join(carpeta_logs, "sistema.log")

    logging.basicConfig(
        filename=ruta_archivo,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True
    )

    return logging.getLogger("SoftwareFJ")


logger = configurar_registro()


def registrar_evento(mensaje):
    logger.info(mensaje)


def registrar_error(mensaje):
    logger.error(mensaje)


def registrar_excepcion(mensaje):
    logger.exception(mensaje)

