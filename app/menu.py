from crear_turno import crear_turno
from consultar_turno import consultar_turno
from eliminar_turno import eliminar_turno
from actualizar_turno import actualizar_turno
from consultar_turnos_medico import consultar_turnos_medico

from auth import login

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
            # print('5. Opciones avanzadas')  # si existe
            print('0. Salir')
            opciones_validas = {0,1,2,3,4}
        elif user["es_medico"]:
            print('1. Consultar mis turnos (por especialidad)')
            print('0. Salir')
            opciones_validas = {0,1}
        else:  # paciente
            print('1. Consultar mis turnos (por DNI)')
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
                crear_turno()         # ya lo tenés:contentReference[oaicite:7]{index=7}
            elif opt == 2:
                consultar_turno()     # ya lo tenés:contentReference[oaicite:8]{index=8}
            elif opt == 3:
                actualizar_turno()    # ya lo tenés:contentReference[oaicite:9]{index=9}
            elif opt == 4:
                eliminar_turno()      # ya lo tenés:contentReference[oaicite:10]{index=10}
            # elif opt == 5:
            #     opciones_avanzadas()
        elif user["es_medico"]:
            if opt == 0:
                print('Hasta luego, gracias por confiar en InstaTurno.')
                break
            elif opt == 1:
                consultar_turnos_medico(user["id_usuario"])
        else:  # paciente
            if opt == 0:
                print('Hasta luego, gracias por confiar en InstaTurno.')
                break
            elif opt == 1:
                # Reutilizamos tu flujo "Consultar turnos por paciente" (te pedirá DNI):contentReference[oaicite:11]{index=11}
                consultar_turno()

# Main
if __name__ == "__main__":
    menu_inicio()
