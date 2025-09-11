from crear_turno import crear_turno
from eliminar_turno import eliminar_turno
from actualizar_turno import actualizar_turno
from consultar_turnos_medico import consultar_turnos_medico
from crear_usuario import crear_usuario
from auth import login
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

        if user.get("es_admin"):
            # Admin: solo gestiona usuarios
            print('1. Crear Usuario')
            print('2. Ver Usuarios')
            print('3. Cambiar Permisos de Usuario')
            print('4. Eliminar Usuario')
            print('0. Salir')
            opciones_validas = {0,1,2,3,4}

        elif user.get("es_empleado"):
            # Empleado: gestiona turnos
            print('1. Crear Turno')
            print('2. Consultar Turno')
            print('3. Actualizar Turno')
            print('4. Eliminar Turno')
            print('0. Salir')
            opciones_validas = {0,1,2,3,4}

        elif user.get("es_medico"):
            # Médico: solo consulta sus turnos
            print('1. Consultar mis turnos (por especialidad)')
            print('0. Salir')
            opciones_validas = {0,1}

        else:
            # Paciente: CRUD solo de SUS turnos
            print('1. Crear MI Turno')
            print('2. Consultar MIS Turnos')
            print('3. Actualizar MI Turno')
            print('4. Eliminar MI Turno')
            print('0. Salir')
            opciones_validas = {0,1,2,3,4}

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

        # --- Rutas por rol ---
        if user.get("es_admin"):
            if opt == 0:
                print('Hasta luego, gracias por confiar en InstaTurno.')
                break
            elif opt == 1:
                crear_usuario()
            elif opt == 2:
                print("Listado de usuarios: (TODO)")
            elif opt == 3:
                print("Cambiar permisos: (TODO)")
            elif opt == 4:
                print("Eliminar usuario: (TODO)")
            input("\nENTER para volver al menú...")

        elif user.get("es_empleado"):
            if opt == 0:
                print('Hasta luego, gracias por confiar en InstaTurno.')
                break
            elif opt == 1:
                crear_turno(user)  # empleado crea turnos
            elif opt == 2:
                consultar_turno_mod.consultar_turno(user)
            elif opt == 3:
                actualizar_turno(user)  # asegurar que valide permisos en la función
            elif opt == 4:
                eliminar_turno(user)    # asegurar que valide permisos en la función
            input("\nENTER para volver al menú...")

        elif user.get("es_medico"):
            if opt == 0:
                print('Hasta luego, gracias por confiar en InstaTurno.')
                break
            elif opt == 1:
                consultar_turnos_medico(user["id_usuario"])
            input("\nENTER para volver al menú...")

        else:
            # Paciente
            if opt == 0:
                print('Hasta luego, gracias por confiar en InstaTurno.')
                break
            elif opt == 1:
                crear_turno(user)  # paciente crea SU turno
            elif opt == 2:
                consultar_turno_mod.consultar_turno(user)  # debe filtrar por su DNI/usuario
            elif opt == 3:
                actualizar_turno(user)  # debe permitir solo turnos propios
            elif opt == 4:
                eliminar_turno(user)    # debe permitir solo turnos propios
            input("\nENTER para volver al menú...")

# Main
if __name__ == "__main__":
    menu_inicio()

