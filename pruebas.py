
# Pruebas automaticas del sistema Software FJ

import unittest

from clientes import Cliente
from entidades import Entidad
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import ValidacionError, OperacionNoPermitidaError


class PruebasSoftwareFJ(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente(
            "12345",
            "Damian Henao",
            "damian@gmail.com",
            "3001234567"
        )

        self.sala = ReservaSala(
            "S01",
            "Sala de reuniones",
            25000
        )

        self.equipo = AlquilerEquipo(
            "E01",
            "Proyector",
            15000
        )

        self.asesoria = Asesoria(
            "A01",
            "Asesoria tecnologica",
            50000
        )

    # Prueba 1: Registrar un cliente correctamente
    def test_registrar_cliente(self):
        self.assertEqual(self.cliente.nombre, "Damian Henao")

    # Prueba 2: Rechazar un correo invalido
    def test_correo_invalido(self):
        with self.assertRaises(ValidacionError):
            Cliente("123", "Juan", "correo_invalido", "3001234567")

    # Prueba 3: Rechazar un telefono invalido
    def test_telefono_invalido(self):
        with self.assertRaises(ValidacionError):
            Cliente("123", "Juan", "juan@gmail.com", "123")

    # Prueba 4: Calcular el costo de una sala
    def test_calcular_reserva_sala(self):
        resultado = self.sala.calcular_costo(2)
        self.assertEqual(resultado, 50000)

    # Prueba 5: Calcular el alquiler de equipos
    def test_calcular_alquiler_equipo(self):
        resultado = self.equipo.calcular_costo(3)
        self.assertEqual(resultado, 45000)

    # Prueba 6: Calcular una asesoria con descuento
    def test_calcular_asesoria(self):
        resultado = self.asesoria.calcular_costo(2, 10)
        self.assertEqual(resultado, 90000)

    # Prueba 7: Rechazar una cantidad invalida
    def test_cantidad_invalida(self):
        with self.assertRaises(ValidacionError):
            self.sala.calcular_costo(-2)

    # Prueba 8: Crear una reserva correctamente
    def test_crear_reserva(self):
        reserva = Reserva(
            "R001",
            self.cliente,
            self.sala,
            2
        )

        self.assertEqual(reserva.estado, "Pendiente")

    # Prueba 9: Confirmar una reserva
    def test_confirmar_reserva(self):
        reserva = Reserva(
            "R002",
            self.cliente,
            self.sala,
            2
        )

        costo = reserva.confirmar()

        self.assertEqual(costo, 50000)
        self.assertEqual(reserva.estado, "Confirmada")

    # Prueba 10: Cancelar una reserva pendiente
    def test_cancelar_reserva(self):
        reserva = Reserva(
            "R003",
            self.cliente,
            self.sala,
            1
        )

        reserva.cancelar()

        self.assertEqual(reserva.estado, "Cancelada")

    # Prueba adicional: No confirmar una reserva cancelada
    def test_confirmar_reserva_cancelada(self):
        reserva = Reserva(
            "R004",
            self.cliente,
            self.sala,
            1
        )

        reserva.cancelar()

        with self.assertRaises(OperacionNoPermitidaError):
            reserva.confirmar()

    # Prueba adicional: Actualizar correo
    def test_actualizar_correo(self):
        self.cliente.actualizar_correo("nuevo@gmail.com")

        self.assertEqual(
            self.cliente.correo,
            "nuevo@gmail.com"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
