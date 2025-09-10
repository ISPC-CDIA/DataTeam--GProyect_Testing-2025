from conectar_base_datos import conectar_base_datos
from tabulate import tabulate

def crear_turno():
    conn = conectar_base_datos()
    cursor = conn.cursor()

    print('Para CREAR un turno, seleccione un departamento médico:')

    #Recupera de la DB la tabla de especialidades.
    cursor.execute('SELECT id_especialidad, Nombre FROM Especialidad ORDER BY Nombre ASC;')
    especialidades = cursor.fetchall()

    #Si hay especialidades cargadas en la tabla, las devuelve por pantalla
    #para eso usamos TABULATE, nos deja mas presentable la interfaz.
    if especialidades:
        headers = ["ID", "Especialidad"]
        tabla_especialidades = [[especialidad[0], especialidad[1]] for especialidad in especialidades]
        print(tabulate(tabla_especialidades, headers=headers, tablefmt="grid"))
    else:
        print("No hay especialidades disponibles.")

    #Validamos el input del usuario -> si la opción NUMÉRICA coincide con algun valor del 'largo' de elementos de especialidades
    #almacena la opción para proseguir. Caso contrario, devuelve una alerta.
    while True:
        try:
            f = int(input())
            if 1 <= f <= len(especialidades):
                user_turn = especialidades[f-1]
                break
            else:
                print("Por favor, ingrese un número válido.")
        except ValueError:
            print("Por favor, ingrese un número.")


    #Habiendo almacenado la opción de Especialidad -> Almacena los datos del paciente
    user_m = input('Ingrese su Nombre:')
    user_a = input('Ingrese su Apellido: ')
    user_dni = input('Ingrese su DNI: ')

    # Comprobación -> el Paciente existe en el sistema?
    # Solicitamos a la DB que busque el DNI ingresado
    cursor.execute('SELECT DNI FROM Paciente WHERE DNI = %s', (user_dni,))
    t = cursor.fetchone()

    # Si el paciente NO se encuntra en la DB -> Agrega el paciente
    #
    # Siguiente paso (indistinto a la preexistencia del paciente) es recuperar el ID de la tabla para -> cargar un nuevo turno con ese ID
    #en la tabla de turnos
    if not t:
        cursor.execute('INSERT INTO Paciente (Nombre, Apellido, DNI) VALUES (%s, %s, %s);', (user_m, user_a, user_dni))
        cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s;', (user_dni,))
        tdni = cursor.fetchone()[0]
        cursor.execute('INSERT INTO Turno (fecha, hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES (CURDATE(), CURTIME(), %s, %s);', (tdni, f))
    else:
        cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s', (user_dni,))
        tdni = cursor.fetchone()[0]
        cursor.execute('INSERT INTO Turno (fecha, hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES (CURDATE(), CURTIME(), %s, %s);', (tdni, f))


    # Mensaje final -> avisa la especialidad, el código del turno (ID) que se va a utilizar para otros tŕamites en el sistema
    print(f'Usted seleccionó {user_turn}.')
    cursor.execute('SELECT MAX(id_turno) FROM Turno;')
    c = cursor.fetchone()
    print(f'El código de su turno es: {c[0]}.') #Borré la coma, chicos :D
    print('Recibirá un Email con la confirmación del horario.') # ----> OBJETIVO! poder implementar esta funcionalidad 

    conn.commit()
    conn.close()
