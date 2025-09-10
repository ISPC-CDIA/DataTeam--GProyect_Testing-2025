# auth.py
from mysql import connector
from passlib.hash import bcrypt

def get_conn():
    # Usamos tu misma conexión que en conectar_base_datos.py
    return connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="Turnero"
    )

def set_password(username: str, plain_password: str) -> bool:
    """Setea/actualiza el hash de password para un usuario."""
    pwd_hash = bcrypt.hash(plain_password)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE Usuario SET password_hash=%s WHERE username=%s", (pwd_hash, username))
    conn.commit()
    ok = cur.rowcount > 0
    cur.close()
    conn.close()
    return ok

def login(username: str, plain_password: str):
    """
    Devuelve un dict con info del usuario si login ok:
    {id_usuario, username, rol, dni, es_admin, es_empleado, es_medico, es_paciente}
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
    if not bcrypt.verify(plain_password, row["password_hash"]):
        return None

    rol = row["rol"].lower() if row["rol"] else ""
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
