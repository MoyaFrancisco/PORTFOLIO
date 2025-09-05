import pandas as pd
import pymysql

try:
    # Leer el CSV (ajustar codificación si da problemas, por ejemplo 'utf-8' o 'latin1')
    df = pd.read_csv("info_jugadores_la_liga(Sheet1).csv", encoding='latin1')

    # Conexión a la base de datos
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="Player12",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.Cursor
    )
    print("Conexión exitosa")

    with connection.cursor() as cursor:
        # Vaciar la tabla antes de insertar
        cursor.execute("TRUNCATE TABLE jugadores")

        insert_query = """
            INSERT INTO jugadores (nombre, dorsal, pais, posicion, equipo)
            VALUES (%s, %s, %s, %s, %s)
        """

        registros_insertados = 0

        for index, row in df.iterrows():
            try:
                # Omitimos si faltan columnas obligatorias
                if pd.isna(row["apodo"]) or pd.isna(row["pais"]) or pd.isna(row["posicion"]) or pd.isna(row["equipo"]):
                    print(f"Fila {index} omitida por valores nulos obligatorios.")
                    continue

                # Ejecutar insert
                cursor.execute(insert_query, (
                    row["apodo"],
                    row["dorsal"] if not pd.isna(row["dorsal"]) else None,
                    row["pais"],
                    row["posicion"],
                    row["equipo"]
                ))
                registros_insertados += 1

            except Exception as e:
                print(f"Error en fila {index}: {e}")

        connection.commit()
        print(f"{registros_insertados} registros insertados correctamente.")

except Exception as e:
    print(f"Error al conectar o insertar en MySQL: {e}")

finally:
    if 'connection' in locals() and connection.open:
        connection.close()
        print("Conexión cerrada")
