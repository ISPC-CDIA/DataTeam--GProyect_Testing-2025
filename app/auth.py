# auth.py (simple, sin bcrypt)
from mysql import connector

def get_conn():
    return connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="Turnero"
    )

def login(username: str, plain_password: str):
    """
    Devuelve dict con info del usuario si la contraseña (texto plano) coincide.
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT u.id_usuario, u.username, u.email, u.password_hash, u.dni,
               r.nombre AS rol
        FROM Usuario u
        JOIN Rol r ON r.id_rol = u.id_rol
        WHERE u.username=%s
    """, (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None
    # Comparación directa en texto plano
    if plain_password != row["password_hash"]:
        return None

    rol = (row["rol"] or "").lower()
    return {
        "id_usuario": row["id_usuario"],
        "username": row["username"],
        "rol": rol,
        "dni": row["dni"],
        "es_admin": rol == "admin",
        "es_empleado": rol == "empleado",
        "es_medico": rol == "medico",
        "es_paciente": rol == "paciente",
    }

def set_password_plain(username: str, new_password: str) -> bool:
    """
    (Opcional) Cambia la contraseña en texto plano desde el código.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE Usuario SET password_hash=%s WHERE username=%s",
                (new_password, username))
    conn.commit()
    ok = cur.rowcount > 0
    cur.close(); conn.close()
    return ok
