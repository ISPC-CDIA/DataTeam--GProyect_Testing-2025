from conectar_base_datos import conectar_base_datos
from tabulate import tabulate

def _elegir_por_id(rows, etiqueta, headers):
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

def _get_user_dni(conn, user):
    """Devuelve el DNI del usuario logueado. Primero del dict 'user', si no, lo lee de la BD."""
    dni = user.get("dni")
    if dni is not None and str(dni).strip() != "":
        return str(dni).strip()
    cur = conn.cursor(buffered=True)
    cur.execute("SELECT dni FROM Usuario WHERE id_usuario = %s;", (user["id_usuario"],))
    row = cur.fetchone()
    return (str(row[0]).strip() if row and row[0] is not None else None)

def crear_turno(user):
    # Reglas de rol
    es_admin    = user.get("es_admin", False)
    es_empleado = user.get("es_empleado", False)
    es_medico   = user.get("es_medico", False)
    es_paciente = not (es_admin or es_empleado or es_medico)

    if es_admin:
        print("⛔ El admin gestiona usuarios; no crea turnos.")
        return
    if es_medico:
        print("⛔ El médico no crea turnos.")
        return

    conn = conectar_base_datos()
    cursor = conn.cursor(buffered=True)

    # 1) DEPARTAMENTO
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
        departamentos, etiqueta="Departamento", headers=["ID", "Departamento"]
    )
    if id_departamento is None:
        conn.close()
        return

    # 2) ESPECIALIDAD (FK directa a Departamento)
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
        especialidades, etiqueta="Especialidad", headers=["ID", "Especialidad"]
    )
    if id_especialidad is None:
        conn.close()
        return

    # 3) PACIENTE (según rol)
    if es_empleado:
        # Empleado crea para cualquier DNI
        print()
        user_dni = input('Ingrese DNI del paciente: ').strip()

        # buscar paciente por DNI
        cursor.execute('SELECT id_paciente, Nombre, Apellido FROM Paciente WHERE DNI = %s;', (user_dni,))
        row = cursor.fetchone()
        if row:
            id_paciente = row[0]
        else:
            # crear paciente si no existe
            nombre = input('Nombre del paciente: ').strip()
            apellido = input('Apellido del paciente: ').strip()
            cursor.execute(
                'INSERT INTO Paciente (Nombre, Apellido, DNI) VALUES (%s, %s, %s);',
                (nombre, apellido, user_dni)
            )
            conn.commit()
            cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s;', (user_dni,))
            id_paciente = cursor.fetchone()[0]

    else:
        # Paciente crea su propio turno: NO pedimos nombre/apellido/DNI
        user_dni = _get_user_dni(conn, user)
        if not user_dni:
            # Fallback mínimo si el login no trae DNI ni está en Usuario
            user_dni = input("Ingrese su DNI: ").strip()

        # buscar paciente por DNI; si no está, pedimos nombre/apellido UNA sola vez
        cursor.execute('SELECT id_paciente, Nombre, Apellido FROM Paciente WHERE DNI = %s;', (user_dni,))
        row = cursor.fetchone()
        if row:
            id_paciente = row[0]
        else:
            print("No encontramos tu ficha de paciente. Vamos a crearla.")
            nombre = input('Tu Nombre: ').strip()
            apellido = input('Tu Apellido: ').strip()
            cursor.execute(
                'INSERT INTO Paciente (Nombre, Apellido, DNI) VALUES (%s, %s, %s);',
                (nombre, apellido, user_dni)
            )
            conn.commit()
            cursor.execute('SELECT id_paciente FROM Paciente WHERE DNI = %s;', (user_dni,))
            id_paciente = cursor.fetchone()[0]

    # 4) Crear turno (fecha/hora actuales por simplicidad del TP)
    cursor.execute("""
        INSERT INTO Turno (fecha, hora, Paciente_id_paciente, Especialidad_id_especialidad)
        VALUES (CURDATE(), CURTIME(), %s, %s);
    """, (id_paciente, id_especialidad))
    id_turno = cursor.lastrowid

    conn.commit()
    conn.close()

    # Confirmación
    print(f"\n✅ Turno creado correctamente.")
    print(f"Departamento: {nombre_departamento}")
    print(f"Especialidad: {nombre_especialidad}")
    print(f"DNI paciente: {user_dni}")
    if id_turno:
        print(f"Código de turno: {id_turno}")











