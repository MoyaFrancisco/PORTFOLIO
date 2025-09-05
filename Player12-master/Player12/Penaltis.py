import os
import sys
import customtkinter
import random
from customtkinter import CTkImage
from PIL import Image

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class Penaltis(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # Tamaño fijo
        ancho_ventana = 700
        alto_ventana = 700

        # Obtener tamaño de pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Calcular posición centrada
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        # Aplicar geometría centrada
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")


        self.title("Juego de Penaltis")
        self.resizable(False, False)
        self.configure(fg_color="#5f9501")

        self.font_title = customtkinter.CTkFont(family="Bebas Neue", size=30)
        self.font_text = customtkinter.CTkFont(family="Bebas Neue", size=22)

        self.modo_juego = None
        self.turno_actual = None
        self.penaltis_j1 = 0
        self.penaltis_j2 = 0
        self.goles_j1 = 0
        self.goles_j2 = 0
        self.tiro_j1 = ""
        self.tiro_j2 = ""
        self.turno_activo = True

        # Cargar imágenes
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS  # Carpeta temporal usada por PyInstaller
            except AttributeError:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)
        self.imgs_porteria = {
            "Izquierda": CTkImage(Image.open(resource_path("img\port_izquierda.jpg")), size=(208, 626)),
            "Centro": CTkImage(Image.open(resource_path("img\port_centro.jpg")), size=(208, 626)),
            "Derecha": CTkImage(Image.open(resource_path("img\port_derecha.jpg")), size=(208, 626)),
        }

        self.mostrar_menu()

    def mostrar_menu(self):
        self.clear_screen()

        titulo = customtkinter.CTkLabel(self, text="Selecciona el modo de juego", font=self.font_title, text_color="white")
        titulo.pack(pady=40)

        boton_multi = customtkinter.CTkButton(self, text="2 Jugadores (local)", font=self.font_text,
                                              corner_radius=25, width=200, command=self.iniciar_multijugador)
        boton_multi.pack(pady=10)

        boton_ia = customtkinter.CTkButton(self, text="Contra la IA", font=self.font_text,
                                           corner_radius=25, width=200, command=self.iniciar_contra_ia)
        boton_ia.pack(pady=10)
        
        boton_volver = customtkinter.CTkButton(self, text="Volver al Menú Principal", font=self.font_text,
                                               corner_radius=25, width=200, command=self.volver_al_menu)
        boton_volver.pack(pady=30)

    def mostrar_instrucciones(self, modo):
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS  # Carpeta temporal usada por PyInstaller
            except AttributeError:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        popup = customtkinter.CTkToplevel(self)
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
            imagen_fondo = customtkinter.CTkImage(Image.open(resource_path("./img/futebol.jpg")), size=(700, 500))
            label_fondo = customtkinter.CTkLabel(popup, image=imagen_fondo, text="")
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            label_fondo = customtkinter.CTkLabel(popup, text="")
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        frame_texto = customtkinter.CTkFrame(popup, fg_color="white")
        frame_texto.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.8)

        customtkinter.CTkLabel(
            frame_texto,
            text="INSTRUCCIONES DEL JUEGO:",
            font=customtkinter.CTkFont(size=20, weight="bold"),
            text_color="black"
        ).pack(pady=(10, 10))

        instrucciones = ""
        if modo == "MULTI":
            instrucciones = (
                """1. El juego es por turnos: primero lanza el Jugador 1, luego el Jugador 2.

2. Cada jugador debe elegir una zona para lanzar (Izquierda, Centro o Derecha) y luego atajar el disparo del rival.

3. Para tirar, haz clic sobre la parte de la portería donde quieres lanzar.

4. Cuando te toque atajar, también deberás hacer clic en la zona donde crees que el rival va a disparar.

5. Si el portero y el tiro coinciden, ¡es parada! Si no, ¡es gol!

6. Cada jugador lanza 5 penaltis. Gana el que más goles marque.
""" )
            
        elif modo == "IA":
            instrucciones = ("""
1. Juegas como Jugador 1. La IA será tu oponente (Jugador 2).

2. En tu turno, elige una zona para disparar: Izquierda, Centro o Derecha.

3. La IA intentará adivinar tu disparo. Si acierta, ataja el penalti; si no, es gol.

4. Luego la IA tirará y tú deberás elegir una zona para atajar su tiro.

5. El sistema te mostrará el resultado de cada jugada (gol, parada, fallo).

6. Ambos lanzan 5 penaltis. Gana quien más goles marque.
""" )

        textbox = customtkinter.CTkTextbox(
            frame_texto,
            wrap="word",
            font=("Bebas Neue", 16),
            fg_color="white",
            text_color="black"
        )
        textbox.pack(expand=True, fill="both", padx=10, pady=(0, 10))
        textbox.insert("0.0", instrucciones)
        textbox.configure(state="disabled")

        customtkinter.CTkButton(
            popup,
            text="Entendido",
            command=popup.destroy,
            width=140,
            fg_color="#D32F2F",
            bg_color="#5f9501",
            hover_color="#C62828"
        ).place(relx=0.5, rely=0.9, anchor="center")

        popup.update()
        popup.grab_set()
        popup.wait_window()


    def iniciar_multijugador(self):
        self.mostrar_instrucciones("MULTI")
        self.modo_juego = "MULTI"
        self.reset_estado()
        self.mostrar_controles()
        self.crear_porteria()

    def iniciar_contra_ia(self):
        self.mostrar_instrucciones("IA")
        self.modo_juego = "IA"
        self.reset_estado()
        self.mostrar_controles()
        self.crear_porteria()

    def reset_estado(self):
        self.turno_actual = "J1_TIRA"
        self.penaltis_j1 = 0
        self.penaltis_j2 = 0
        self.goles_j1 = 0
        self.goles_j2 = 0
        self.tiro_j1 = ""
        self.tiro_j2 = ""
        self.turno_activo = True
        self.clear_screen()

    def mostrar_controles(self):
        self.turno_label = customtkinter.CTkLabel(self, text="Turno: Jugador 1 tira", font=self.font_text, text_color="white")
        self.turno_label.pack(pady=10)

        self.contador_label = customtkinter.CTkLabel(self, text=self.obtener_contadores(), font=self.font_text, text_color="white")
        self.contador_label.pack(pady=10)

        volver = customtkinter.CTkButton(self, text="Ir atrás", font=self.font_text,
                                         corner_radius=25, command=self.mostrar_menu)
        volver.pack(pady=10)

    def obtener_contadores(self):
        nombre_j2 = "IA" if self.modo_juego == "IA" else "Jugador 2"
        return f"Jugador 1: {self.penaltis_j1}/5   {nombre_j2}: {self.penaltis_j2}/5"

    def crear_porteria(self):
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS  # Carpeta temporal usada por PyInstaller
            except AttributeError:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        self.porteria_frame = customtkinter.CTkFrame(self, fg_color="#447300", corner_radius=20)
        self.porteria_frame.pack(pady=20)

        self.etiquetas_porteria = {}  # Guardar referencias para efectos

        posiciones = ["Izquierda", "Centro", "Derecha"]
        for i, pos in enumerate(posiciones):
            img_normal = CTkImage(Image.open(resource_path(f"img/port_{pos.lower()}.jpg")), size=(208, 626))
            img_zoom = CTkImage(Image.open(resource_path(f"img/port_{pos.lower()}.jpg")), size=(228, 646))

            etiqueta = customtkinter.CTkLabel(self.porteria_frame, image=img_normal, text="")
            etiqueta.grid(row=0, column=i, padx=10)
            etiqueta.bind("<Enter>", lambda e, p=pos, l=etiqueta: self.hover_on(p, l))
            etiqueta.bind("<Leave>", lambda e, p=pos, l=etiqueta: self.hover_off(p, l))
            etiqueta.bind("<Button-1>", lambda e, p=pos, l=etiqueta: self.click_porteria(p, l))

            self.etiquetas_porteria[pos] = {
                "label": etiqueta,
                "normal": img_normal,
                "zoom": img_zoom
            }
    def hover_on(self, pos, label):
        label.configure(image=self.etiquetas_porteria[pos]["zoom"])

    def hover_off(self, pos, label):
        label.configure(image=self.etiquetas_porteria[pos]["normal"])

    def click_porteria(self, pos, label):
        # Simular clic bajando opacidad de la imagen brevemente
        original_image = self.etiquetas_porteria[pos]["normal"]
        def resource_path(relative_path):
                try:
                    base_path = sys._MEIPASS  # Carpeta temporal usada por PyInstaller
                except AttributeError:
                    base_path = os.path.abspath(".")

                return os.path.join(base_path, relative_path)
        # Crear una versión oscurecida temporalmente
        image_path = f"img/port_{pos.lower()}.jpg"
        imagen_click = Image.open((resource_path(f"img/port_{pos.lower()}.jpg"))).convert("RGBA")
        overlay = Image.new("RGBA", imagen_click.size, (0, 0, 0, 80))  # capa semitransparente
        imagen_click.paste(overlay, (0, 0), overlay)
        img_temporal = CTkImage(imagen_click, size=(208, 626))

        label.configure(image=img_temporal)
        self.after(150, lambda: label.configure(image=original_image))  # restaurar imagen
        self.seleccionar_posicion(pos)


    def seleccionar_posicion(self, eleccion):
        if not self.turno_activo:
            return
        self.turno_activo = False

        if self.modo_juego == "MULTI":
            if self.turno_actual == "J1_TIRA":
                self.tiro_j1 = eleccion
                self.turno_label.configure(text="Turno: Jugador 2 ataja")
                self.turno_actual = "J2_ATAJA"
                self.turno_activo = True

            elif self.turno_actual == "J2_ATAJA":
                resultado = "¡Jugador 1 falló!" if self.tiro_j1 == eleccion else "¡Gol de Jugador 1!"
                if "Gol" in resultado:
                    self.goles_j1 += 1
                self.penaltis_j1 += 1
                self.verificar_fin(resultado)

            elif self.turno_actual == "J2_TIRA":
                self.tiro_j2 = eleccion
                self.turno_label.configure(text="Turno: Jugador 1 ataja")
                self.turno_actual = "J1_ATAJA"
                self.turno_activo = True

            elif self.turno_actual == "J1_ATAJA":
                resultado = "¡Jugador 2 falló!" if self.tiro_j2 == eleccion else "¡Gol de Jugador 2!"
                if "Gol" in resultado:
                    self.goles_j2 += 1
                self.penaltis_j2 += 1
                self.verificar_fin(resultado)

        elif self.modo_juego == "IA":
            if self.turno_actual == "J1_TIRA":
                self.tiro_j1 = eleccion
                ia_ataja = random.choice(["Izquierda", "Centro", "Derecha"])
                resultado = "¡La IA atajó!" if ia_ataja == self.tiro_j1 else "¡Gol del Jugador!"
                if "Gol" in resultado:
                    self.goles_j1 += 1
                self.penaltis_j1 += 1
                self.verificar_fin(resultado)
                self.after(2500, self.turno_ia_dispara)

            elif self.turno_actual == "J2_TIRA":
                self.tiro_j2 = random.choice(["Izquierda", "Centro", "Derecha"])
                resultado = "¡Has atajado el tiro de la IA!" if eleccion == self.tiro_j2 else "¡Gol de la IA!"
                if "Gol" in resultado:
                    self.goles_j2 += 1
                self.penaltis_j2 += 1
                self.verificar_fin(resultado)
                self.after(2500, self.turno_jugador_dispara)

    def turno_ia_dispara(self):
        self.turno_actual = "J2_TIRA"
        self.turno_label.configure(text="Turno: Elige dónde atajar a la IA")
        self.turno_activo = True

    def turno_jugador_dispara(self):
        self.turno_actual = "J1_TIRA"
        self.turno_label.configure(text="Turno: Elige dónde tirar")
        self.turno_activo = True

    def verificar_fin(self, resultado):
        self.turno_label.configure(text=resultado)
        self.contador_label.configure(text=self.obtener_contadores())

        if self.penaltis_j1 == 5 and self.penaltis_j2 == 5:
            self.finalizar_partido()
        elif self.modo_juego == "MULTI":
            self.after(2500, self.siguiente_turno)

    def siguiente_turno(self):
        if self.penaltis_j1 + self.penaltis_j2 < 10 and self.modo_juego == "MULTI":
            if (self.penaltis_j1 + self.penaltis_j2) % 2 == 0:
                self.turno_actual = "J1_TIRA"
                self.turno_label.configure(text="Turno: Jugador 1 tira")
            else:
                self.turno_actual = "J2_TIRA"
                self.turno_label.configure(text="Turno: Jugador 2 tira")
            self.turno_activo = True

    def finalizar_partido(self):
        self.porteria_frame.destroy()
        nombre_j2 = "IA" if self.modo_juego == "IA" else "Jugador 2"
        resultado_final = f"Goles Jugador 1: {self.goles_j1}\nGoles {nombre_j2}: {self.goles_j2}\n"
        if self.goles_j1 > self.goles_j2:
            resultado_final += f"¡Ganador: Jugador 1!"
        elif self.goles_j2 > self.goles_j1:
            resultado_final += f"¡Ganador: {nombre_j2}!"
        else:
            resultado_final += "¡Empate!"

        self.turno_label.configure(text="")
        self.contador_label.configure(text="")
        resumen = customtkinter.CTkLabel(self, text=resultado_final, font=self.font_text, text_color="white")
        resumen.pack(pady=40)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def volver_al_menu(self):
        self.destroy()
        self.master.deiconify()

if __name__ == "__main__":
    app = Penaltis()
    app.mainloop()