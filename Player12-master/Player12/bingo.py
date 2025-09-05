import os
import sys
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import random
import db

ROJO = "#B71C1C"

class Bingo(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Bingo de Equipos")
        self.geometry("900x700")
        self.configure(fg_color="#fff5f5")
        self.parent = parent

        self.jugadores = self.obtener_jugadores()
        self.escudos_usados = []
        self.celdas = []

        self.grid_frame = ctk.CTkFrame(self, fg_color="white")
        self.grid_frame.pack(pady=30)

        self.caja_frame = ctk.CTkFrame(self, fg_color="white")
        self.caja_frame.pack(pady=20)

        self.crear_cuadricula()
        self.crear_cajetilla()
        self.crear_boton_volver()

        self.protocol("WM_DELETE_WINDOW", self.volver_al_menu)

        self.after(100, self.centrar_ventana)
        self.after(200, self.mostrar_instrucciones)

    def centrar_ventana(self, ventana=None):
        ventana = ventana or self
        ventana.update_idletasks()
        w = ventana.winfo_width()
        h = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (w // 2)
        y = (ventana.winfo_screenheight() // 2) - (h // 2)
        ventana.geometry(f"{w}x{h}+{x}+{y}")

    def obtener_jugadores(self):
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, dorsal, equipo FROM jugadores")
        jugadores = cursor.fetchall()
        cursor.close()
        conn.close()
        random.shuffle(jugadores)
        return jugadores

    def obtener_equipos(self):
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, ruta_escudo FROM equipos")
        equipos = cursor.fetchall()
        cursor.close()
        conn.close()
        return equipos

    def crear_cuadricula(self):
        
        def resource_path(relative_path):
                try:
                    base_path = sys._MEIPASS  # Carpeta temporal usada por PyInstaller
                except AttributeError:
                    base_path = os.path.abspath(".")
                return os.path.join(base_path, relative_path)
            
        equipos = self.obtener_equipos()
        seleccionados = random.sample(equipos, 9)
        self.escudos_usados = [nombre for nombre, _ in seleccionados]

        for i in range(3):
            for j in range(3):
                nombre, ruta = seleccionados[i * 3 + j]
                img = ctk.CTkImage(Image.open(resource_path(ruta)), size=(100, 100))

                contenedor = ctk.CTkFrame(
                    self.grid_frame,
                    fg_color="white",
                    width=120,
                    height=120,
                    border_color=ROJO,
                    border_width=2,
                    corner_radius=15
                )
                contenedor.grid(row=i, column=j, padx=10, pady=10)

                label = ctk.CTkLabel(contenedor, image=img, text="")
                label.image_ref = img
                label.pack(padx=10, pady=10)

                label.bind("<Button-1>", lambda e, equipo=nombre, lbl=label: self.tachar_equipo(equipo, lbl))
                label.bind("<Enter>", lambda e, lbl=label: lbl.configure(cursor="hand2"))
                label.bind("<Leave>", lambda e, lbl=label: lbl.configure(cursor=""))

                self.celdas.append({"equipo": nombre, "label": label, "tachado": False})

    def crear_cajetilla(self):
        self.info_label = ctk.CTkLabel(
            self.caja_frame,
            text="",
            font=ctk.CTkFont("Arial", 20, "bold"),
            text_color=ROJO
        )
        self.info_label.pack(side="left", padx=10)

        self.skip_btn = ctk.CTkButton(
            self.caja_frame,
            text="⏭️ Saltar",
            command=self.siguiente_jugador,
            fg_color=ROJO,
            hover_color="#c62828",
            corner_radius=10,
            font=ctk.CTkFont("Arial", 16)
        )
        self.skip_btn.pack(side="left", padx=10)

        self.siguiente_jugador()

    def crear_boton_volver(self):
        self.boton_volver = ctk.CTkButton(
            self,
            text="⬅️ Volver al menú",
            command=self.volver_al_menu,
            fg_color=ROJO,
            hover_color="#c62828",
            font=ctk.CTkFont("Arial", 16),
            corner_radius=10
        )
        self.boton_volver.pack(pady=10)

    def siguiente_jugador(self):
        if not self.jugadores:
            self.info_label.configure(text="No hay más jugadores.")
            self.skip_btn.configure(state="disabled")
            return
        self.jugador_actual = self.jugadores.pop()
        nombre, dorsal, equipo = self.jugador_actual
        self.info_label.configure(text=f"{nombre}  |  #{equipo} ")

    def tachar_equipo(self, equipo, label):
        if not hasattr(self, "jugador_actual"):
            return

        _, _, equipo_jugador = self.jugador_actual
        if equipo == equipo_jugador:
            for celda in self.celdas:
                if celda["equipo"] == equipo and not celda["tachado"]:
                    celda["label"].configure(fg_color=ROJO)
                    celda["tachado"] = True
                    break
            if all(c["tachado"] for c in self.celdas):
                messagebox.showinfo("¡Ganaste!", "¡Has completado el bingo!")
                self.on_close()
            else:
                self.siguiente_jugador()
        else:
            messagebox.showwarning("Error", "Este escudo no corresponde al jugador actual.")

    def mostrar_instrucciones(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Cómo jugar")
        popup.geometry("500x400")
        popup.configure(fg_color="white")
        popup.resizable(False, False)

        ctk.CTkLabel(
            popup,
            text="INSTRUCCIONES DEL JUEGO:",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#b71c1c"
        ).pack(pady=(20, 10))

        frame_texto = ctk.CTkFrame(popup, fg_color="white")
        frame_texto.pack(padx=20, pady=10, fill="both", expand=True)

        ctk.CTkLabel(
            frame_texto,
            text="Haz clic sobre el escudo del equipo al que pertenece el jugador mostrado.",
            font=ctk.CTkFont(size=16),
            text_color="black",
            anchor="w",
            justify="left",
            wraplength=440
        ).pack(anchor="w", pady=5)

        for simbolo, color, texto in [
            ("✔️", "#4CAF50", "Si aciertas, el escudo se marcará automáticamente y pasarás al siguiente jugador."),
            ("❌", "#F44336", "Si te equivocas, no pasa nada."),
            ("⏭️", "#e9c706", "Puedes usar el botón 'Saltar' para avanzar sin marcar.")
        ]:
            linea = ctk.CTkFrame(frame_texto, fg_color="white")
            linea.pack(anchor="w", pady=5)
            ctk.CTkLabel(linea, text=simbolo, text_color=color, font=ctk.CTkFont(size=16)).pack(side="left")
            ctk.CTkLabel(linea, text=texto, text_color="black", font=ctk.CTkFont(size=16),
                         wraplength=400, justify="left").pack(side="left")

        ctk.CTkLabel(
            frame_texto,
            text="¡Completa los 9 escudos para ganar el juego!",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#b71c1c",
            anchor="w"
        ).pack(anchor="w", pady=(10, 0))

        ctk.CTkButton(
            popup,
            text="Entendido",
            command=popup.destroy,
            width=120,
            fg_color="#b71c1c",
            hover_color="#d32f2f"
        ).pack(pady=20)

        popup.grab_set()
        self.centrar_ventana(popup)

    def volver_al_menu(self):
        self.destroy()
        self.master.deiconify()

    def on_close(self):
        self.volver_al_menu()