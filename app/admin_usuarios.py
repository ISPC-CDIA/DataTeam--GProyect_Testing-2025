# admin_usuarios.py
from conectar_base_datos import conectar_base_datos
from tabulate import tabulate
import mysql.connector  # para detectar errores específicos (FK 1451)

# Si estos nombres existen en tu tabla Rol.nombre, listo:
ROLES_VALIDOS = {"admin", "empleado", "medico", "paciente"}

def ver_usuarios():
    conn = conectar_base_datos()
    c = conn.cursor(buffered=True)
    try:
        c.execute("""
            SELECT u.id_usuario,
                   u.username,
                   COALESCE(r.nombre, '(sin rol)') AS rol
            FROM Usuario u
            LEFT JOIN Rol r ON r.id_rol = u.id_rol
            ORDER BY u.id_usuario ASC;
        """)
        rows = c.fetchall()
        if not rows:
            print("No hay usuarios.")
        else:
            print(tabulate(rows, headers=["ID", "Usuario", "Rol"], tablefmt="grid"))
    except Exception as e:
        print(f"Error al listar usuarios: {e}")
    finally:
        conn.close()

def cambiar_rol_usuario():
    conn = conectar_base_datos()
    c = conn.cursor(buffered=True)
    try:
        id_u = input("ID de usuario a modificar: ").strip()
        if not id_u.isdigit():
            print("ID inválido.")
            return

        nuevo = input("Nuevo rol [admin/empleado/medico/paciente]: ").strip().lower()
        if nuevo not in ROLES_VALIDOS:
            print("Rol inválido.")
            return

        # Buscar el id_rol por nombre
        c.execute("SELECT id_rol FROM Rol WHERE nombre = %s;", (nuevo,))
        row = c.fetchone()
        if not row:
            print("Ese rol no existe en la tabla Rol.")
            return
        id_rol = row[0]

        # Actualizar el usuario
        c.execute("UPDATE Usuario SET id_rol = %s WHERE id_usuario = %s;", (id_rol, id_u))
        if c.rowcount == 0:
            print("No existe el usuario indicado.")
        else:
            conn.commit()
            print("✅ Rol actualizado.")
    except Exception as e:
        print(f"Error al cambiar rol: {e}")
    finally:
        conn.close()

def eliminar_usuario():
    conn = conectar_base_datos()
    c = conn.cursor(buffered=True)
    try:
        id_u = input("ID de usuario a eliminar (0 para cancelar): ").strip()
        if id_u == "0":
            print("Operación cancelada.")
            return
        if not id_u.isdigit():
            print("ID inválido.")
            return

        # Mostrar info antes de borrar
        c.execute("""
            SELECT u.id_usuario,
                   u.username,
                   COALESCE(r.nombre, '(sin rol)') AS rol
            FROM Usuario u
            LEFT JOIN Rol r ON r.id_rol = u.id_rol
            WHERE u.id_usuario = %s
        """, (id_u,))
        row = c.fetchone()
        if not row:
            print("No existe el usuario indicado.")
            return

        print(tabulate([row], headers=["ID", "Usuario", "Rol"], tablefmt="grid"))

        # (opcional) bloquear eliminación de admins
        if str(row[2]).lower() == "admin":
            print("⛔ No se puede eliminar un usuario con rol admin.")
            return

        if input("¿Confirmar eliminación? (s/n): ").strip().lower() != "s":
            print("Operación cancelada.")
            return

        c.execute("DELETE FROM Usuario WHERE id_usuario = %s;", (id_u,))
        conn.commit()

        if c.rowcount == 0:
            print("No se eliminó ningún usuario.")
        else:
            print("✅ Usuario eliminado.")

    except mysql.connector.Error as e:
        # 1451: Cannot delete or update a parent row: a foreign key constraint fails
        if getattr(e, "errno", None) == 1451:
            print("⛔ No se puede eliminar: el usuario tiene datos relacionados (p. ej., Paciente/Turnos).")
            print("Primero elimine/desvincule esos registros o configure la FK con ON DELETE.")
        else:
            print(f"Error al eliminar usuario: {e.errno} {e.msg}")
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
    finally:
        conn.close()

