# crear_usuario.py
from mysql import connector
from passlib.hash import bcrypt
from tabulate import tabulate

def get_conn():
    return connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="Turnero"
    )

def _seleccionar_rol(cur):
    cur.execute("SELECT id_rol, nombre FROM Rol ORDER BY nombre ASC;")
    roles = cur.fetchall()
    if not roles:
        print("No hay roles cargados.")
        return None
    print("\nRoles disponibles:")
    print(tabulate(roles, headers=["ID", "Rol"], tablefmt="grid"))
    while True:
        try:
            rid = int(input("Ingrese ID de rol: ").strip())
            if any(r[0] == rid for r in roles):
                return rid
            print("Rol inválido.")
        except ValueError:
            print("Ingrese un número válido.")

def crear_usuario():
    print("\n- Crear Usuario -")
    username = input("Username: ").strip()
    email = input("Email (opcional): ").strip() or None
    dni_in = input("DNI (opcional, solo si es paciente): ").strip()
    dni = int(dni_in) if dni_in.isdigit() else None

    # contraseña
    while True:
        pwd = input("Contraseña: ").strip()
        pwd2 = input("Repetir contraseña: ").strip()
        if pwd and pwd == pwd2:
            break
        print("Las contraseñas no coinciden o están vacías.")

    conn = get_conn()
    cur = conn.cursor()

    # elegir rol
    rol_id = _seleccionar_rol(cur)
    if not rol_id:
        cur.close(); conn.close()
        return

    # validar username/email únicos
    cur.execute("SELECT COUNT(*) FROM Usuario WHERE username=%s OR (email IS NOT NULL AND email=%s)", (username, email))
    if cur.fetchone()[0] > 0:
        print("Ya existe un usuario con ese username o email.")
        cur.close(); conn.close()
        return

    # insertar usuario
    pwd_hash = bcrypt.hash(pwd)
    cur.execute("""
        INSERT INTO Usuario (username, email, password_hash, dni, id_rol)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, email, pwd_hash, dni, rol_id))
    conn.commit()

    # Opcional: vincular con Paciente por DNI
    if dni is not None:
        cur.execute("SELECT id_usuario FROM Usuario WHERE username=%s", (username,))
        uid = cur.fetchone()[0]
        # Vincula el primer paciente con ese DNI (si existe)
        cur.execute("UPDATE Paciente SET usuario_id=%s WHERE DNI=%s AND usuario_id IS NULL LIMIT 1", (uid, dni))
        conn.commit()

    # Opcional: vincular con Médico
    vinc_med = input("¿Vincular con un Médico? (s/n): ").strip().lower()
    if vinc_med == 's':
        try:
            cur.execute("SELECT id_medico, Nombre, Apellido FROM Medico ORDER BY id_medico ASC;")
            medicos = cur.fetchall()
            print(tabulate(medicos, headers=["ID", "Nombre", "Apellido"], tablefmt="grid"))
            mid = int(input("Ingrese ID de médico a vincular: ").strip())
            cur.execute("SELECT id_usuario FROM Usuario WHERE username=%s", (username,))
            uid = cur.fetchone()[0]
            cur.execute("UPDATE Medico SET usuario_id=%s WHERE id_medico=%s AND (usuario_id IS NULL OR usuario_id=0)", (uid, mid))
            conn.commit()
        except Exception as e:
            print("No se pudo vincular con Médico:", e)

    print("✅ Usuario creado correctamente.")
    cur.close()
    conn.close()
