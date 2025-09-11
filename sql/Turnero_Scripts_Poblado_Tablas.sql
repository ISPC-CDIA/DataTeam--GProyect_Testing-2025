-- Merged initial seed script (Departamentos/Especialidades/Horarios/Medicos/Pacientes/Turnos + Roles/Usuarios)
USE Turnero;

-- Roles base
INSERT IGNORE INTO Rol (nombre) VALUES ('admin'), ('empleado'), ('medico'), ('paciente');

-- Usuarios de ejemplo 
INSERT INTO Usuario (username, email, password_hash, dni, id_rol)
SELECT 'admin', 'admin@demo.local', 'admin123', NULL, r.id_rol
FROM Rol r WHERE r.nombre='admin'
ON DUPLICATE KEY UPDATE email=VALUES(email), password_hash='admin123';

INSERT INTO Usuario (username, email, password_hash, dni, id_rol)
SELECT 'medico_mario', 'mario.sanchez@demo.local', 'medico123', NULL, r.id_rol
FROM Rol r WHERE r.nombre='medico'
ON DUPLICATE KEY UPDATE email=VALUES(email), password_hash='medico123';

INSERT INTO Usuario (username, email, password_hash, dni, id_rol)
SELECT 'paciente_abdala', 'mario.abdala@demo.local', 'paciente123', 28740858, r.id_rol
FROM Rol r WHERE r.nombre='paciente'
ON DUPLICATE KEY UPDATE email=VALUES(email), password_hash='paciente123';

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

-- Pacientes 
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Lucía', 'Gómez', 12345678); -- 1
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Martín', 'Pérez', 23456789); -- 2
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Sofía', 'Martínez', 34567590); -- 3
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Mateo', 'González', 35678901); -- 4
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Valentina', 'Rodríguez', 26789012); -- 5
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Benjamín', 'López', 37890123); -- 6
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Isabella', 'Fernández', 38901234); -- 7
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Tomás', 'Díaz', 89012345); -- 8
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Olivia', 'Suárez', 20123456); -- 9
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Agustín', 'Torres', 12545678); -- 10
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Emma', 'Giménez', 23456879); -- 11
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Dylan', 'Paz', 34567890); -- 12
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Mía', 'Ríos', 45678901); -- 13
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Lucas', 'Vega', 56789012); -- 14
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Renata', 'Luna', 67890123); -- 15
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Joaquín', 'Alvarez', 28901234); -- 16
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Emilia', 'Romero', 39012345); -- 17
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Bautista', 'Martínez', 30123456); -- 18
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Catalina', 'González', 19345679); -- 19
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Felipe', 'Pérez', 23456780); -- 20
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Mario', 'Abdala', 28740858); -- 21 (ejemplo de paciente con usuario)
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Luisa', 'Aguero', 29651813); -- 22
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Carlos', 'Aguilera', 40184442); -- 23
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Adriana', 'Alfonso', 26104249); -- 24
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Eugenia', 'Aleu', 32997809); -- 25
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Daniela', 'Algan', 35794895); -- 26
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Pablo', 'Barlesi', 27589790); -- 27
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Ariel', 'Barnech', 38354542); -- 28
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Gustavo', 'Barrios', 34180521); -- 29
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Erik', 'Baum', 24021740); -- 30
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Sergio', 'Barreto', 17999076); -- 31
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Gabriel', 'Barreiro', 11765715); -- 32
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Marcela', 'Blasco', 26104497); -- 33
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Carolina', 'Cabral', 25351240); -- 34
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Juana', 'Caceres', 27848583); -- 35
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Gerardo', 'Caci', 22539579); -- 36
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Amadeo', 'Caballero', 33784897); -- 37
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Valeria', 'Bustos', 16576347); -- 38
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Luis', 'Calcagno', 24500499); -- 39
INSERT INTO Turnero.Paciente (Nombre, Apellido, DNI) VALUES ('Florencia', 'Camejo', 25731636); -- 40

-- Vincular usuario paciente por DNI
UPDATE Paciente p
JOIN Usuario u ON u.username='paciente_abdala'
SET p.usuario_id = u.id_usuario
WHERE p.DNI = 28740858;

-- Turnos 
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-01', 10, 1, 1); -- 1
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-03', 8, 2, 2); -- 2
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-02', 12, 3, 3); -- 3
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-04', 15, 4, 4); -- 4
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-05', 16, 5, 5); -- 5
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-06', 18, 6, 6); -- 6
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-07', 20, 7, 7); -- 7
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-08', 10, 8, 8); -- 8
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-09', 8, 9, 9); -- 9
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-10', 12, 10, 10); -- 10
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-11', 15, 11, 11); -- 11
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-12', 16, 12, 12); -- 12
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-13', 18, 13, 13); -- 13
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-14', 20, 14, 14); -- 14
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-15', 10, 15, 15); -- 15
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-16', 8, 16, 16); -- 16
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-17', 12, 17, 1); -- 17
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-18', 15, 18, 2); -- 18
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-19', 16, 19, 3); -- 19
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-20', 18, 20, 4); -- 20
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-01', 8, 21, 5); -- 21
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-03', 9, 22, 6); -- 22
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-02', 10, 23, 7); -- 23
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-04', 11, 24, 8); -- 24
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-05', 12, 25, 9); -- 25
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-06', 13, 26, 10); -- 26
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-07', 14, 27, 11); -- 27
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-08', 15, 28, 12); -- 28
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-09', 16, 29, 13); -- 29
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-10', 17, 30, 14); -- 30
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-11', 18, 31, 15); -- 31
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-12', 19, 32, 16); -- 32
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-13', 20, 33, 1); -- 33
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-14', 8, 34, 2); -- 34
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-15', 9, 35, 3); -- 35
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-16', 8, 36, 4); -- 36
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-17', 10, 37, 5); -- 37
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-18', 11, 38, 6); -- 38
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-19', 12, 39, 7); -- 39
INSERT INTO Turnero.Turno (Fecha, Hora, Paciente_id_paciente, Especialidad_id_especialidad) VALUES ('2025-07-20', 13, 40, 8); -- 40
