import sqlite3


def gestionar_conexion(func):
    def wrapper(*args, **kwargs):
        db, cursor = None, None
        try:
            db = sqlite3.connect("crud.db")
            cursor = db.cursor()
            result = func(cursor, *args, **kwargs) # Ejecuta la función con la conexión
            db.commit()  # Guarda los cambios si la operación fue exitosa
            return result
        except ValueError:
            print("ERROR: El ID debe ser numérico.")
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")
        except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
            print(f"Error operativo de la base de datos: {e}")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            if cursor:
                cursor.close()  # Asegurar el cierre del cursor
            if db:
                db.close()  # Asegurar el cierre de la conexión a la BBDD
   
    return wrapper


def validar_data(nombre: str, apellido: str):
    return (nombre.isalpha() and 3 <= len(nombre) <= 50 and 
            apellido.isalpha() and 3 <= len(apellido) <= 50)


@gestionar_conexion
def crear_registro(cursor):
    nombre = input("Ingresa un nombre: ")
    apellido = input("Ingresa un apellido: ")

    # Validar datos de entrada
    if validar_data(nombre, apellido):
        cursor.execute(
            "INSERT INTO Persona(nombre, apellido) VALUES (?, ?)",
            (nombre, apellido)
        )
        print(f"{nombre} {apellido} añadido con éxito!")
    else:
        print("ERROR: Ingresa los datos correctamente.")


@gestionar_conexion
def obtener_registro(cursor): 
    id = int(input("Ingresa el ID: "))

    if id > 0:
        cursor.execute("SELECT * FROM Persona WHERE id = ?", (id,))
        registro = cursor.fetchone()
        if registro is not None:
            print(f"Datos: {registro}")
            return registro
        else:
            print("No existen datos relacionados al ID ingresado.")
    else:
        print("ERROR: El ID debe ser mayor a 0.")


@gestionar_conexion
def obtener_todos_los_registros(cursor):
    cursor.execute("SELECT * FROM Persona")
    registros = cursor.fetchall()  
    if registros: 
        print("Todos los registros:")
        for registro in registros:
            print(registro)
        return registros  # Devolver los registros si se requiere más adelante
    else:
        print("No hay registros en la tabla.")


@gestionar_conexion
def actualizar_registro(cursor):
    registro = obtener_registro()  
    if registro:
        nombre = input("Ingresa el nuevo nombre: ")
        apellido = input("Ingresa el nuevo apellido: ")

        if validar_data(nombre, apellido):
            cursor.execute(
                "UPDATE Persona SET nombre = ?, apellido = ? WHERE id = ?",
                (nombre, apellido, registro[0])
            )
            print("Registro actualizado con éxito.")
        else:
            print("ERROR: Ingresa los datos correctamente.")


@gestionar_conexion
def eliminar_registro(cursor):
    registro = obtener_registro() 
    if registro:
        confirmacion = input(f"¿Estás seguro de que deseas eliminar el registro {registro}? (s/n): ")
        if confirmacion.lower() == 's':
            cursor.execute("DELETE FROM Persona WHERE id = ?", (registro[0],))
            print("Registro eliminado con éxito.")
        else:
            print("Operación cancelada.")