import os
import customtkinter as ctk
from tkinter import messagebox

# Configuración inicial
MAX_ATTEMPTS = 6

COLOR_CORRECT = "#4CAF50"
COLOR_PRESENT = "#FFEB3B"
COLOR_ABSENT = "#F44336"
COLOR_EMPTY = "#CCCCCC"
TEXT_COLOR = "#FFFFFF"
TEXT_COLOR_DARK = "#000000"

class WordleGame(ctk.CTkToplevel):
    def __init__(self, parent, secret_word):
        super().__init__(parent)
        self.secret_word = secret_word.upper()
        self.word_length = len(self.secret_word)
        self.attempts = 0
        self.grid_cells = []
        self.letras_usadas = {}  # Guardar estado de cada letra

        self.title("Player 12 - Adivina el jugador ")

        LETRA_ANCHO = 125
        ESPACIADO = 100
        ancho_total = (LETRA_ANCHO * len(secret_word)) + ESPACIADO
        self.geometry(f"{ancho_total}x1200")

        self.configure(bg="white")
        self.create_layout()
        self.mostrar_instrucciones()

        self.centrar_ventana()
        self.protocol("WM_DELETE_WINDOW", self.volver_al_menu)

    def resource_path(relative_path):
        """Devuelve el path absoluto, compatible con PyInstaller."""
        try:
            base_path = sys._MEIPASS  # Carpeta temporal usada por PyInstaller
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def create_layout(self):
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.pack(expand=True)

        self.title_label = ctk.CTkLabel(self.container, text="⚽ Player 12 - Adivina el Jugador",
                                        font=ctk.CTkFont(size=36, weight="bold"),
                                        text_color="#b71c1c")
        self.title_label.pack(pady=40)

        self.frame_grid = ctk.CTkFrame(self.container, fg_color="white")
        self.frame_grid.pack(pady=(20, 10))

        # ⚽ TECLADO VIRTUAL entre la cuadrícula y el input
        self.keyboard_frame = ctk.CTkFrame(self.container, fg_color="white")
        self.keyboard_frame.pack(pady=10)
        self.render_keyboard()

        for row in range(MAX_ATTEMPTS):
            row_cells = []
            for col in range(self.word_length):
                lbl = ctk.CTkLabel(self.frame_grid, text="", width=70, height=70,
                                   fg_color=COLOR_EMPTY, text_color=TEXT_COLOR_DARK,
                                   font=ctk.CTkFont(size=32, weight="bold"),
                                   corner_radius=10)
                lbl.grid(row=row, column=col, padx=6, pady=6)
                row_cells.append(lbl)
            self.grid_cells.append(row_cells)

        self.entry = ctk.CTkEntry(self.container,
                                  placeholder_text="Nombre del jugador...",
                                  width=400,
                                  font=ctk.CTkFont(size=24),
                                  fg_color="white",
                                  text_color=TEXT_COLOR_DARK)
        self.entry.pack(pady=(10, 5))
        self.entry.focus()
        self.entry.bind("<Return>", lambda event: self.check_word())

        self.btn_submit = ctk.CTkButton(self.container, text="Probar",
                                        width=150, height=50,
                                        font=ctk.CTkFont(size=20),
                                        fg_color="#b71c1c",
                                        hover_color="#d32f2f",
                                        command=self.check_word)
        self.btn_submit.pack(pady=(0, 5))

        self.btn_exit = ctk.CTkButton(self.container, text="Volver al menú",
                                      width=150, height=40,
                                      font=ctk.CTkFont(size=16),
                                      fg_color="#777",
                                      hover_color="#999",
                                      command=self.volver_al_menu)
        self.btn_exit.pack(pady=(0, 10))

    def check_word(self):
        word = self.entry.get().strip().upper()

        if len(word) > self.word_length or not word.isalpha():
            messagebox.showerror("Error", f"Máximo {self.word_length} letras. Solo letras.")
            return
        if self.attempts >= MAX_ATTEMPTS:
            messagebox.showinfo("Fin del juego", f"Has perdido. El jugador era: {self.secret_word}")
            return

        word = word.ljust(self.word_length)
        secret_word_list = list(self.secret_word)
        guess_result = ["absent"] * self.word_length

        for i in range(self.word_length):
            if word[i] == self.secret_word[i]:
                guess_result[i] = "correct"
                secret_word_list[i] = None

        for i in range(self.word_length):
            if guess_result[i] == "correct":
                continue
            if word[i] in secret_word_list and word[i] != " ":
                guess_result[i] = "present"
                secret_word_list[secret_word_list.index(word[i])] = None

        for i in range(self.word_length):
            letra = word[i]
            lbl = self.grid_cells[self.attempts][i]
            lbl.configure(text=letra if letra != " " else "")

            if guess_result[i] == "correct":
                lbl.configure(fg_color=COLOR_CORRECT, text_color=TEXT_COLOR)
                self.letras_usadas[letra] = "correct"
            elif guess_result[i] == "present":
                lbl.configure(fg_color=COLOR_PRESENT, text_color=TEXT_COLOR_DARK)
                if self.letras_usadas.get(letra) != "correct":
                    self.letras_usadas[letra] = "present"
            else:
                lbl.configure(fg_color=COLOR_ABSENT, text_color=TEXT_COLOR)
                if letra not in self.letras_usadas:
                    self.letras_usadas[letra] = "absent"

        self.render_keyboard()
        self.attempts += 1
        self.entry.delete(0, ctk.END)

        if word.strip() == self.secret_word:
            messagebox.showinfo("¡Felicidades!", f"¡Adivinaste a {self.secret_word}!")
            self.entry.configure(state="disabled")
            self.btn_submit.configure(state="disabled")
        elif self.attempts >= MAX_ATTEMPTS:
            messagebox.showinfo("Fin del juego", f"Has perdido. El jugador era: {self.secret_word}")
            self.entry.configure(state="disabled")
            self.btn_submit.configure(state="disabled")

    def render_keyboard(self):
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()

        letras = "QWERTYUIOPASDFGHJKLZXCVBNM"
        filas = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

        for fila in filas:
            fila_frame = ctk.CTkFrame(self.keyboard_frame, fg_color="white")
            fila_frame.pack(pady=3)
            for letra in fila:
                estado = self.letras_usadas.get(letra, "unused")
                color = {
                    "correct": COLOR_CORRECT,
                    "present": COLOR_PRESENT,
                    "absent": COLOR_ABSENT,
                    "unused": COLOR_EMPTY
                }[estado]
                txt_color = TEXT_COLOR_DARK if estado == "present" else TEXT_COLOR
                btn = ctk.CTkLabel(fila_frame, text=letra, width=40, height=40,
                                   fg_color=color,
                                   text_color=txt_color,
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   corner_radius=6)
                btn.pack(side="left", padx=3)

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
            text="Adivina el nombre del jugador siguiendo estas pautas:",
            font=ctk.CTkFont(size=16),
            text_color="black",
            anchor="w"
        ).pack(anchor="w")

        # Línea 1
        ctk.CTkLabel(
            frame_texto,
            text="  ✅ Letra en la posición correcta:",
            font=ctk.CTkFont(size=16),
            text_color="black",
            anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            frame_texto,
            text="  Verde",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50"
        ).pack(anchor="w", padx=20)

        # Línea 2
        ctk.CTkLabel(
            frame_texto,
            text="  🟡 Letra en otra posición:",
            font=ctk.CTkFont(size=16),
            text_color="black",
            anchor="w"
        ).pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(
            frame_texto,
            text="  Amarillo",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#e9c706"
        ).pack(anchor="w", padx=20)

        # Línea 3
        ctk.CTkLabel(
            frame_texto,
            text="  ❌ Letra incorrecta:",
            font=ctk.CTkFont(size=16),
            text_color="black",
            anchor="w"
        ).pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(
            frame_texto,
            text="  Rojo",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#F44336"
        ).pack(anchor="w", padx=20)

        # Línea final
        ctk.CTkLabel(
            popup,
            text=f"Tienes {MAX_ATTEMPTS} intentos. ¡Suerte!",
            font=ctk.CTkFont(size=16),
            text_color="black"
        ).pack(pady=(10, 0))

        ctk.CTkButton(
            popup,
            text="Entendido",
            command=popup.destroy,
            width=120,
            fg_color="#b71c1c",
            hover_color="#d32f2f"
        ).pack(pady=20)

        popup.grab_set()

    def centrar_ventana(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def volver_al_menu(self):
        self.destroy()
        self.master.deiconify()
