from conectar_base_datos import conectar_base_datos

def actualizar_turno():
    conn = conectar_base_datos()
    cursor = conn.cursor()

    while True:
        try:
            # Siempre contemplemos la opción del usuario de no querer avanzar.
            print('Ingrese su código de turno o digite 0 (cero) para Salir: ')
            #Almacenamos el código de turno (Id_turno)
            c = int(input())
            if c == 0:
                print('Adios')
                return
            break
        except ValueError:
            # Alerta
            print("Código no válido. Por favor, ingrese un número.")

    # Conlsuta a la DB -> Existe este id?
    #de ser así, devuelveme el nombre completo y la especialidad.
    cursor.execute("""SELECT t.id_turno,
                             CONCAT(p.Nombre, ' ', p.Apellido) AS Nombre_Paciente,
                             e.Nombre AS Nombre_Especialidad
                       FROM Turno t
                       INNER JOIN Paciente p ON t.Paciente_id_paciente = p.id_paciente
                       INNER JOIN Especialidad e ON t.Especialidad_id_especialidad = e.id_especialidad
                       WHERE t.id_turno = %s;""", (c,))
    turno = cursor.fetchone()

    if turno:
        print(f"El turno seleccionado corresponde al paciente {turno[1]}, para el área de {turno[2]}")
        print("¿Qué desea modificar?")
        print('1. Paciente.')
        print('2. Área.')
        print('0. Salir.')

        # Acá comienza a complicarse
        while True:
            try:
                opcion = int(input())
                if opcion in [1, 2, 0]:
                    break
                else:
                    print("Por favor, ingrese 1 o 2.")
            except ValueError:
                print("Por favor, ingrese un número.")
        # Qué pasa si queremos modificar el nombre del paciente, pero el paciente no está en el sistema?
        if opcion == 1:
            nuevo_dni = input('Ingrese el nuevo DNI:')
            # DB, este DNI existe?
            cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s;', (nuevo_dni,))
            h = cursor.fetchone()

            # Si, el DNI existe -> Entonces modifica la tabla turno con este nuevo id_paciente en la id_turno agregada anteriormente.
            if h:
                cursor.execute('UPDATE Turno SET Paciente_id_paciente = %s WHERE id_turno = %s;', (h[0], c))
                conn.commit()
                print('Se ha actualizado el turno')
            # No, el DNI no existe -> Entonces, crea un nuevo paciente!
            else:
                print('Paciente no encontrado en el Sistema.')

                # Datos necesarios para completar la tabla 'Paciente' (El DNI ya lo tenemos de antes ;D)
                nuevo_nombre = input('Ingrese el nuevo nombre: ')
                nuevo_apellido = input('Ingrese el nuevo apellido: ')

                # INSERT a la DB
                cursor.execute('INSERT INTO Paciente (Nombre, Apellido, DNI) VALUES (%s, %s, %s);', (nuevo_nombre, nuevo_apellido, nuevo_dni))
                conn.commit()
                # Solicitamos el nuevo id_paciente para actualizar la tabla 'Turno'
                cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s', (nuevo_dni,))
                i = cursor.fetchone()
                cursor.execute('UPDATE Turno SET Paciente_id_paciente = %s WHERE id_turno = %s;', (i[0], c))
                conn.commit()
                #FIN
                print('Se ha actualizado el turno')

        # Si decide modificar la Especialidad, es un poco mas sencillo.    
        elif opcion == 2:
            cursor.execute('SELECT id_especialidad, Nombre FROM Especialidad ORDER BY Nombre ASC;')
            especialidades = cursor.fetchall()
            print("Seleccione una nueva Área:")

            # No implementamos 'TABULATE' porque asumimos que -> al ser una modificación del turno creado ya se conoce el código
            #y priorizamos la rapidez en este caso.
            for idx, esp in enumerate(especialidades, start=1):
                print(f'{idx}. {esp[1]}')

            while True:
                try:
                    f = int(input())
                    if 1 <= f <= len(especialidades):
                        nueva_area = especialidades[f-1][1]
                        break
                    else:
                        print("Por favor, ingrese un número válido.")
                except ValueError:
                    print("Por favor, ingrese un número.")

            cursor.execute("SELECT id_especialidad FROM Especialidad WHERE Nombre = %s;", (nueva_area,))
            especialidad = cursor.fetchone()

            # Si bien, anteriormente compromabos la opción del usuario comparandola con la cantidad de especialidades
            #no está de mas hacer está comprobación. -> nunca se sabe cuando puede haberr un hueco en la DB
            if especialidad:
                cursor.execute('UPDATE Turno SET Especialidad_id_especialidad = %s WHERE id_turno = %s;', (especialidad[0], c))
                conn.commit()
                print(f'El área ha sido actualizada a {nueva_area}')
            else:
                print(f'No se encontró el área {nueva_area}')

        # Salir.
        elif opcion == 0:
            print("Adios.")

    # Si la primer consulta a la DB (para buscar el id del turno) no encuentra nada, nos alerta.
    else:
       print('No se encontraron turnos para el código:', c)

    conn.close()
