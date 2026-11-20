
# Interfaz grafica del sistema Software FJ

import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import SistemaError
from registro import registrar_evento, registrar_error


class InterfazSoftwareFJ:

    def __init__(self, ventana):

        self.ventana = ventana
        self.ventana.title("Software FJ - Gestion Integral")
        self.ventana.geometry("1050x700")
        self.ventana.minsize(850, 600)

        self.clientes = []
        self.reservas = []

        self.servicios = [
            ReservaSala("S01", "Sala de reuniones", 25000),
            AlquilerEquipo("E01", "Proyector", 15000),
            Asesoria("A01", "Asesoria tecnologica", 50000)
        ]

        self.crear_interfaz()
        registrar_evento("Interfaz grafica iniciada")

    def crear_interfaz(self):

        encabezado = tk.Frame(
            self.ventana,
            bg="#17365D",
            height=100
        )
        encabezado.pack(fill="x")

        titulo = tk.Label(
            encabezado,
            text="SOFTWARE FJ",
            font=("Arial", 25, "bold"),
            bg="#17365D",
            fg="white"
        )
        titulo.pack(pady=(15, 0))

        subtitulo = tk.Label(
            encabezado,
            text="Sistema de Gestion de Clientes, Servicios y Reservas",
            font=("Arial", 11),
            bg="#17365D",
            fg="white"
        )
        subtitulo.pack()

        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.pestana_clientes = ttk.Frame(self.pestanas)
        self.pestana_servicios = ttk.Frame(self.pestanas)
        self.pestana_reservas = ttk.Frame(self.pestanas)
        self.pestana_registros = ttk.Frame(self.pestanas)

        self.pestanas.add(
            self.pestana_clientes,
            text="Clientes"
        )

        self.pestanas.add(
            self.pestana_servicios,
            text="Servicios"
        )

        self.pestanas.add(
            self.pestana_reservas,
            text="Reservas"
        )

        self.pestanas.add(
            self.pestana_registros,
            text="Registros"
        )

        self.crear_pestana_clientes()
        self.crear_pestana_servicios()
        self.crear_pestana_reservas()
        self.crear_pestana_registros()

    # --------------------------------
    # GESTION DE CLIENTES
    # --------------------------------

    def crear_pestana_clientes(self):

        marco = ttk.LabelFrame(
            self.pestana_clientes,
            text="Registrar nuevo cliente",
            padding=15
        )
        marco.pack(fill="x", padx=15, pady=15)

        ttk.Label(
            marco,
            text="Identificacion:"
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.identificacion = ttk.Entry(marco, width=35)
        self.identificacion.grid(row=0, column=1, pady=5)

        ttk.Label(
            marco,
            text="Nombre:"
        ).grid(row=1, column=0, sticky="w", pady=5)

        self.nombre = ttk.Entry(marco, width=35)
        self.nombre.grid(row=1, column=1, pady=5)

        ttk.Label(
            marco,
            text="Correo:"
        ).grid(row=2, column=0, sticky="w", pady=5)

        self.correo = ttk.Entry(marco, width=35)
        self.correo.grid(row=2, column=1, pady=5)

        ttk.Label(
            marco,
            text="Telefono:"
        ).grid(row=3, column=0, sticky="w", pady=5)

        self.telefono = ttk.Entry(marco, width=35)
        self.telefono.grid(row=3, column=1, pady=5)

        ttk.Button(
            marco,
            text="Registrar cliente",
            command=self.registrar_cliente
        ).grid(row=4, column=1, pady=12, sticky="e")

        tabla_marco = ttk.LabelFrame(
            self.pestana_clientes,
            text="Clientes registrados",
            padding=10
        )
        tabla_marco.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        columnas = (
            "identificacion",
            "nombre",
            "correo",
            "telefono"
        )

        self.tabla_clientes = ttk.Treeview(
            tabla_marco,
            columns=columnas,
            show="headings"
        )

        encabezados = {
            "identificacion": "Identificacion",
            "nombre": "Nombre",
            "correo": "Correo",
            "telefono": "Telefono"
        }

        for columna, texto in encabezados.items():
            self.tabla_clientes.heading(
                columna,
                text=texto
            )

        self.tabla_clientes.pack(
            fill="both",
            expand=True
        )

    def registrar_cliente(self):

        try:
            identificacion = self.identificacion.get().strip()
            nombre = self.nombre.get().strip()
            correo = self.correo.get().strip()
            telefono = self.telefono.get().strip()

            if any(
                c.identificacion == identificacion
                for c in self.clientes
            ):
                raise ValueError(
                    "El cliente ya esta registrado."
                )

            cliente = Cliente(
                identificacion,
                nombre,
                correo,
                telefono
            )

            self.clientes.append(cliente)

            self.tabla_clientes.insert(
                "",
                "end",
                values=(
                    cliente.identificacion,
                    cliente.nombre,
                    cliente.correo,
                    cliente.telefono
                )
            )

            registrar_evento(
                f"Cliente registrado desde interfaz: {identificacion}"
            )

            self.actualizar_clientes_reserva()

            self.identificacion.delete(0, tk.END)
            self.nombre.delete(0, tk.END)
            self.correo.delete(0, tk.END)
            self.telefono.delete(0, tk.END)

            messagebox.showinfo(
                "Software FJ",
                "Cliente registrado correctamente."
            )

        except (SistemaError, ValueError) as error:
            registrar_error(str(error))
            messagebox.showerror("Error", str(error))

    # --------------------------------
    # CATALOGO DE SERVICIOS
    # --------------------------------

    def crear_pestana_servicios(self):

        marco = ttk.LabelFrame(
            self.pestana_servicios,
            text="Catalogo de servicios disponibles",
            padding=15
        )
        marco.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        columnas = (
            "codigo",
            "nombre",
            "precio",
            "descripcion"
        )

        self.tabla_servicios = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings"
        )

        self.tabla_servicios.heading(
            "codigo",
            text="Codigo"
        )
        self.tabla_servicios.heading(
            "nombre",
            text="Servicio"
        )
        self.tabla_servicios.heading(
            "precio",
            text="Precio"
        )
        self.tabla_servicios.heading(
            "descripcion",
            text="Descripcion"
        )

        self.tabla_servicios.column("codigo", width=90)
        self.tabla_servicios.column("nombre", width=180)
        self.tabla_servicios.column("precio", width=120)
        self.tabla_servicios.column("descripcion", width=350)

        self.tabla_servicios.pack(
            fill="both",
            expand=True
        )

        for servicio in self.servicios:
            self.tabla_servicios.insert(
                "",
                "end",
                values=(
                    servicio.identificacion,
                    servicio.nombre,
                    f"${servicio.precio_base:,.2f}",
                    servicio.describir()
                )
            )

    # --------------------------------
    # GESTION DE RESERVAS
    # --------------------------------

    def crear_pestana_reservas(self):

        marco = ttk.LabelFrame(
            self.pestana_reservas,
            text="Crear nueva reserva",
            padding=15
        )
        marco.pack(fill="x", padx=15, pady=10)

        ttk.Label(
            marco,
            text="Cliente:"
        ).grid(row=0, column=0, sticky="w", pady=6)

        self.combo_clientes = ttk.Combobox(
            marco,
            state="readonly",
            width=35
        )
        self.combo_clientes.grid(
            row=0,
            column=1,
            pady=6
        )

        ttk.Label(
            marco,
            text="Servicio:"
        ).grid(row=1, column=0, sticky="w", pady=6)

        self.combo_servicios = ttk.Combobox(
            marco,
            state="readonly",
            width=35,
            values=[
                f"{s.identificacion} - {s.nombre}"
                for s in self.servicios
            ]
        )
        self.combo_servicios.grid(
            row=1,
            column=1,
            pady=6
        )

        ttk.Label(
            marco,
            text="Horas o cantidad de equipos:"
        ).grid(row=2, column=0, sticky="w", pady=6)

        self.duracion = ttk.Entry(marco, width=38)
        self.duracion.grid(row=2, column=1, pady=6)

        ttk.Button(
            marco,
            text="Crear reserva",
            command=self.crear_reserva
        ).grid(row=3, column=1, pady=12, sticky="e")

        acciones = ttk.Frame(
            self.pestana_reservas,
            padding=10
        )
        acciones.pack(fill="x")

        ttk.Button(
            acciones,
            text="Confirmar seleccionada",
            command=self.confirmar_reserva
        ).pack(side="left", padx=5)

        ttk.Button(
            acciones,
            text="Cancelar seleccionada",
            command=self.cancelar_reserva
        ).pack(side="left", padx=5)

        columnas = (
            "codigo",
            "cliente",
            "servicio",
            "duracion",
            "estado",
            "costo"
        )

        self.tabla_reservas = ttk.Treeview(
            self.pestana_reservas,
            columns=columnas,
            show="headings"
        )

        encabezados = {
            "codigo": "Reserva",
            "cliente": "Cliente",
            "servicio": "Servicio",
            "duracion": "Duracion",
            "estado": "Estado",
            "costo": "Costo total"
        }

        for columna, texto in encabezados.items():
            self.tabla_reservas.heading(
                columna,
                text=texto
            )

        self.tabla_reservas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.actualizar_clientes_reserva()

    def actualizar_clientes_reserva(self):

        self.combo_clientes["values"] = [
            f"{c.identificacion} - {c.nombre}"
            for c in self.clientes
        ]

    def crear_reserva(self):

        try:
            cliente_seleccionado = self.combo_clientes.get()

            if not cliente_seleccionado:
                raise ValueError(
                    "Debe seleccionar un cliente."
                )

            identificacion = cliente_seleccionado.split(" - ")[0]

            cliente = next(
                c for c in self.clientes
                if c.identificacion == identificacion
            )

            servicio_seleccionado = self.combo_servicios.get()

            if not servicio_seleccionado:
                raise ValueError(
                    "Debe seleccionar un servicio."
                )

            codigo = servicio_seleccionado.split(" - ")[0]

            servicio = next(
                s for s in self.servicios
                if s.identificacion == codigo
            )

            cantidad_texto = self.duracion.get().strip()

            if isinstance(servicio, AlquilerEquipo):
                cantidad = int(cantidad_texto)
            else:
                cantidad = float(cantidad_texto)

            numero = len(self.reservas) + 1
            codigo_reserva = f"R{numero:03d}"

            reserva = Reserva(
                codigo_reserva,
                cliente,
                servicio,
                cantidad
            )

            self.reservas.append(reserva)

            self.actualizar_tabla_reservas()

            registrar_evento(
                f"Reserva creada desde interfaz: {codigo_reserva}"
            )

            self.duracion.delete(0, tk.END)

            messagebox.showinfo(
                "Software FJ",
                f"Reserva {codigo_reserva} creada correctamente."
            )

        except (SistemaError, ValueError, StopIteration) as error:
            registrar_error(str(error))
            messagebox.showerror("Error", str(error))

    def obtener_reserva_seleccionada(self):

        seleccion = self.tabla_reservas.selection()

        if not seleccion:
            messagebox.showwarning(
                "Aviso",
                "Seleccione una reserva de la tabla."
            )
            return None

        valores = self.tabla_reservas.item(
            seleccion[0],
            "values"
        )

        codigo = valores[0]

        return next(
            (
                r for r in self.reservas
                if r.identificacion == codigo
            ),
            None
        )

    def actualizar_tabla_reservas(self):

        for elemento in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(elemento)

        for reserva in self.reservas:

            costo = (
                f"${reserva.costo_total:,.2f}"
                if reserva.costo_total is not None
                else "Pendiente"
            )

            self.tabla_reservas.insert(
                "",
                "end",
                values=(
                    reserva.identificacion,
                    reserva.cliente.nombre,
                    reserva.servicio.nombre,
                    reserva.duracion,
                    reserva.estado,
                    costo
                )
            )

    def confirmar_reserva(self):

        reserva = self.obtener_reserva_seleccionada()

        if reserva is None:
            return

        descuento = simpledialog.askfloat(
            "Confirmar reserva",
            "Ingrese el descuento (0 a 100):",
            minvalue=0,
            maxvalue=100,
            parent=self.ventana
        )

        if descuento is None:
            return

        try:
            costo = reserva.confirmar(descuento)

            self.actualizar_tabla_reservas()

            registrar_evento(
                f"Reserva confirmada desde interfaz: {reserva.identificacion}"
            )

            messagebox.showinfo(
                "Reserva confirmada",
                f"El costo total es: ${costo:,.2f}"
            )

        except SistemaError as error:
            registrar_error(str(error))
            messagebox.showerror("Error", str(error))

    def cancelar_reserva(self):

        reserva = self.obtener_reserva_seleccionada()

        if reserva is None:
            return

        try:
            reserva.cancelar()

            self.actualizar_tabla_reservas()

            registrar_evento(
                f"Reserva cancelada desde interfaz: {reserva.identificacion}"
            )

            messagebox.showinfo(
                "Software FJ",
                "Reserva cancelada correctamente."
            )

        except SistemaError as error:
            registrar_error(str(error))
            messagebox.showerror("Error", str(error))

    # --------------------------------
    # CONSULTA DE REGISTROS
    # --------------------------------

    def crear_pestana_registros(self):

        marco = ttk.LabelFrame(
            self.pestana_registros,
            text="Historial de eventos y errores",
            padding=10
        )
        marco.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        ttk.Button(
            marco,
            text="Actualizar registros",
            command=self.consultar_registros
        ).pack(anchor="e", pady=5)

        self.texto_registros = tk.Text(
            marco,
            wrap="word",
            font=("Consolas", 10),
            height=20
        )

        self.texto_registros.pack(
            fill="both",
            expand=True
        )

        self.consultar_registros()

    def consultar_registros(self):

        ruta = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "logs",
            "sistema.log"
        )

        self.texto_registros.delete(
            "1.0",
            tk.END
        )

        try:
            with open(
                ruta,
                "r",
                encoding="utf-8"
            ) as archivo:

                contenido = archivo.read()

                if contenido:
                    self.texto_registros.insert(
                        tk.END,
                        contenido
                    )
                else:
                    self.texto_registros.insert(
                        tk.END,
                        "No hay eventos registrados."
                    )

        except FileNotFoundError:
            self.texto_registros.insert(
                tk.END,
                "Todavia no existe el archivo de registros."
            )


# --------------------------------
# INICIAR APLICACION
# --------------------------------

if __name__ == "__main__":

    ventana = tk.Tk()

    aplicacion = InterfazSoftwareFJ(ventana)

    ventana.mainloop()
