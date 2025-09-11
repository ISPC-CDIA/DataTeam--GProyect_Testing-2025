from conectar_base_datos import conectar_base_datos
from tabulate import tabulate

def _elegir_por_id(rows, etiqueta, headers):
    """
    Muestra una tabla [ID, Nombre] y pide SOLO el ID exacto.
    0 o 'q' -> cancelar/volver.
    Devuelve (id_elegido, nombre_elegido) o (None, None) si se cancela.
    """
    if not rows:
        print(f"No hay {etiqueta}s disponibles.")
        return None, None

    print(tabulate(rows, headers=headers, tablefmt="grid"))

    ids_validos = {r[0] for r in rows}
    nombres_por_id = {r[0]: r[1] for r in rows}

    while True:
        val = input(f"Ingrese el ID de {etiqueta} (0 para volver): ").strip().lower()
        if val in ("0", "q"):
            return None, None
        if val.isdigit():
            _id = int(val)
            if _id in ids_validos:
                return _id, nombres_por_id[_id]
        print("ID inválido. Ingrese un ID que exista en la tabla (o 0 para volver).")

def crear_turno():
    conn = conectar_base_datos()
    cursor = conn.cursor(buffered=True)  # evita "commands out of sync"

    # 1) Elegir DEPARTAMENTO
    print('Para CREAR un turno, seleccione un DEPARTAMENTO médico:\n')

    cursor.execute("""
        SELECT id_departamento, Nombre
        FROM Departamento
        ORDER BY id_departamento ASC;
    """)
    departamentos = cursor.fetchall()
    if not departamentos:
        print("No hay departamentos disponibles.")
        conn.close()
        return

    id_departamento, nombre_departamento = _elegir_por_id(
        departamentos,
        etiqueta="Departamento",
        headers=["ID", "Departamento"]
    )
    if id_departamento is None:
        conn.close()
        return

    # 2) Elegir ESPECIALIDAD (FK directa en Especialidad)
    print(f"\nDepartamento elegido: {nombre_departamento}")
    print("Ahora seleccione una ESPECIALIDAD disponible en este departamento:\n")

    cursor.execute("""
        SELECT id_especialidad, Nombre
        FROM Especialidad
        WHERE Departamento_id_departamento = %s
        ORDER BY id_especialidad ASC;
    """, (id_departamento,))
    especialidades = cursor.fetchall()
    if not especialidades:
        print("No hay especialidades para ese departamento.")
        conn.close()
        return

    id_especialidad, nombre_especialidad = _elegir_por_id(
        especialidades,
        etiqueta="Especialidad",
        headers=["ID", "Especialidad"]
    )
    if id_especialidad is None:
        conn.close()
        return

    # 3) Datos del paciente
    print()
    user_m = input('Ingrese Nombre del paciente: ').strip()
    user_a = input('Ingrese Apellido del paciente: ').strip()
    user_dni = input('Ingrese DNI del paciente: ').strip()

    cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s;', (user_dni,))
    row = cursor.fetchone()

    if row is None:
        cursor.execute(
            'INSERT INTO Paciente (Nombre, Apellido, DNI) VALUES (%s, %s, %s);',
            (user_m, user_a, user_dni)
        )
        cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s;', (user_dni,))
        tdni = cursor.fetchone()[0]
    else:
        tdni = row[0]

    # 4) Crear turno
    cursor.execute("""
        INSERT INTO Turno (fecha, hora, Paciente_id_paciente, Especialidad_id_especialidad)
        VALUES (CURDATE(), CURTIME(), %s, %s);
    """, (tdni, id_especialidad))
    id_turno = cursor.lastrowid

    conn.commit()
    conn.close()

    # 5) Confirmación
    print(f"\n✅ Turno creado correctamente.")
    print(f"Departamento: {nombre_departamento}")
    print(f"Especialidad: {nombre_especialidad}")
    if id_turno:
        print(f"Código de turno: {id_turno}")
    print('Recibirá un Email con la confirmación del horario (a implementar).')









