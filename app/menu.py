from crear_turno import crear_turno
from consultar_turno import consultar_turno
from eliminar_turno import eliminar_turno
from actualizar_turno import actualizar_turno
from opciones_avanzadas import opciones_avanzadas

def menu_inicio():

    print('- Bienvenido al Sistema de Gestión de Turnos -')

    while True:
        print('Para continuar seleccionar una opción:')
        print('1. Crear Turno.')
        print('2. Consultar Turno.')
        print('3. Actualizar Turno.')
        print('4. Eliminar Turno.')
        print('5. Opciones avanzadas.')
        print('0. Salir')

        while True:
            try:
                user_opt = int(input())
                if user_opt in [0, 1, 2, 3, 4, 5]:
                    break
                else:
                    print("Por favor, ingrese un número entre 0 y 5.")
            except ValueError:
                print("Por favor, ingrese un número.")


        if user_opt == 1:
            crear_turno()
        elif user_opt == 2:
            consultar_turno()
        elif user_opt == 3:
            actualizar_turno()
        elif user_opt == 4:
            eliminar_turno()
        elif user_opt == 5:
            opciones_avanzadas()

        print('Desea realizar otro trámite?')
        print('1. Si.')
        print('2. No')
        while True:
            try:
                h = int(input())
                if h in [1, 2]:
                    break
                else:
                    print("Por favor, ingrese 1 o 2.")
            except ValueError:
                print("Por favor, ingrese un número.")

        if h != 1:
            print('Hasta luego, gracias por confiar en InstaTurno.')
            break

# Main
if __name__ == "__main__":
    menu_inicio()
