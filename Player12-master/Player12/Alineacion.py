import os
import sys
import pymysql
from PIL import Image
import customtkinter as Ctk
import random
import pywinstyles

class Alineacion(Ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Alineación")
    
        ancho_ventana = 1200
        alto_ventana = 900

        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")


        self.configure(fg_color="white")

        self.ROJO = "#B71C1C"
        self.GRIS = "#9E9E9E"
        self.VERDE_CAMPO = "#5f9501"
        self.FUENTE_MODERNA = ("Bebas Neue", 16)
        self.DB_CONFIG = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "Player12"
        }
        self.formacion = {"Portero": 1, "Defensa": 4, "Centrocampista": 3, "Delantero": 3}
        self.alineacion = {pos: [] for pos in self.formacion}
        self.labels = {pos: [] for pos in self.formacion}
        self.equipo_labels = {pos: [] for pos in self.formacion}
        self.popup_activo = False 

        self.equipos = self.obtener_equipos()

        self.create_widgets()

        self.mostrar_instrucciones()

        self.protocol("WM_DELETE_WINDOW", self.volver_al_menu)

    def mostrar_popup(self, titulo, mensaje):
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS 
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        
        if self.popup_activo:
            return
        self.popup_activo = True

        try:
            popup = Ctk.CTkToplevel(self)
            popup.title(titulo)
            popup.geometry("500x350")
            popup.minsize(500, 350)
            popup.resizable(True, True)
            popup.transient(self)
            popup.configure(fg_color="white")

            try:
                imagen_fondo = Ctk.CTkImage(Image.open(resource_path("./img/futebol.jpg")), size=(500, 350))
                label_fondo = Ctk.CTkLabel(popup, image=imagen_fondo, text="")
                label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception:
                label_fondo = Ctk.CTkLabel(popup, text="")
                label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

            frame_texto = Ctk.CTkFrame(popup, fg_color="white")
            frame_texto.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.8)

            Ctk.CTkLabel(
                frame_texto,
                text=titulo,
                font=Ctk.CTkFont(size=18, weight="bold"),
                text_color="black"
            ).pack(pady=(10, 10))

            frame_mensaje = Ctk.CTkFrame(frame_texto, fg_color="#CCCCCC")
            frame_mensaje.pack(padx=10, pady=(0, 10), fill="x")

            Ctk.CTkLabel(
                frame_mensaje,
                text=mensaje,
                font=("Bebas Neue", 14),
                text_color="black",
                wraplength=400,
                justify="center"
            ).pack(padx=10, pady=10)

            Ctk.CTkButton(
                popup,
                text="Entendido",
                command=lambda: [popup.destroy(), setattr(self, "popup_activo", False)],
                width=120,
                fg_color=self.ROJO,
                hover_color="#D32F2F",
                font=self.FUENTE_MODERNA
            ).place(relx=0.5, rely=0.9, anchor="center")

            popup.update()
            popup.grab_set()
            popup.focus_force()
            popup.wait_window()
        except Exception as e:
            print(f"Error al mostrar popup: {e}")
        finally:
            self.popup_activo = False

    def mostrar_instrucciones(self):
        def resource_path(relative_path):
                try:
                    base_path = sys._MEIPASS 
                except AttributeError:
                    base_path = os.path.abspath(".")

                return os.path.join(base_path, relative_path)
        
        popup = Ctk.CTkToplevel(self)
        popup.title("Instrucciones del Juego")

        ancho_popup = 700
        alto_popup = 500

        ancho_pantalla = popup.winfo_screenwidth()
        alto_pantalla = popup.winfo_screenheight()

        x = (ancho_pantalla // 2) - (ancho_popup // 2)
        y = (alto_pantalla // 2) - (alto_popup // 2)

        popup.geometry(f"{ancho_popup}x{alto_popup}+{x}+{y}")
        popup.minsize(ancho_popup, alto_popup)
        popup.resizable(True, True)
        popup.transient(self)

        try:
            imagen_fondo = Ctk.CTkImage(Image.open(resource_path("./img/futebol.jpg")), size=(700, 500))
            label_fondo = Ctk.CTkLabel(popup, image=imagen_fondo, text="")
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            label_fondo = Ctk.CTkLabel(popup, text="")
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        frame_texto = Ctk.CTkFrame(popup, fg_color="white")
        frame_texto.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.8)

        Ctk.CTkLabel(
            frame_texto,
            text="INSTRUCCIONES DEL JUEGO DE ALINEACIONES:",
            font=Ctk.CTkFont(size=20, weight="bold"),
            text_color="black"
        ).pack(pady=(10, 10))

        instrucciones = (
            "1. Escribe el nombre del jugador en el cuadro y presiona 'Agregar jugador'.\n\n"
            "2. El jugador debe coincidir con la posición y equipo asignado.\n\n"
            "3. Si no hay espacio para ese jugador en la posición y equipo, se mostrará un aviso.\n\n"
            "4. Puedes seleccionar jugadores de la lista de sugerencias que aparece al escribir.\n\n"
            "5. La formación es 1 Portero, 4 Defensas, 3 Centrocampistas y 3 Delanteros.\n\n"
            "6. Disfruta creando tu alineación perfecta!"
        )

        textbox = Ctk.CTkTextbox(frame_texto, wrap="word", font=("Bebas Neue", 16), fg_color="white", text_color="black")
        textbox.pack(expand=True, fill="both", padx=10, pady=(0, 10))
        textbox.insert("0.0", instrucciones)
        textbox.configure(state="disabled")

        Ctk.CTkButton(
            popup,
            text="Entendido",
            command=popup.destroy,
            width=140,
            fg_color=self.ROJO,
            bg_color=self.VERDE_CAMPO,
            hover_color="#D32F2F"
        ).place(relx=0.5, rely=0.9, anchor="center")

        popup.update()
        popup.grab_set()
        popup.wait_window()

    def obtener_equipos(self):
        try:
            connection = pymysql.connect(**self.DB_CONFIG)
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM equipos")
                resultados = cursor.fetchall()
                return [r[0] for r in resultados]
        except pymysql.MySQLError as e:
            self.mostrar_popup("Error de conexión", f"No se pudo conectar a la BD: {e}")
            return []
        finally:
            if 'connection' in locals():
                connection.close()

    def create_widgets(self):
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        
        try:
            self.imagen_fondo = Ctk.CTkImage(Image.open(resource_path("./img/futebol.jpg")), size=(1200, 900))
            self.label_fondo = Ctk.CTkLabel(self, image=self.imagen_fondo, text="")
            self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            self.label_fondo = Ctk.CTkLabel(self, text="")
            self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)


        self.contenido_borde = Ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.contenido_borde.place(relx=0.048, rely=0.148, relwidth=0.904, relheight=0.704)


        self.contenido_frame = Ctk.CTkFrame(self.contenido_borde, fg_color=self.VERDE_CAMPO, corner_radius=15)
        self.contenido_frame.pack(expand=True, fill="both", padx=3, pady=3)

        pywinstyles.set_opacity(self.contenido_frame, 0x00000001)


        self.crear_fila("Delantero", 3)
        self.crear_fila("Centrocampista", 3)
        self.crear_fila("Defensa", 4)
        self.crear_fila("Portero", 1)

        self.busqueda_frame = Ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        self.busqueda_frame.pack(pady=10)

        self.entry = Ctk.CTkEntry(self.busqueda_frame, width=300, height=45, font=self.FUENTE_MODERNA,
                                  fg_color="black", bg_color="transparent", text_color="#FFFFFF")
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.bind("<KeyRelease>", self.mostrar_sugerencias)

        self.boton_agregar = Ctk.CTkButton(self.busqueda_frame, text="Agregar jugador",
                                           command=self.enviar_nombre,
                                           fg_color=self.ROJO,
                                           height=45,
                                           width=140,
                                           font=self.FUENTE_MODERNA,
                                           corner_radius=20,
                                           bg_color="transparent",
                                           text_color="#FFFFFF")
        self.boton_agregar.pack(side="left")

        self.btn_exit = Ctk.CTkButton(
            self,
            text="Volver al menú",
            command=self.volver_al_menu,
            fg_color=self.ROJO,
            height=45,
            width=140,
            font=self.FUENTE_MODERNA,
            corner_radius=20,
            bg_color=self.VERDE_CAMPO,
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=1.0, anchor="s", y=-10)

        self.suggestion_frame = Ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        self.suggestion_frame.pack(pady=(0, 20), fill="x", ipady=40)

    def crear_fila(self, posicion, cantidad):
        fila_frame = Ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        fila_frame.pack(pady=10, fill="x")

        inner_frame = Ctk.CTkFrame(fila_frame, fg_color="transparent")
        inner_frame.pack(anchor="center")

        for _ in range(cantidad):
            label = Ctk.CTkLabel(inner_frame, text="", width=210, height=80,
                                 fg_color="#CCCCCC", corner_radius=15, text_color="#000000",
                                 anchor="center", justify="center", wraplength=200)
            label.pack(side="left", padx=10)
            equipo_azar = random.choice(self.equipos) if self.equipos else "Sin equipo"
            label.configure(text=equipo_azar)
            self.labels[posicion].append(label)
            self.equipo_labels[posicion].append(equipo_azar)

    def buscar_sugerencias(self, prefijo):
        try:
            connection = pymysql.connect(**self.DB_CONFIG)
            with connection.cursor() as cursor:
                query = "SELECT nombre FROM jugadores WHERE nombre LIKE %s LIMIT 3"
                cursor.execute(query, (f"%{prefijo}%",))
                resultados = cursor.fetchall()
                return [resultado[0] for resultado in resultados]
        except pymysql.MySQLError as e:
            self.mostrar_popup("Error de conexión", f"No se pudo conectar a la BD: {e}")
            return []
        finally:
            if 'connection' in locals():
                connection.close()

    def buscar_jugador(self, nombre):
        try:
            connection = pymysql.connect(**self.DB_CONFIG)
            with connection.cursor() as cursor:
                query = "SELECT nombre, posicion, equipo, dorsal FROM jugadores WHERE nombre = %s"
                cursor.execute(query, (nombre,))
                resultado = cursor.fetchone()
                return resultado if resultado else None
        except pymysql.MySQLError as e:
            self.mostrar_popup("Error de conexión", f"No se pudo conectar a la BD: {e}")
            return None
        finally:
            if 'connection' in locals():
                connection.close()

    def mostrar_sugerencias(self, event):
        texto = self.entry.get().strip()
        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()
        if len(texto) >= 3:
            sugerencias = self.buscar_sugerencias(texto)
            if sugerencias:
                for sugerencia in sugerencias:
                    label = Ctk.CTkLabel(self.suggestion_frame, text=sugerencia,
                                         fg_color="#CCCCCC", corner_radius=10, text_color="#000000")
                    label.pack(pady=5, padx=10, fill="x")
                    label.bind("<Button-1>", lambda event, sug=sugerencia: self.autocompletar(sug))
                self.suggestion_frame.pack(pady=(0, 20), fill="x", ipady=40)
            else:
                self.suggestion_frame.pack_forget()
        else:
            self.suggestion_frame.pack_forget()

    def autocompletar(self, sugerencia):
        self.entry.delete(0, Ctk.END)
        self.entry.insert(0, sugerencia)
        self.suggestion_frame.pack_forget()

    def enviar_nombre(self):
        nombre = self.entry.get().strip()
        if nombre:
            self.agregar_jugador()
            self.suggestion_frame.pack_forget()
    def alineacion_completa(self):
        for posicion, max_jugadores in self.formacion.items():
            if len(self.alineacion[posicion]) < max_jugadores:
                return False
        return True
    
    def agregar_jugador(self):
        nombre = self.entry.get().strip()
        if not nombre:
            self.mostrar_popup("Entrada vacía", "Por favor, ingrese el nombre de un jugador.")
            return
        resultado = self.buscar_jugador(nombre)
        if not resultado:
            self.mostrar_popup("No encontrado", f"No se encontró el jugador: {nombre}")
            self.entry.delete(0, Ctk.END)
            return
        nombre_jugador, posicion, equipo_jugador, dorsal = resultado

        if nombre_jugador in self.alineacion[posicion]:
            self.mostrar_popup("Jugador repetido", f"{nombre_jugador} ya está en la alineación.")
            self.entry.delete(0, Ctk.END)
            return

        indices_libres = [i for i in range(len(self.alineacion[posicion]), self.formacion[posicion])]
        if not indices_libres:
            self.mostrar_popup("Posición llena", f"No hay espacio para más jugadores en la posición '{posicion}'.")
            self.entry.delete(0, Ctk.END)
            return

        print("Jugador:", nombre_jugador)
        print("Posición:", posicion)
        print("Equipo del jugador:", equipo_jugador)
        print("Equipos disponibles en esa posición:", self.equipo_labels[posicion])

        indices_libres = [
            i for i, equipo_label in enumerate(self.equipo_labels[posicion])
            if equipo_label is not None
        ]

        asignado = False
        for i in indices_libres:
            equipo_label = self.equipo_labels[posicion][i]
            print(f"Comparando '{equipo_label}' con '{equipo_jugador}'")

            if equipo_label.strip().lower() == equipo_jugador.strip().lower():
                label = self.labels[posicion][i]
                label.configure(
                    text=f"{nombre_jugador}\n#{dorsal}",
                    fg_color=self.ROJO,
                    corner_radius=15,
                    text_color="#FFFFFF"
                )
                self.alineacion[posicion].append(nombre_jugador)
                self.equipo_labels[posicion][i] = None
                asignado = True
                break

        if not asignado:
            self.mostrar_popup(
                "No coincide equipo",
                f"No hay espacios libres para la posición '{posicion}' con el equipo '{equipo_jugador}'."
            )

        self.entry.delete(0, Ctk.END)

        if self.alineacion_completa():
            self.mostrar_popup_completado()

    def alineacion_completa(self):
        for posicion, cantidad in self.formacion.items():
            if len(self.alineacion.get(posicion, [])) < cantidad:
                return False
        return True

    def mostrar_popup_completado(self):
        def resource_path(relative_path):
                try:
                    base_path = sys._MEIPASS
                except AttributeError:
                    base_path = os.path.abspath(".")

                return os.path.join(base_path, relative_path)
        if self.popup_activo:
            return
        self.popup_activo = True

        try:
            ancho_popup = 500
            alto_popup = 350

            self.update_idletasks()
            ancho_ventana = self.winfo_width()
            alto_ventana = self.winfo_height()
            x_ventana = self.winfo_rootx()
            y_ventana = self.winfo_rooty()

            x = x_ventana + (ancho_ventana // 2) - (ancho_popup // 2)
            y = y_ventana + (alto_ventana // 2) - (alto_popup // 2)

            popup = Ctk.CTkToplevel(self)
            popup.title("¡Alineación Completa!")
            popup.geometry(f"{ancho_popup}x{alto_popup}+{x}+{y}")
            popup.minsize(ancho_popup, alto_popup)
            popup.resizable(True, True)
            popup.transient(self)
            popup.configure(fg_color="white")

            try:
                imagen_fondo = Ctk.CTkImage(Image.open(resource_path("./img/futebol.jpg")), size=(ancho_popup, alto_popup))
                label_fondo = Ctk.CTkLabel(popup, image=imagen_fondo, text="")
                label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception:
                label_fondo = Ctk.CTkLabel(popup, text="")
                label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

            frame_texto = Ctk.CTkFrame(popup, fg_color="white")
            frame_texto.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.8)

            Ctk.CTkLabel(
                frame_texto,
                text="¡Has completado el juego!",
                font=Ctk.CTkFont(size=18, weight="bold"),
                text_color="black"
            ).pack(pady=(10, 10))

            frame_mensaje = Ctk.CTkFrame(frame_texto, fg_color="#CCCCCC")
            frame_mensaje.pack(padx=10, pady=(0, 10), fill="x")

            Ctk.CTkLabel(
                frame_mensaje,
                text="¡Felicidades! Has completado la alineación!",
                font=("Bebas Neue", 14),
                text_color="black",
                wraplength=400,
                justify="center"
            ).pack(padx=10, pady=10)

            def cerrar_todo():
                self.destroy()
                self.master.deiconify()
                popup.destroy()

            Ctk.CTkButton(
                popup,
                text="OK",
                command=cerrar_todo,
                width=120,
                fg_color=self.ROJO,
                hover_color="#D32F2F",
                font=self.FUENTE_MODERNA
            ).place(relx=0.5, rely=0.9, anchor="center")

            popup.update()
            popup.grab_set()
            popup.focus_force()
            popup.wait_window()
        finally:
            self.popup_activo = False

    def volver_al_menu(self):
        self.destroy()
        self.master.deiconify()