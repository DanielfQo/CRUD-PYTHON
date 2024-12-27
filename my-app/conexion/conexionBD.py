import mysql.connector

def connectionBD():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="123456",
            database="crud_python",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )
        if connection.is_connected():
            # print("Conexión exitosa a la BD")
            return connection
        else:
            print("No se pudo establecer la conexión a la base de datos.")
            return None
    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")
        return None
