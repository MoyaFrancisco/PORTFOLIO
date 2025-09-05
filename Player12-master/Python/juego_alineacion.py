import customtkinter as Ctk
from tkinter import messagebox
import pymysql

# Configuración de CustomTkinter
Ctk.set_appearance_mode("System")  # Modo oscuro o claro según el sistema
Ctk.set_default_color_theme("blue")

# Paleta de colores inspirada en Futbol11.com
COLOR_FONDO = "#1E5631"  # Verde oscuro (césped)
COLOR_TEXTO = "#FFFFFF"  # Blanco
COLOR_BOTON = "#FFD700"  # Amarillo dorado
COLOR_JUGADOR = "#FFDD44"  # Amarillo suave
FUENTE_MODERNA = ("Bebas Neue", 16)

# Configuración de conexión a la base de datos
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "Player12"
}

# Distribución por formación
formacion = {
    "Portero": 1,
    "Defensa": 4,
    "Centrocampista": 3,
    "Delantero": 3
}

# Lista de posiciones ocupadas
alineacion = {
    "Portero": [],
    "Defensa": [],
    "Centrocampista": [],
    "Delantero": []
}

# Conectar a la base de datos y buscar jugador
def buscar_jugador(nombre):
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre, posicion FROM jugadores WHERE nombre = %s", (nombre,))
            resultado = cursor.fetchone()
            return resultado
    except pymysql.MySQLError as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la BD: {e}")
        return None
    finally:
        if 'connection' in locals():
            connection.close()

# Añadir jugador a la formación
def agregar_jugador():
    nombre = entry.get().strip()
    if not nombre:
        return

    resultado = buscar_jugador(nombre)
    if not resultado:
        messagebox.showwarning("No encontrado", f"No se encontró el jugador: {nombre}")
        entry.delete(0, Ctk.END)
        return

    apodo, posicion = resultado

    for pos in alineacion.values():
        if apodo in pos:
            messagebox.showinfo("Jugador repetido", f"{apodo} ya está en la alineación.")
            entry.delete(0, Ctk.END)
            return

    if posicion in alineacion and len(alineacion[posicion]) >= formacion[posicion]:
        messagebox.showinfo("Posición llena", f"La posición '{posicion}' ya está completa.")
        entry.delete(0, Ctk.END)
        return

    label = labels[posicion][len(alineacion[posicion])]
    label.configure(text=apodo, fg_color=COLOR_JUGADOR)
    alineacion[posicion].append(apodo)
    entry.delete(0, Ctk.END)

# Interfaz con CustomTkinter
ventana = Ctk.CTk()
ventana.title("Alineación 1-4-3-3")
ventana.geometry("800x600")
ventana.configure(bg_color=COLOR_FONDO)

labels = {
    "Portero": [],
    "Defensa": [],
    "Centrocampista": [],
    "Delantero": []
}

frame = Ctk.CTkFrame(ventana)
frame.pack(pady=20)

def crear_fila(posicion, cantidad):
    fila_frame = Ctk.CTkFrame(frame)
    fila_frame.pack(pady=10)

    for _ in range(cantidad):
        label = Ctk.CTkLabel(fila_frame, text="", width=100, height=50, fg_color="gray")
        label.pack(side="left", padx=10)
        labels[posicion].append(label)

crear_fila("Delantero", 3)
crear_fila("Centrocampista", 3)
crear_fila("Defensa", 4)
crear_fila("Portero", 1)

entry = Ctk.CTkEntry(ventana, width=300, font=FUENTE_MODERNA)
entry.pack(pady=10)

boton = Ctk.CTkButton(ventana, text="Agregar jugador", command=agregar_jugador, fg_color=COLOR_BOTON)
boton.pack(pady=20)

ventana.mainloop()