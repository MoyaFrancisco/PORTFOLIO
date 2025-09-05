import os
import sys
import customtkinter as ctk
from tkinter import messagebox
import db
import hashlib
from PIL import Image
from customtkinter import CTkFont

ROJO = "#B71C1C"

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login - Player 12")
        self.geometry("800x600")
        self.resizable(False, False)
        self.centrar_ventana()
        self.configure(fg_color="#002e71")

        # Cargar fuente personalizada
        self.fuente = CTkFont("font/Prompt-Regular.ttf", size=16)
        def resource_path(relative_path):
                    try:
                        base_path = sys._MEIPASS  # Carpeta temporal usada por PyInstaller
                    except AttributeError:
                        base_path = os.path.abspath(".")

                    return os.path.join(base_path, relative_path)
        # Fondo imagen campo de fútbol
        self.bg_image = ctk.CTkImage(Image.open(resource_path("img/campo.png")), size=(800, 600))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Título con fondo transparente
        self.label_title = ctk.CTkLabel(
            self,
            text="⚽ Player 12 ",
            font=("Prompt", 48, "bold"),
            text_color=ROJO,
            fg_color="white",
        )
        self.label_title.place(relx=0.5, rely=0.22, anchor="center")

        # Campo de usuario
        self.username_entry = ctk.CTkEntry(
            self,
            placeholder_text="Usuario",
            width=300,
            font=self.fuente,
            fg_color="white"
        )
        self.username_entry.place(relx=0.5, rely=0.38, anchor="center")

        # Campo de contraseña
        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Contraseña",
            show="*",
            width=300,
            font=self.fuente,
        )
        self.password_entry.place(relx=0.5, rely=0.46, anchor="center")

        # Botón de iniciar sesión
        self.login_button = ctk.CTkButton(
            self,
            text="Iniciar Sesión",
            fg_color=ROJO,
            hover_color="#d32f2f",
            font=self.fuente,
            command=self.login,
            width=200,
            bg_color="#0066a8"
        )
        self.login_button.place(relx=0.5, rely=0.56, anchor="center")

        # Botón de crear cuenta
        self.register_button = ctk.CTkButton(
            self,
            text="Crear Cuenta",
            fg_color=ROJO,
            hover_color="#d32f2f",
            font=self.fuente,
            command=self.registrar,
            width=200,
            bg_color="#3c8a3f"
        )
        self.register_button.place(relx=0.5, rely=0.63, anchor="center")

    def login(self):
        from Main import MainMenu
        usuario = self.username_entry.get()
        password = self.password_entry.get()
        if not usuario or not password:
            messagebox.showerror("Error", "Completa todos los campos.")
            return

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM usuarios WHERE username = %s", (usuario,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row and row[0] == hash_password(password):
            self.destroy()
            MainMenu().mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def registrar(self):
        usuario = self.username_entry.get()
        password = self.password_entry.get()
        if not usuario or not password:
            messagebox.showerror("Error", "Completa todos los campos.")
            return

        conn = db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)",
                           (usuario, hash_password(password)))
            conn.commit()
            messagebox.showinfo("Éxito", "Cuenta creada correctamente.")
        except:
            messagebox.showerror("Error", "El usuario ya existe.")
        finally:
            cursor.close()
            conn.close()

    def centrar_ventana(self):
        self.update_idletasks()  # Asegura que se conozcan el ancho y alto
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = LoginWindow()
    app.mainloop()