from conectar_base_datos import conectar_base_datos

def actualizar_turno(user):
    conn = conectar_base_datos()
    cursor = conn.cursor(buffered=True)  # ayuda a evitar "commands out of sync"

    # --- Validación de rol ---
    es_admin    = user.get("es_admin", False)
    es_empleado = user.get("es_empleado", False)
    es_medico   = user.get("es_medico", False)
    es_paciente = not (es_admin or es_empleado or es_medico)

    if es_admin or es_medico:
        print("⛔ No tiene permisos para actualizar turnos.")
        conn.close()
        return

    # --- Ingreso del ID de turno ---
    while True:
        try:
            print('Ingrese su código de turno o digite 0 (cero) para Salir: ')
            c = int(input().strip())
            if c == 0:
                print('Adiós')
                conn.close()
                return
            break
        except ValueError:
            print("Código no válido. Por favor, ingrese un número.")

    # --- Traer datos del turno seleccionado ---
    cursor.execute("""
        SELECT t.id_turno,
               CONCAT(p.Nombre, ' ', p.Apellido) AS Nombre_Paciente,
               p.DNI,
               e.Nombre AS Nombre_Especialidad,
               t.Paciente_id_paciente
        FROM Turno t
        INNER JOIN Paciente p     ON t.Paciente_id_paciente = p.id_paciente
        INNER JOIN Especialidad e ON t.Especialidad_id_especialidad = e.id_especialidad
        WHERE t.id_turno = %s;
    """, (c,))
    turno = cursor.fetchone()

    if not turno:
        print('No se encontraron turnos para el código:', c)
        conn.close()
        return

    id_turno, nombre_paciente, dni_turno, especialidad_turno, id_paciente_turno = turno
    print(f"El turno seleccionado corresponde al paciente {nombre_paciente} (DNI {dni_turno}), para la especialiad de {especialidad_turno}")

    # --- Si es PACIENTE, confirmar que el turno es suyo ---
    if es_paciente:
        dni_confirm = input("Para continuar, ingrese su DNI: ").strip()
        if dni_confirm != str(dni_turno):
            print("⛔ No puede actualizar un turno que no es suyo.")
            conn.close()
            return

    # --- Menú según rol ---
    if es_empleado:
        print("¿Qué desea modificar?")
        print('1. Paciente')
        print('2. Especialidad')
        print('0. Salir')
        opciones_validas = {0,1,2}
    else:
        # Paciente: solo puede cambiar Especialidad
        print("¿Qué desea modificar?")
        print('2. Especialidad')
        print('0. Salir')
        opciones_validas = {0,2}

    # leer opción
    while True:
        try:
            opcion = int(input().strip())
            if opcion in opciones_validas:
                break
            else:
                print("Opción inválida.")
        except ValueError:
            print("Por favor, ingrese un número.")

    # --- Opción 1: cambiar Paciente (solo EMPELADO) ---
    if opcion == 1 and es_empleado:
        nuevo_dni = input('Ingrese el nuevo DNI: ').strip()

        cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s;', (nuevo_dni,))
        h = cursor.fetchone()

        if h:
            cursor.execute('UPDATE Turno SET Paciente_id_paciente = %s WHERE id_turno = %s;', (h[0], c))
            conn.commit()
            print('✅ Se ha actualizado el turno (paciente).')
        else:
            print('Paciente no encontrado en el Sistema.')
            nuevo_nombre = input('Ingrese el nuevo nombre: ').strip()
            nuevo_apellido = input('Ingrese el nuevo apellido: ').strip()

            cursor.execute(
                'INSERT INTO Paciente (Nombre, Apellido, DNI) VALUES (%s, %s, %s);',
                (nuevo_nombre, nuevo_apellido, nuevo_dni)
            )
            conn.commit()

            cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s', (nuevo_dni,))
            i = cursor.fetchone()

            cursor.execute('UPDATE Turno SET Paciente_id_paciente = %s WHERE id_turno = %s;', (i[0], c))
            conn.commit()
            print('✅ Se ha actualizado el turno (paciente creado y asignado).')

    # --- Opción 2: cambiar Especialidad (EMPLEADO o PACIENTE) ---
    elif opcion == 2:
        # Listar especialidades ordenadas por Nombre (puede ser por ID si preferís)
        cursor.execute('SELECT id_especialidad, Nombre FROM Especialidad ORDER BY Nombre ASC;')
        especialidades = cursor.fetchall()

        if not especialidades:
            print("No hay especialidades disponibles.")
            conn.close()
            return

        print("Seleccione una nueva Especialidad:")
        for idx, esp in enumerate(especialidades, start=1):
            print(f'{idx}. {esp[1]}')

        while True:
            try:
                f = int(input().strip())
                if 1 <= f <= len(especialidades):
                    nueva_area_nombre = especialidades[f-1][1]
                    break
                else:
                    print("Por favor, ingrese un número válido.")
            except ValueError:
                print("Por favor, ingrese un número.")

        cursor.execute("SELECT id_especialidad FROM Especialidad WHERE Nombre = %s;", (nueva_area_nombre,))
        especialidad = cursor.fetchone()

        if especialidad:
            cursor.execute(
                'UPDATE Turno SET Especialidad_id_especialidad = %s WHERE id_turno = %s;',
                (especialidad[0], c)
            )
            conn.commit()
            print(f'✅ La especialidad ha sido actualizada a {nueva_area_nombre}')
        else:
            print(f'No se encontró la especialidad {nueva_area_nombre}')

    elif opcion == 0:
        print("Adiós.")

    conn.close()

