import mysql.connector
import random
import unicodedata

def quitar_tildes(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def obtener_nombre_jugador_formateado():
    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Player12"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM jugadores")
    nombres = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    conn.close()

    while True:
        nombre_original = random.choice(nombres).strip()

        if "." in nombre_original and " " not in nombre_original:
            partes = nombre_original.split(".")
            if len(partes) >= 2 and partes[1]:
                nombre_formateado = partes[1].strip()
                break
            else:
                continue

        elif "." in nombre_original and " " in nombre_original:
            partes = nombre_original.split()
            if len(partes) == 2 and "." in partes[0]:
                nombre_formateado = partes[1].strip()
                break
            else:
                continue

        elif " " in nombre_original:
            nombre_formateado = nombre_original.replace(" ", "")
            break

        else:
            nombre_formateado = nombre_original
            break

    return quitar_tildes(nombre_formateado).lower()