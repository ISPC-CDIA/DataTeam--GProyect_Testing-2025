from conectar_base_datos import conectar_base_datos
from tabulate import tabulate
import mysql.connector

HEADERS = ["ID Turno", "DNI", "Nombre", "Apellido", "Especialidad", "Fecha", "Hora"]

def _render(rows):
    if rows:
        print(tabulate(rows, headers=HEADERS, tablefmt="grid"))
    else:
        print("⚠️ No se encontraron turnos con ese criterio.")

def _q_base(cursor, where="", params=()):
    sql = f"""
        SELECT 
            t.id_turno,
            p.DNI,
            p.Nombre,
            p.Apellido,
            e.nombre AS Especialidad,
            DATE_FORMAT(t.fecha, '%Y-%m-%d') AS fecha,
            DATE_FORMAT(t.hora,  '%H:%i')     AS hora
        FROM Turno t
        JOIN Paciente     p ON p.id_paciente     = t.Paciente_id_paciente
        JOIN Especialidad e ON e.id_especialidad = t.Especialidad_id_especialidad
        {where}
        ORDER BY t.fecha DESC, t.hora DESC, t.id_turno DESC
    """
    cursor.execute(sql, params)
    return cursor.fetchall()

def _mis_turnos_paciente(cursor, id_usuario):
    """Paciente: filtra por vínculo Paciente.usuario_id"""
    try:
        return _q_base(cursor, "WHERE p.usuario_id = %s", (id_usuario,))
    except mysql.connector.errors.ProgrammingError:
        print("⚠️ Paciente no está vinculado por usuario_id. Agrega Paciente.usuario_id o usa búsqueda por DNI.")
        return []

def _mis_turnos_medico(cursor, id_usuario):
    """Médico: turnos de sus especialidades (sin Medico_id_medico en Turno)."""
    try:
        sql = """
            SELECT 
                t.id_turno, p.DNI, p.Nombre, p.Apellido, e.nombre,
                DATE_FORMAT(t.fecha,'%Y-%m-%d'), DATE_FORMAT(t.hora,'%H:%i')
            FROM Turno t
            JOIN Paciente p                 ON p.id_paciente = t.Paciente_id_paciente
            JOIN Especialidad e             ON e.id_especialidad = t.Especialidad_id_especialidad
            JOIN Medico_has_Especialidad me ON me.Especialidad_id_especialidad = e.id_especialidad
            JOIN Medico m                   ON m.id_medico = me.Medico_id_medico
            WHERE m.usuario_id = %s
            ORDER BY t.fecha DESC, t.hora DESC, t.id_turno DESC
        """
        cursor.execute(sql, (id_usuario,))
        return cursor.fetchall()
    except mysql.connector.errors.ProgrammingError:
        print("⚠️ Vincula Medico.usuario_id para filtrar por médico (o ajusta el WHERE).")
        return []

def consultar_turno(usuario_actual=None):
    """
    - Paciente: ve solo sus turnos (oculta 'listar todos').
    - Médico: ve turnos de sus especialidades.
    - Admin/Recepción (o sin usuario_actual): submenú completo.
    """
    rol = (usuario_actual or {}).get("rol")
    id_usuario = (usuario_actual or {}).get("id_usuario")

    if rol == "paciente" and id_usuario:
        conn = conectar_base_datos(); cur = conn.cursor()
        try:
            rows = _mis_turnos_paciente(cur, id_usuario)
        finally:
            conn.close()
        print("\n=== MIS TURNOS ===")
        _render(rows)
        input("\nPresione ENTER para volver...")
        return

    if rol == "medico" and id_usuario:
        conn = conectar_base_datos(); cur = conn.cursor()
        try:
            rows = _mis_turnos_medico(cur, id_usuario)
        finally:
            conn.close()
        print("\n=== TURNOS DE MIS ESPECIALIDADES ===")
        _render(rows)
        input("\nPresione ENTER para volver...")
        return

    # Admin/recepción (o sin usuario): submenú
    while True:
        print("\n=== CONSULTA DE TURNOS ===")
        print("1) Listar TODOS los turnos")
        print("2) Buscar por DNI")
        print("3) Buscar por FECHA (YYYY-MM-DD)")
        print("0) Volver")

        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "0":
            break

        conn = conectar_base_datos(); cur = conn.cursor()
        try:
            if opcion == "1":
                rows = _q_base(cur)
            elif opcion == "2":
                dni = input("DNI exacto: ").strip()
                rows = _q_base(cur, "WHERE p.DNI = %s", (dni,)) if dni else []
            elif opcion == "3":
                fecha = input("Fecha (YYYY-MM-DD): ").strip()
                rows = _q_base(cur, "WHERE t.fecha = %s", (fecha,)) if fecha else []
            else:
                print("Opción inválida."); continue
        finally:
            conn.close()

        _render(rows)
        input("\nPresione ENTER para continuar...")
