from conectar_base_datos import conectar_base_datos

def eliminar_turno():
    conn = conectar_base_datos()
    cursor = conn.cursor()

    # Opción -> Salida
    print('0. Salir.')

    while True:
        try:
            c = int(input('Ingrese su código de turno: '))
            if c == 0:
                print(" - Cerrando Módulo -")
                return
            break
        except ValueError:
            print("Código no válido. Por favor, ingrese un número.")

    # el ID del turno se utiliza para muchos támites -> en este caso, para borrar
    cursor.execute('DELETE FROM Turno WHERE id_turno = %s;', (c,))
    conn.commit()

    if cursor.rowcount > 0:
        print(f'Su turno {c} ha sido ELIMINADO.')
    else:
        print('Turno NO encontrado.')

    cursor.close()
    conn.close()
