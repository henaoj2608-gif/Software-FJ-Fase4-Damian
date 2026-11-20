
# Gestion de reservas del sistema Software FJ

from datetime import datetime
from clientes import Cliente
from servicios import Servicio
from excepciones import (
    ReservaError,
    ClienteError,
    ServicioError,
    ValidacionError,
    OperacionNoPermitidaError
)


class Reserva:

    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada")

    def __init__(self, identificacion, cliente, servicio, duracion):

        if not identificacion or not identificacion.strip():
            raise ValidacionError("La identificacion de la reserva es obligatoria.")

        if not isinstance(cliente, Cliente):
            raise ClienteError("Debe seleccionar un cliente valido.")

        if not isinstance(servicio, Servicio):
            raise ServicioError("Debe seleccionar un servicio valido.")

        servicio.validar_parametros(duracion)

        self.__identificacion = identificacion.strip()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"
        self.__fecha_creacion = datetime.now()
        self.__costo_total = None

    @property
    def identificacion(self):
        return self.__identificacion

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    def calcular_costo(self, descuento=0):
        return self.__servicio.calcular_costo(
            self.__duracion,
            descuento
        )

    def confirmar(self, descuento=0):
        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        try:
            self.__costo_total = self.calcular_costo(descuento)
        except Exception as error:
            raise ReservaError(
                "No fue posible calcular el costo de la reserva."
            ) from error
        else:
            self.__estado = "Confirmada"
            return self.__costo_total

    def cancelar(self):
        if self.__estado == "Cancelada":
            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra cancelada."
            )

        if self.__estado == "Confirmada":
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva confirmada."
            )

        self.__estado = "Cancelada"
        return "La reserva fue cancelada correctamente."

    def describir(self):
        return (
            f"Reserva: {self.__identificacion} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duracion: {self.__duracion} | "
            f"Estado: {self.__estado}"
        )
