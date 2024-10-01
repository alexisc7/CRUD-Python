from funciones import (crear_registro, obtener_registro, obtener_todos_los_registros,
                       actualizar_registro, eliminar_registro)

def mostrar_menu():
    print("""
--- Sistema CRUD ---
[1] Crear un registro 
[2] Obtener un registro
[3] Obtener todos los registros
[4] Actualizar un registro
[5] Borrar un registro
[6] Salir del CRUD
""")

def ejecutar_opcion(opcion):
    match opcion:
        case "1": 
            crear_registro()
        case "2": 
            obtener_registro()
        case "3": 
            obtener_todos_los_registros()
        case "4": 
            actualizar_registro()
        case "5": 
            eliminar_registro()
        case "6":
            print("Saliendo del CRUD...")
            return False
    return True

def main():
    continuar = True
    while continuar:
        mostrar_menu()
        opcion = input("Ingresa una opción: ") 
        if opcion.isnumeric() and 1 <= int(opcion) <= 6:
            continuar = ejecutar_opcion(opcion)
        else:
            print("ERROR: Ingresa una opción entre 1 y 6.")

if __name__ == "__main__":
    main()
