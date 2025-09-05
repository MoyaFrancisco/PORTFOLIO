import os
import sys
import customtkinter as ctk
from PIL import Image
from Wordle import WordleGame
from formateoNombres import obtener_nombre_jugador_formateado
from Alineacion import Alineacion
from login_window import LoginWindow
from bingo import Bingo
from Penaltis import Penaltis

# Colores y fuentes
FUENTE_MODERNA = ("Bebas Neue", 16)
FUENTE_TITULO = ("Bebas Neue", 48)
ROJO = "#B71C1C"
BLANCO = "#FFFFFF"
GRIS_CLARO = "#F0F0F0"
SOMBRA = "#E0E0E0"

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Player 12")
        self.resizable(False, False)
        self.geometry("1250x800")
        self.centrar_ventana(1250, 800)
        self.configure(fg_color=GRIS_CLARO)
        self.create_widgets()

    def create_widgets(self):
        def resource_path(relative_path):
                        try:
                            base_path = sys._MEIPASS  # Carpeta temporal usada por PyInstaller
                        except AttributeError:
                            base_path = os.path.abspath(".")
                        return os.path.join(base_path, relative_path)
                
        self.frame = ctk.CTkFrame(self, fg_color=GRIS_CLARO, corner_radius=0)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        try:
            self.img_izq = ctk.CTkImage(Image.open(resource_path("img/izquierda.png")), size=(250, 700))
            self.img_der = ctk.CTkImage(Image.open(resource_path("img/derecha.png")), size=(250, 700))
            self.icon_wordle = ctk.CTkImage(Image.open(resource_path("img/wordle.png")), size=(100, 100))
            self.icon_alineacion = ctk.CTkImage(Image.open(resource_path("img/alineacion.png")), size=(100, 100))
            self.icon_bingo = ctk.CTkImage(Image.open(resource_path("img/bingo.png")), size=(100, 100))
            self.icon_penaltis = ctk.CTkImage(Image.open(resource_path("img/imgpenaltis.png")), size=(100, 100))
        except Exception as e:
            print(f"Error al cargar imágenes: {e}")
            self.img_izq = self.img_der = self.icon_wordle = self.icon_alineacion = self.icon_bingo = self.icon_penaltis = None

        self.frame.columnconfigure((0, 1, 2), weight=1)

        if self.img_izq:
            ctk.CTkLabel(self.frame, image=self.img_izq, text="", fg_color=GRIS_CLARO).grid(row=0, column=0, sticky="ns")

        menu_frame = ctk.CTkFrame(self.frame, fg_color=BLANCO, corner_radius=20, border_color=SOMBRA, border_width=2)
        menu_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        title = ctk.CTkLabel(menu_frame, text="⚽ Player 12",
                             font=ctk.CTkFont(*FUENTE_TITULO, weight="bold"),
                             text_color=ROJO)
        title.pack(pady=30)

        juegos_frame = ctk.CTkFrame(menu_frame, fg_color=BLANCO)
        juegos_frame.pack(pady=20)

        juegos_frame.grid_columnconfigure((0, 1), weight=1)

        self.agregar_boton_juego(juegos_frame, self.icon_wordle, "Wordle", self.open_wordle).grid(row=0, column=0, padx=30, pady=20)
        self.agregar_boton_juego(juegos_frame, self.icon_alineacion, "Alineación", self.open_alineacion).grid(row=0, column=1, padx=30, pady=20)
        self.agregar_boton_juego(juegos_frame, self.icon_bingo, "Bingo", self.open_bingo).grid(row=1, column=0, padx=30, pady=20)
        self.agregar_boton_juego(juegos_frame, self.icon_penaltis, "Penaltis", self.open_penaltis).grid(row=1, column=1, padx=30, pady=20)

        opciones_frame = ctk.CTkFrame(menu_frame, fg_color=BLANCO)
        opciones_frame.pack(pady=(20, 10))

        self.crear_boton(opciones_frame, "Cerrar sesión", self.logout, ancho=140).pack(side="left", padx=10)
        self.crear_boton(opciones_frame, "Salir del juego", self.quit, ancho=140).pack(side="left", padx=10)

        if self.img_der:
            ctk.CTkLabel(self.frame, image=self.img_der, text="", fg_color=GRIS_CLARO).grid(row=0, column=2, sticky="ns")

    def agregar_boton_juego(self, parent, icono, texto, comando):
        frame = ctk.CTkFrame(parent, fg_color=BLANCO)
        if icono:
            icono_normal = icono
            icono_zoom = ctk.CTkImage(icono._light_image, size=(110, 110))

            borde = ctk.CTkFrame(frame, fg_color=ROJO, corner_radius=8)
            borde.pack(pady=5)
            img_lbl = ctk.CTkLabel(borde, image=icono_normal, text="", fg_color=BLANCO)
            img_lbl.pack(padx=3, pady=3)

        boton = self.crear_boton(frame, texto, comando)
        boton.pack(pady=(5, 10))

        def al_entrar(_):
            if icono:
                img_lbl.configure(image=icono_zoom)
            boton.configure(font=ctk.CTkFont("Bebas Neue", 26))

        def al_salir(_):
            if icono:
                img_lbl.configure(image=icono_normal)
            boton.configure(font=ctk.CTkFont("Bebas Neue", 22))

        if icono:
            img_lbl.bind("<Button-1>", lambda e: comando())
            img_lbl.bind("<Enter>", al_entrar)
            img_lbl.bind("<Leave>", al_salir)

        boton.bind("<Enter>", al_entrar)
        boton.bind("<Leave>", al_salir)

        return frame

    def crear_boton(self, parent, texto, comando, ancho=200):
        return ctk.CTkButton(parent, text=texto, width=ancho, height=50,
                            font=ctk.CTkFont("Bebas Neue", 22),
                            fg_color=ROJO,
                            hover_color="#d32f2f",
                            corner_radius=10,
                            command=comando)

    def open_wordle(self):
        self.withdraw()
        try:
            # WordleGame(self, secret_word=obtener_nombre_jugador_formateado())
            WordleGame(self, "courtois")
        except Exception as e:
            print(f"Error al abrir Wordle: {e}")
            self.deiconify()

    def open_alineacion(self):
        self.withdraw()
        try:
            Alineacion(self)
        except Exception as e:
            print(f"Error al abrir Alineación: {e}")
            self.deiconify()

    def open_bingo(self):
        self.withdraw()
        try:
            bingo_win = Bingo(self)
            bingo_win.grab_set()
        except Exception as e:
            print(f"Error al abrir Bingo: {e}")
            self.deiconify()

    def open_penaltis(self):
        self.withdraw()
        try:
            penaltis_win = Penaltis(self)
            penaltis_win.grab_set()  # hace la ventana modal
        except Exception as e:
            print(f"Error al abrir Penaltis: {e}")
            self.deiconify()

    def logout(self):
        self.destroy()
        LoginWindow().mainloop()

    def centrar_ventana(self, ancho, alto):
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("dark-blue")
    app = MainMenu()
    app.mainloop()