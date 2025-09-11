from conectar_base_datos import conectar_base_datos
from tabulate import tabulate

def consultar_turno():
    conn = conectar_base_datos()
    cursor = conn.cursor()

    print('- Consulta de Turnos -')
    while True:
        print('1. Consultar turnos por paciente.')
        print('2. Consultar todos los turnos.')
        print('0. Salir.')

        # Comprobación de la opción del usuario -> Se contempla la necesidad del usuario de salir sin avanzar o el error humano y el tipeo erroeno.
        while True:
            try:        
                user_opt = (int(input()))
                if user_opt in [0, 1, 2]:
                    break
                else:
                    print("Por favor, ingrese un número entre 0 y 2.")
            except ValueError:
                print("Por favor, ingrese un número correcto.")

        # Opción: Salir -> Finaliza el módulo
        if user_opt == 0:
            print('Cerrando Módulo Consultas...')
            break
        
        # Solicitamos DNI para comenzar la busqueda en la DB
        if user_opt == 1:
            user_dni = input('Ingrese su DNI: ')

            # Querida DB, buscame este DNI, porfis.
            #ah, y si podes realizar un JOIN para presentar en una nueva tabla los datos de 3 tablas (Turnos, Especialdiad y Paciente)
            cursor.execute("""SELECT t.id_turno,
                                     t.fecha,
                                     CONCAT(p.Nombre, ' ', p.Apellido) AS Nombre_Paciente,
                                     e.Nombre AS Nombre_Especialidad
                              FROM Turno t
                              INNER JOIN Paciente p ON t.Paciente_id_paciente = p.id_paciente
                              INNER JOIN Especialidad e ON t.Especialidad_id_especialidad = e.id_especialidad
                              WHERE p.DNI = %s
                              ORDER BY t.fecha DESC, Nombre_Paciente ASC, Nombre_Especialidad ASC;""", (user_dni,))
            turnos = cursor.fetchall()

            # Devolución por consola -> Tabulate para la presentación
            if turnos:
                user_a = turnos[0][0]  
                print("Los turnos para el paciente", user_a, "son:")
                
                headers = ["Código", "Fecha", "Nombre Completo", "Especialidad"]
                tabla_turnos = [[turno[0], turno[1], turno[2], turno[3]] for turno in turnos]
                
                print(tabulate(tabla_turnos, headers=headers, tablefmt="grid"))
            else:
                #Si no se encuentra el DNI cargado, se contempla un mensaje de alerta.
                print('No se encontraron turnos para el DNI', user_dni)
            break
        
        # Si se solicita la 'opión 2' llama la función general.
        if user_opt == 2:
            consulta_global()
        break

    conn.close()
