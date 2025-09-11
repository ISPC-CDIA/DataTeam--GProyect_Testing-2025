# app/consultar_turno.py
from conectar_base_datos import conectar_base_datos
from tabulate import tabulate

HEADERS = ["ID Turno", "DNI", "Nombre", "Apellido", "Especialidad", "Fecha", "Hora"]

def _render_turnos(rows):
    if rows:
        print(tabulate(rows, headers=HEADERS, tablefmt="grid"))
    else:
        print("⚠️ No se encontraron turnos con ese criterio.")

def _q_base(cursor, where_clause="", params=()):
    sql = f"""
        SELECT 
            t.id_turno,
            p.DNI,
            p.Nombre,
            p.Apellido,
            e.nombre AS Especialidad,
            DATE_FORMAT(t.fecha, '%%Y-%%m-%%d') AS fecha,
            DATE_FORMAT(t.hora, '%%H:%%i')        AS hora
        FROM Turno t
        JOIN Paciente   p ON p.id_paciente = t.Paciente_id_paciente
        JOIN Especialidad e ON e.id_especialidad = t.Especialidad_id_especialidad
        {where_clause}
        ORDER BY t.fecha DESC, t.hora DESC, t.id_turno DESC
    """
    cursor.execute(sql, params)
    return cursor.fetchall()

def _listar_todos(cursor):
    rows = _q_base(cursor)

