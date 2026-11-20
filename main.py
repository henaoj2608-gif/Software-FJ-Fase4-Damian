
# Programa principal del sistema Software FJ

import os

from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import (
    SistemaError,
    ValidacionError,
    ClienteError,
    ServicioError,
    ReservaError
)
from registro import (
    registrar_evento,
    registrar_error,
    registrar_excepcion
)


# Listas para almacenar la informacion
clientes = []
reservas = []


# Catalogo de servicios disponibles
servicios = [
    ReservaSala("S01", "Sala de reuniones", 25000),
    AlquilerEquipo("E01", "Proyector", 15000),
    Asesoria("A01", "Asesoria tecnologica", 50000)
]


def buscar_cliente(identificacion):
    for cliente in clientes:
        if cliente.identificacion == identificacion:
            return cliente

    return None


def buscar_reserva(identificacion):
    for reserva in reservas:
        if reserva.identificacion == identificacion:
            return reserva

    return None


def registrar_cliente():
    try:
        print("\n--- REGISTRO DE CLIENTE ---")

        identificacion = input("Identificacion: ").strip()
        nombre = input("Nombre completo: ").strip()
        correo = input("Correo electronico: ").strip()
        telefono = input("Telefono: ").strip()

        if buscar_cliente(identificacion):
            raise ClienteError(
                "El cliente ya se encuentra registrado."
            )

        cliente = Cliente(
            identificacion,
            nombre,
            correo,
            telefono
        )

        clientes.append(cliente)

        registrar_evento(
            f"Cliente registrado: {identificacion}"
        )

    except SistemaError as error:
        registrar_error(str(error))
        print(f"Error: {error}")

    else:
        print("Cliente registrado correctamente.")

    finally:
        print("Operacion de registro finalizada.")


def mostrar_clientes():
    print("\n--- LISTA DE CLIENTES ---")

    if not clientes:
        print("No hay clientes registrados.")
        return

    for cliente in clientes:
        print(cliente.describir())


def mostrar_servicios():
    print("\n--- SERVICIOS DISPONIBLES ---")

    for servicio in servicios:
        print(
            f"Codigo: {servicio.identificacion} | "
            f"{servicio.describir()}"
        )


def crear_reserva():
    try:
        print("\n--- CREAR RESERVA ---")

        identificacion_cliente = input(
            "Identificacion del cliente: "
        ).strip()

        cliente = buscar_cliente(identificacion_cliente)

        if cliente is None:
            raise ClienteError("El cliente no existe.")

        mostrar_servicios()

        codigo = input(
            "Codigo del servicio: "
        ).strip().upper()

        servicio = next(
            (s for s in servicios if s.identificacion == codigo),
            None
        )

        if servicio is None:
            raise ServicioError(
                "El servicio seleccionado no existe."
            )

        duracion_texto = input(
            "Cantidad de horas o equipos: "
        ).strip()

        try:
            if isinstance(servicio, AlquilerEquipo):
                duracion = int(duracion_texto)
            else:
                duracion = float(duracion_texto)

        except ValueError as error:
            raise ValidacionError(
                "La cantidad ingresada no es numerica."
            ) from error

        numero = len(reservas) + 1
        identificacion = f"R{numero:03d}"

        nueva_reserva = Reserva(
            identificacion,
            cliente,
            servicio,
            duracion
        )

        reservas.append(nueva_reserva)

        registrar_evento(
            f"Reserva creada: {identificacion}"
        )

        print("Reserva creada correctamente.")
        print(nueva_reserva.describir())

    except SistemaError as error:
        registrar_error(str(error))
        print(f"Error: {error}")

    else:
        print("Proceso de reserva finalizado correctamente.")

    finally:
        print("Operacion de creacion finalizada.")


def confirmar_reserva():
    try:
        print("\n--- CONFIRMAR RESERVA ---")

        identificacion = input(
            "Identificacion de la reserva: "
        ).strip().upper()

        reserva = buscar_reserva(identificacion)

        if reserva is None:
            raise ReservaError("La reserva no existe.")

        descuento = float(
            input(
                "Descuento (escriba solo el numero, sin %): "
            )
        )

        costo = reserva.confirmar(descuento)

        registrar_evento(
            f"Reserva confirmada: {identificacion}"
        )

        print("Reserva confirmada correctamente.")
        print(f"Costo total: ${costo:,.2f}")

    except (SistemaError, ValueError) as error:
        registrar_error(str(error))
        print(f"Error: {error}")

    else:
        print("Confirmacion realizada correctamente.")

    finally:
        print("Operacion de confirmacion finalizada.")


def cancelar_reserva():
    try:
        print("\n--- CANCELAR RESERVA ---")

        identificacion = input(
            "Identificacion de la reserva: "
        ).strip().upper()

        reserva = buscar_reserva(identificacion)

        if reserva is None:
            raise ReservaError("La reserva no existe.")

        resultado = reserva.cancelar()

        registrar_evento(
            f"Reserva cancelada: {identificacion}"
        )

        print(resultado)

    except SistemaError as error:
        registrar_error(str(error))
        print(f"Error: {error}")

    else:
        print("Cancelacion realizada correctamente.")

    finally:
        print("Operacion de cancelacion finalizada.")


def mostrar_reservas():
    print("\n--- LISTA DE RESERVAS ---")

    if not reservas:
        print("No hay reservas registradas.")
        return

    for reserva in reservas:
        print(reserva.describir())

        if reserva.costo_total is not None:
            print(
                f"Costo total: ${reserva.costo_total:,.2f}"
            )


def consultar_cliente():
    print("\n--- CONSULTAR CLIENTE ---")

    identificacion = input(
        "Identificacion del cliente: "
    ).strip()

    cliente = buscar_cliente(identificacion)

    if cliente is None:
        print("No se encontro el cliente.")
    else:
        print(cliente.describir())


def actualizar_correo():
    try:
        print("\n--- ACTUALIZAR CORREO ---")

        identificacion = input(
            "Identificacion del cliente: "
        ).strip()

        cliente = buscar_cliente(identificacion)

        if cliente is None:
            raise ClienteError("El cliente no existe.")

        nuevo_correo = input(
            "Nuevo correo electronico: "
        ).strip()

        cliente.actualizar_correo(nuevo_correo)

        registrar_evento(
            f"Correo actualizado: {identificacion}"
        )

        print("Correo actualizado correctamente.")

    except SistemaError as error:
        registrar_error(str(error))
        print(f"Error: {error}")

    finally:
        print("Operacion de actualizacion finalizada.")


def consultar_registros():
    print("\n--- REGISTRO DE EVENTOS ---")

    ruta = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "logs",
        "sistema.log"
    )

    try:
        with open(
            ruta,
            "r",
            encoding="utf-8"
        ) as archivo:

            contenido = archivo.read()

            if contenido:
                print(contenido)
            else:
                print("No hay eventos registrados.")

    except FileNotFoundError:
        print("Todavia no existe el archivo de registros.")

    except OSError as error:
        registrar_error(
            f"Error al consultar los registros: {error}"
        )
        print(f"No se pudo leer el archivo: {error}")


def mostrar_menu():
    print("\n" + "=" * 48)
    print("       SOFTWARE FJ - GESTION INTEGRAL")
    print("=" * 48)
    print("1. Registrar cliente")
    print("2. Mostrar clientes")
    print("3. Mostrar servicios")
    print("4. Crear reserva")
    print("5. Confirmar reserva")
    print("6. Cancelar reserva")
    print("7. Mostrar reservas")
    print("8. Consultar cliente")
    print("9. Actualizar correo")
    print("10. Consultar registro de eventos")
    print("0. Salir")
    print("=" * 48)


def ejecutar_sistema():

    registrar_evento("Inicio del sistema Software FJ")

    while True:
        mostrar_menu()

        try:
            opcion = input(
                "Seleccione una opcion: "
            ).strip()

            if opcion == "1":
                registrar_cliente()

            elif opcion == "2":
                mostrar_clientes()

            elif opcion == "3":
                mostrar_servicios()

            elif opcion == "4":
                crear_reserva()

            elif opcion == "5":
                confirmar_reserva()

            elif opcion == "6":
                cancelar_reserva()

            elif opcion == "7":
                mostrar_reservas()

            elif opcion == "8":
                consultar_cliente()

            elif opcion == "9":
                actualizar_correo()

            elif opcion == "10":
                consultar_registros()

            elif opcion == "0":
                registrar_evento(
                    "Cierre del sistema Software FJ"
                )
                print("Gracias por utilizar Software FJ.")
                break

            else:
                print(
                    "Opcion no valida. Intente nuevamente."
                )

        except KeyboardInterrupt:
            registrar_evento("Interrupcion del sistema")
            print("\nEl sistema fue interrumpido.")
            break

        except Exception as error:
            registrar_excepcion(
                "Error inesperado durante la ejecucion"
            )
            print(
                f"Se produjo un error inesperado: {error}"
            )


if __name__ == "__main__":
    ejecutar_sistema()
