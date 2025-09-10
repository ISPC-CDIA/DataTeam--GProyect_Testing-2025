# consultar_turnos_medico.py
from conectar_base_datos import conectar_base_datos
from tabulate import tabulate

def consultar_turnos_medico(id_usuario: int):
    """
    Lista turnos de las especialidades asociadas al médico cuyo usuario_id = id_usuario.
    """
    conn = conectar_base_datos()
    cur = conn.cursor()

    # 1) Buscamos el id_medico por usuario
    cur.execute("""
        SELECT m.id_medico, m.Nombre, m.Apellido
        FROM Medico m
        WHERE m.usuario_id = %s
    """, (id_usuario,))
    med = cur.fetchone()
    if not med:
        print("No se encontró el médico asociado a este usuario.")
        cur.close(); conn.close()
        return

    id_medico = med[0]

    # 2) Traemos las especialidades del médico
    cur.execute("""
        SELECT mhe.Especialidad_id_especialidad
        FROM Medico_has_Especialidad mhe
        WHERE mhe.Medico_id_medico = %s
    """, (id_medico,))
    esp_rows = cur.fetchall()
    if not esp_rows:
        print("El médico no tiene especialidades asociadas.")
        cur.close(); conn.close()
        return

    esp_ids = [r[0] for r in esp_rows]

    # 3) Traemos los turnos de esas especialidades
    formato_in = ",".join(["%s"] * len(esp_ids))
    query = f"""
        SELECT t.id_turno, t.fecha, t.hora,
               CONCAT(p.Nombre, ' ', p.Apellido) AS Paciente,
               e.Nombre AS Especialidad
        FROM Turno t
        JOIN Paciente p ON p.id_paciente = t.Paciente_id_paciente
        JOIN Especialidad e ON e.id_especialidad = t.Especialidad_id_especialidad
        WHERE t.Especialidad_id_especialidad IN ({formato_in})
        ORDER BY t.fecha DESC, t.hora DESC
    """
    cur.execute(query, esp_ids)
    rows = cur.fetchall()
    cur.close(); conn.close()

    if not rows:
        print("No hay turnos en tus especialidades.")
        return

    headers = ["Código", "Fecha", "Hora", "Paciente", "Especialidad"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
