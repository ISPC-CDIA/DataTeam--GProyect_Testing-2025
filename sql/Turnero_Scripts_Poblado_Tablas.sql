-- Merged initial seed script (Departamentos/Especialidades/Horarios/Medicos/Pacientes/Turnos + Roles/Usuarios)
USE Turnero;

-- Roles base
INSERT IGNORE INTO Rol (nombre) VALUES ('admin'), ('empleado'), ('medico'), ('paciente');

-- Usuarios de ejemplo (password_hash TEMP; luego se reemplaza por hash real con Python)
INSERT INTO Usuario (username, email, password_hash, dni, id_rol)
SELECT 'admin', 'admin@demo.local', 'TEMP', NULL, r.id_rol FROM Rol r WHERE r.nombre='admin'
ON DUPLICATE KEY UPDATE email=VALUES(email);

INSERT INTO Usuario (username, email, password_hash, dni, id_rol)
SELECT 'medico_mario', 'mario.sanchez@demo.local', 'TEMP', NULL, r.id_rol FROM Rol r WHERE r.nombre='medico'
ON DUPLICATE KEY UPDATE email=VALUES(email);

INSERT INTO Usuario (username, email, password_hash, dni, id_rol)
SELECT 'paciente_abdala', 'mario.abdala@demo.local', 'TEMP', 28740858, r.id_rol FROM Rol r WHERE r.nombre='paciente'
ON DUPLICATE KEY UPDATE email=VALUES(email);

-- Departamentos
INSERT INTO Turnero.Departamento (nombre) VALUES ('Medicina'); -- 1
INSERT INTO Turnero.Departamento (nombre) VALUES ('Diagnóstico por Imágenes'); -- 2
INSERT INTO Turnero.Departamento (nombre) VALUES ('Laboratorio'); -- 3

-- Especialidades
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Clínica',1); -- 1
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Pediatría',1); -- 2
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Ortopedia y Traumatología',1); -- 3
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Cardiología',1); -- 4
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Urología',1); -- 5
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Oftalmología',1); -- 6
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Otorrinolaringología',1); -- 7
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Dermatología',1); -- 8
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Gastroenterología',1); -- 9
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Endocrinología',3); -- 10
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Hematología',3); -- 11
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Bioquímica',3); -- 12
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Radiología',2); -- 13
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Ecografía',2); -- 14
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Tomografía',2); -- 15
INSERT INTO Turnero.Especialidad (Nombre, Departamento_id_departamento) VALUES ('Resonancia Magnética',2); -- 16

-- Horarios
INSERT INTO Turnero.Horario (hora_inicio, hora_fin) VALUES (0,4); -- 1
INSERT INTO Turnero.Horario (hora_inicio, hora_fin) VALUES (4,8); -- 2
INSERT INTO Turnero.Horario (hora_inicio, hora_fin) VALUES (8,12); -- 3
INSERT INTO Turnero.Horario (hora_inicio, hora_fin) VALUES (12,16); -- 4
INSERT INTO Turnero.Horario (hora_inicio, hora_fin) VALUES (16,20); -- 5
INSERT INTO Turnero.Horario (hora_inicio, hora_fin) VALUES (20,0); -- 6

-- Médicos (sin usuario aún; luego vinculamos al 1)
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Mario', 'Sánchez', 1); -- 1
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Juan', 'Pérez', 2); -- 2
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('María', 'González', 3); -- 3
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Carlos', 'Gómez', 4); -- 4
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Ana', 'Martínez', 5); -- 5
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Pedro', 'Rodríguez', 6); -- 6
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Marta', 'López', 1); -- 7
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Jorge', 'Fernández', 2); -- 8
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Silvia', 'Díaz', 3); -- 9
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Luis', 'Alvarez', 4); -- 10
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Laura', 'Romero', 5); -- 11
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Fernando', 'Suárez', 6); -- 12
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Gabriela', 'Torres', 1); -- 13
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Ricardo', 'Giménez', 2); -- 14
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Verónica', 'Paz', 3); -- 15
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Hernán', 'Ríos', 4); -- 16
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Cecilia', 'Vega', 5); -- 17
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Gustavo', 'Luna', 6); -- 18
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Dario', 'Medina', 1); -- 19
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Carlos', 'Leguizamon', 2); -- 20
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Erika', 'Costa', 3); -- 21
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Ariel', 'Fernandez', 4); -- 22
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Alicia', 'Martínez', 5); -- 23
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Pablo', 'Casanova', 6); -- 24
INSERT INTO Turnero.Medico (Nombre, Apellido, Horario_id_Horario) VALUES ('Pedro', 'Pensa', 1); -- 25

-- Vincular usuario médico al registro de Medico (id=1)
UPDATE Medico m
JOIN Usuario u ON u.username='medico_mario'
SET m.usuario_id = u.id_usuario
WHERE m.id_medico = 1;

-- Relación médico-especialidad
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (1,1);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (2,2);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (3,3);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (4,4);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (5,5);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (6,6);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (7,7);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (8,8);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (9,9);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (10,10);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (11,11);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (12,12);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (13,13);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (14,14);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (15,15);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (16,16);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (17,1);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (18,2);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (19,3);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (20,4);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (21,5);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (22,6);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (23,7);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (24,8);
INSERT INTO Turnero.Medico_has_Especialidad (Medico_id_medico, Especialidad_id_especialidad) VALUES (25,9);

-- Pacientes (incluye a 'Mario Abdala' con DNI 28740858)
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Lucía', 'Gómez', 12345678); -- 1
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Martín', 'Pérez', 23456789); -- 2
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Sofía', 'Martínez', 34567890); -- 3
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Mateo', 'González', 45678901); -- 4
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Valentina', 'Rodríguez', 56789012); -- 5
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Benjamín', 'López', 67890123); -- 6
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Isabella', 'Fernández', 78901234); -- 7
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Tomás', 'Díaz', 89012345); -- 8
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Olivia', 'Suárez', 90123456); -- 9
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Agustín', 'Torres', 12345678); -- 10
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Emma', 'Giménez', 23456789); -- 11
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Dylan', 'Paz', 34567890); -- 12
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Mía', 'Ríos', 45678901); -- 13
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Lucas', 'Vega', 56789012); -- 14
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Renata', 'Luna', 67890123); -- 15
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Joaquín', 'Alvarez', 78901234); -- 16
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Emilia', 'Romero', 89012345); -- 17
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Bautista', 'Martínez', 90123456); -- 18
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Catalina', 'González', 12345678); -- 19
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Felipe', 'Pérez', 23456789); -- 20
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Mario', 'Abdala', 28740858); -- 21 (ejemplo de paciente con usuario)

-- Vincular usuario paciente por DNI
UPDATE Paciente p
JOIN Usuario u ON u.username='paciente_abdala'
SET p.usuario_id = u.id_usuario
WHERE p.DNI = 28740858;

-- Turnos (idénticos a tus seeds originales)
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2024-07-01', 10, 1, 1); -- 1
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2024-07-03', 8, 2, 2); -- 2
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2024-07-02', 12, 3, 3); -- 3
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2024-07-04', 15, 4, 4); -- 4
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2024-07-05', 16, 5, 5); -- 5
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2024-07-06', 18, 6, 6); -- 6
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2024-07-07', 20, 7, 7); -- 7
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2024-07-08', 10, 8, 8); -- 8
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2024-07-09', 8, 9, 9); -- 9
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2024-07-10', 12, 10, 10); -- 10
-- (puedes seguir pegando el resto de tus inserts de Turno aquí si los necesitas todos)
