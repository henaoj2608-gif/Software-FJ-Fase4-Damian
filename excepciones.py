
# Excepciones personalizadas del sistema Software FJ

class SistemaError(Exception):
    """Error general del sistema."""
    pass


class ValidacionError(SistemaError):
    """Error cuando los datos ingresados no son válidos."""
    pass


class ClienteError(SistemaError):
    """Error relacionado con la gestión de clientes."""
    pass


class ServicioError(SistemaError):
    """Error relacionado con los servicios."""
    pass


class ReservaError(SistemaError):
    """Error relacionado con las reservas."""
    pass


class ServicioNoDisponibleError(ServicioError):
    """Error cuando un servicio no está disponible."""
    pass


class OperacionNoPermitidaError(SistemaError):
    """Error cuando se intenta realizar una operación no permitida."""
    pass
