from crear_turno import crear_turno
from eliminar_turno import eliminar_turno
from actualizar_turno import actualizar_turno
from consultar_turnos_medico import consultar_turnos_medico
from crear_usuario import crear_usuario
from auth import login

# Importar el módulo completo
import consultar_turno as consultar_turno_mod

def menu_inicio():
    print('- Bienvenido al Sistema de Gestión de Turnos -')

    # --- LOGIN ---
    user = None
    intentos = 3
    while intentos > 0 and not user:
        username = input("Usuario: ").strip()
        pwd = input("Contraseña: ").strip()
        user = login(username, pwd)
        if not user:
            intentos -= 1
            print(f"Credenciales inválidas. Intentos restantes: {intentos}")
    if not user:
        print("Fin de sesión.")
        return

    rol = user["rol"]
    print(f"Hola, {user['username']} (rol: {rol})")

    # --- Menús por rol ---
    while True:
        print("\nSeleccione una opción:")

        if user["es_admin"] or user["es_empleado"]:
            print('1. Crear Turno')
            print('2. Consultar Turno')
            print('3. Actualizar Turno')
            print('4. Eliminar Turno')
            print('5. Crear Usuario')
            print('0. Salir')
            opciones_validas = {0,1,2,3,4,5}

        elif user["es_medico"]:
            print('1. Consultar mis turnos (por especialidad)')
            print('0. Salir')
            opciones_validas = {0,1}

        else:  # paciente
            print('1. Consultar mis turnos')
            print('0. Salir')
            opciones_validas = {0,1}

        # leer opción
        while True:
            try:
                opt = int(input("> "))
                if opt in opciones_validas:
                    break
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Ingrese un número válido.")

        # caminos por rol
        if user["es_admin"] or user["es_empleado"]:
            if opt == 0:
                print('Hasta luego, gracias por confiar en InstaTurno.')
                break
            elif opt == 1:
                crear_turno()
                input("\nENTER para volver al menú...")
            elif opt == 2:
                # Pasamos el usuario 
                consultar_turno_mod.consultar_turno(user)
                input("\nENTER para volver al menú...")
            elif opt == 3:
                actualizar_turno()
                input("\nENTER para volver al menú...")
            elif opt == 4:
                eliminar_turno()
                input("\nENTER para volver al menú...")
            elif opt == 5:
                if user["es_admin"]:
                    crear_usuario()
                else:
                    print("Solo un admin puede crear usuarios.")
                input("\nENTER para volver al menú...")

        elif user["es_medico"]:
            if opt == 0:
                print('Hasta luego, gracias por confiar en InstaTurno.')
                break
            elif opt == 1:
                consultar_turnos_medico(user["id_usuario"])
                input("\nENTER para volver al menú...")

        else:  # paciente
            if opt == 0:
                print('Hasta luego, gracias por confiar en InstaTurno.')
                break
            elif opt == 1:
                # 🔑 Esto hace que el paciente vea SOLO sus turnos
                consultar_turno_mod.consultar_turno(user)
                input("\nENTER para volver al menú...")

# Main
if __name__ == "__main__":
    menu_inicio()
