
# Gestion de servicios de la empresa Software FJ

from abc import abstractmethod
from math import isfinite
from entidades import Entidad
from excepciones import ValidacionError


class Servicio(Entidad):

    def __init__(self, identificacion, nombre, precio_base):
        super().__init__(identificacion, nombre)

        if (
            not isinstance(precio_base, (int, float))
            or isinstance(precio_base, bool)
            or not isfinite(precio_base)
            or precio_base <= 0
        ):
            raise ValidacionError(
                "El precio base debe ser un numero mayor que cero."
            )

        self._precio_base = precio_base

    @property
    def precio_base(self):
        return self._precio_base

    @abstractmethod
    def calcular_costo(self, cantidad=1, descuento=0):
        pass

    @abstractmethod
    def validar_parametros(self, cantidad):
        pass

    @abstractmethod
    def describir(self):
        pass


class ReservaSala(Servicio):

    def calcular_costo(self, cantidad=1, descuento=0):
        self.validar_parametros(cantidad)

        if (
            not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise ValidacionError(
                "El descuento debe estar entre 0 y 100."
            )

        subtotal = self.precio_base * cantidad
        return subtotal - (subtotal * descuento / 100)

    def validar_parametros(self, cantidad):
        if (
            not isinstance(cantidad, (int, float))
            or isinstance(cantidad, bool)
            or not isfinite(cantidad)
            or cantidad <= 0
        ):
            raise ValidacionError(
                "Las horas deben ser mayores que cero."
            )

    def describir(self):
        return (
            f"Reserva de sala: {self.nombre} | "
            f"Tarifa por hora: ${self.precio_base}"
        )


class AlquilerEquipo(Servicio):

    def calcular_costo(self, cantidad=1, descuento=0):
        self.validar_parametros(cantidad)

        if (
            not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise ValidacionError(
                "El descuento debe estar entre 0 y 100."
            )

        subtotal = self.precio_base * cantidad
        return subtotal - (subtotal * descuento / 100)

    def validar_parametros(self, cantidad):
        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):
            raise ValidacionError(
                "La cantidad de equipos debe ser un entero positivo."
            )

    def describir(self):
        return (
            f"Alquiler de equipo: {self.nombre} | "
            f"Precio por unidad: ${self.precio_base}"
        )


class Asesoria(Servicio):

    def calcular_costo(self, cantidad=1, descuento=0):
        self.validar_parametros(cantidad)

        if (
            not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise ValidacionError(
                "El descuento debe estar entre 0 y 100."
            )

        subtotal = self.precio_base * cantidad
        return subtotal - (subtotal * descuento / 100)

    def validar_parametros(self, cantidad):
        if (
            not isinstance(cantidad, (int, float))
            or isinstance(cantidad, bool)
            or not isfinite(cantidad)
            or cantidad <= 0
        ):
            raise ValidacionError(
                "La duracion de la asesoria debe ser mayor que cero."
            )

    def describir(self):
        return (
            f"Asesoria especializada: {self.nombre} | "
            f"Precio por hora: ${self.precio_base}"
        )
