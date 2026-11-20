
# Gestion de clientes del sistema Software FJ

import re

from entidades import Entidad
from excepciones import ValidacionError


class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion, nombre)

        # Validar el correo electronico
        if not self.validar_correo(correo):
            raise ValidacionError(
                "El correo electronico no tiene un formato valido."
            )

        # Validar el numero de telefono
        if (
            not isinstance(telefono, str)
            or not telefono.isdigit()
            or len(telefono) < 7
        ):
            raise ValidacionError(
                "El telefono debe tener minimo 7 digitos."
            )

        # Atributos privados
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()

    @staticmethod
    def validar_correo(correo):
        """Comprueba que el correo tenga un formato valido."""

        if not isinstance(correo, str):
            return False

        patron = r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}"

        return re.fullmatch(patron, correo.strip()) is not None

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):
        return (
            f"Cliente: {self.nombre} | "
            f"Identificacion: {self.identificacion} | "
            f"Correo: {self.correo} | "
            f"Telefono: {self.telefono}"
        )

    def actualizar_correo(self, nuevo_correo):

        if not self.validar_correo(nuevo_correo):
            raise ValidacionError(
                "El nuevo correo electronico no es valido."
            )

        self.__correo = nuevo_correo.strip()

        return "Correo actualizado correctamente."

