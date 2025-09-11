# crear_usuario.py
from core.conectar_base_datos import conectar_base_datos
from tabulate import tabulate

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
    print("\n- Crear Usuario (solo admin) -")
    username = input("Username: ").strip()
    email = input("Email (opcional): ").strip() or None
    dni_in = input("DNI (opcional, solo si es paciente): ").strip()
    dni = int(dni_in) if dni_in.isdigit() else None

    # contraseña (texto plano para la práctica)
    while True:
        pwd = input("Contraseña: ").strip()
        pwd2 = input("Repetir contraseña: ").strip()
        if pwd and pwd == pwd2:
            break
        print("Las contraseñas no coinciden o están vacías.")

    conn = conectar_base_datos()
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

    # insertar usuario (contraseña en texto plano)
    cur.execute("""
        INSERT INTO Usuario (username, email, password_hash, dni, id_rol)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, email, pwd, dni, rol_id))
    conn.commit()

    # Vincular con Paciente si corresponde
    if dni is not None:
        cur.execute("SELECT id_usuario FROM Usuario WHERE username=%s", (username,))
        uid = cur.fetchone()[0]
        cur.execute("UPDATE Paciente SET usuario_id=%s WHERE DNI=%s AND (usuario_id IS NULL OR usuario_id=0) LIMIT 1",
                    (uid, dni))
        conn.commit()

    print("✅ Usuario creado correctamente.")
    cur.close()
    conn.close()

