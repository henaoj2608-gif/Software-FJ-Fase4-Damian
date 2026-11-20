
# Clase abstracta para las entidades del sistema Software FJ

from abc import ABC, abstractmethod
from excepciones import ValidacionError


class Entidad(ABC):

    def __init__(self, identificacion, nombre):
        if not identificacion or not identificacion.strip():
            raise ValidacionError("La identificacion es obligatoria.")

        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre es obligatorio.")

        self.__identificacion = identificacion.strip()
        self.__nombre = nombre.strip()

    @property
    def identificacion(self):
        return self.__identificacion

    @property
    def nombre(self):
        return self.__nombre

    @abstractmethod
    def describir(self):
        pass
