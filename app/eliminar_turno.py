from conectar_base_datos import conectar_base_datos

def eliminar_turno(user):
    conn = conectar_base_datos()
    cursor = conn.cursor(buffered=True)  # evita "commands out of sync"

    es_empleado = user.get("es_empleado", False)  # si no es empleado, lo tratamos como paciente

    print('0. Salir.')

    # pedir ID de turno con validación simple
    while True:
        try:
            c = int(input('Ingrese su código de turno: ').strip())
            if c == 0:
                print(" - Cerrando Módulo -")
                cursor.close()
                conn.close()
                return
            break
        except ValueError:
            print("Código no válido. Por favor, ingrese un número.")

    if es_empleado:
        # EMPLEADO: borra cualquier turno por ID
        cursor.execute('DELETE FROM Turno WHERE id_turno = %s;', (c,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f'El turno {c} ha sido ELIMINADO.')
        else:
            print('Turno NO encontrado.')

        cursor.close()
        conn.close()
        return

    # PACIENTE: borra solo SUS turnos
    # 1) obtener DNI del usuario (si viene en user, sino desde la tabla Usuario; y si no, pedirlo)
    def _get_user_dni():
        dni = user.get("dni")
        if dni is not None and str(dni).strip() != "":
            return str(dni).strip()
        cursor.execute("SELECT dni FROM Usuario WHERE id_usuario = %s;", (user["id_usuario"],))
        r = cursor.fetchone()
        return (str(r[0]).strip() if r and r[0] is not None else None)

    dni = _get_user_dni()
    if not dni:
        dni = input("Ingrese su DNI: ").strip()

    # 2) buscar su id_paciente
    cursor.execute("SELECT id_paciente FROM Paciente WHERE DNI = %s;", (dni,))
    pr = cursor.fetchone()
    if not pr:
        print("No se encontró paciente con ese DNI.")
        cursor.close()
        conn.close()
        return
    id_paciente = pr[0]

    # 3) borrar solo si el turno le pertenece
    cursor.execute(
        "DELETE FROM Turno WHERE id_turno = %s AND Paciente_id_paciente = %s;",
        (c, id_paciente)
    )
    conn.commit()

    if cursor.rowcount > 0:
        print(f'Su turno {c} ha sido ELIMINADO.')
    else:
        print('Turno NO encontrado o no pertenece a su DNI.')

    cursor.close()
    conn.close()
