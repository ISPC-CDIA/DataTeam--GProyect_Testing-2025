from mysql import connector

# modificar los datos entre comillas por los correspondientes con sus credenciales de acceso configuradas en la instalación de MySQL
def conectar_base_datos():
    return connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="Turnero"
    )
