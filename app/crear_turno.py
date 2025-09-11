from conectar_base_datos import conectar_base_datos
from tabulate import tabulate

def crear_turno():
    conn = conectar_base_datos()
    cursor = conn.cursor()

    # 1) Elegir DEPARTAMENTO
    print('Para CREAR un turno, seleccione un DEPARTAMENTO médico:\n')

    cursor.execute("""
        SELECT d.id_departamento, d.nombre
        FROM Departamento d
        ORDER BY d.nombre ASC;
    """)
    departamentos = cursor.fetchall()

    if not departamentos:
        print("No hay departamentos disponibles.")
        conn.close()
        return

    tabla_deptos = [[i+1, d[0], d[1]] for i, d in enumerate(departamentos)]
    print(tabulate(tabla_deptos, headers=["N°", "ID", "Departamento"], tablefmt="grid"))

    # Selección segura por N°
    id_departamento = None
    nombre_departamento = None
    while True:
        try:
            opcion = int(input("Ingrese el N° de departamento: ").strip())
            if 1 <= opcion <= len(departamentos):
                id_departamento = departamentos[opcion-1][0]
                nombre_departamento = departamentos[opcion-1][1]
                break
            else:
                print("Por favor, ingrese un número válido.")
        except ValueError:
            print("Por favor, ingrese un número.")

    # 2) Listar ESPECIALIDADES del departamento elegido (sin duplicados)
    print(f"\nDepartamento elegido: {nombre_departamento}")
    print("Ahora seleccione una ESPECIALIDAD disponible en este departamento:\n")

    # Si NO tenés FK directa en Especialidad a Departamento, usamos DISTINCT + JOIN vía Médicos
    cursor.execute("""
        SELECT DISTINCT e.id_especialidad, e.nombre
        FROM Especialidad e
        JOIN Medico_Especialidad me ON me.id_especialidad = e.id_especialidad
        JOIN Medico m ON m.id_medico = me.id_medico
        WHERE m.Departamento_id_departamento = %s
        ORDER BY e.nombre ASC;
    """, (id_departamento,))
    especialidades = cursor.fetchall()

    if not especialidades:
        print("No hay especialidades para ese departamento.")
        conn.close()
        return

    tabla_esps = [[i+1, e[0], e[1]] for i, e in enumerate(especialidades)]
    print(tabulate(tabla_esps, headers=["N°", "ID", "Especialidad"], tablefmt="grid"))

    id_especialidad = None
    nombre_especialidad = None
    while True:
        try:
            opcion = int(input("Ingrese el N° de especialidad: ").strip())
            if 1 <= opcion <= len(especialidades):
                id_especialidad = especialidades[opcion-1][0]
                nombre_especialidad = especialidades[opcion-1][1]
                break
            else:
                print("Por favor, ingrese un número válido.")
        except ValueError:
            print("Por favor, ingrese un número.")

    # 3) Datos del paciente
    print()
    user_m = input('Ingrese su Nombre: ').strip()
    user_a = input('Ingrese su Apellido: ').strip()
    user_dni = input('Ingrese su DNI: ').strip()

    # 4) Upsert paciente (si no existe, lo crea)
    cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s;', (user_dni,))
    row = cursor.fetchone()

    if row is None:
        cursor.execute(
            'INSERT INTO Paciente (Nombre, Apellido, DNI) VALUES (%s, %s, %s);',
            (user_m, user_a, user_dni)
        )
        # Reobtener id_paciente
        cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s;', (user_dni,))
        tdni = cursor.fetchone()[0]
    else:
        tdni = row[0]

    # 5) Crear turno (usa el ID REAL de especialidad, no el índice)
    cursor.execute("""
        INSERT INTO Turno (fecha, hora, Paciente_id_paciente, Especialidad_id_especialidad)
        VALUES (CURDATE(), CURTIME(), %s, %s);
    """, (tdni, id_especialidad))

    # 6) Confirmación
    cursor.execute('SELECT MAX(id_turno) FROM Turno;')
    c = cursor.fetchone()
    id_turno = c[0] if c else None

    conn.commit()
    conn.close()

    print(f"\n✅ Turno creado correctamente.")
    print(f"Departamento: {nombre_departamento}")
    print(f"Especialidad: {nombre_especialidad}")
    if id_turno is not None:
        print(f"Código de turno: {id_turno}")
    print('Recibirá un Email con la confirmación del horario (a implementar).')
