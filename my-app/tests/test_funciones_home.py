import unittest
from unittest.mock import patch, MagicMock
from controllers.funciones_home import sql_lista_empleadosBD, procesar_form_empleado, buscarEmpleadoBD

class TestFuncionesHome(unittest.TestCase):

    @patch('conexion.conexionBD.connectionBD')
    def test_sql_lista_empleadosBD(self, mock_connection):
        result = sql_lista_empleadosBD()
        self.assertEqual(result, [
            {
                'id_empleado': 4,
                'nombre_empleado': 'Urian',
                'apellido_empleado': 'Viera',
                'salario_empleado': 3500000,
                'foto_empleado': 'fda30f83ebbc4fb1a2ce2609b2b1e34c6614c1dff6e44460b9ba27ed5bb8e927.png',
                'sexo_empleado': 'Masculino'
            },
        ])

    @patch('conexion.conexionBD.connectionBD') 
    def test_buscarEmpleadoBD(self, mock_connection):
        # Mocking cursor and fetchall return value
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {
            'id_empleado': 4,
            'nombre_empleado': 'Urian',
            'apellido_empleado': 'Viera',
            'salario_empleado': 3500000,
            'foto_empleado': 'fda30f83ebbc4fb1a2ce2609b2b1e34c6614c1dff6e44460b9ba27ed5bb8e927.png',
            'sexo_empleado': 'Masculino'
        }
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        result = buscarEmpleadoBD('Urian')

        # Asegúrate de que el resultado sea el esperado
        self.assertEqual(result, {
            'id_empleado': 4,
            'nombre_empleado': 'Urian',
            'apellido_empleado': 'Viera',
            'salario_empleado': 3500000,
            'foto_empleado': 'fda30f83ebbc4fb1a2ce2609b2b1e34c6614c1dff6e44460b9ba27ed5bb8e927.png',
            'sexo_empleado': 'Masculino'
        })

    @patch('controllers.funciones_home.procesar_imagen_perfil')
    @patch('conexion.conexionBD.connectionBD')
    
    
    def test_procesar_form_empleado(self, mock_connection, mock_procesar_imagen):
        # Mocking image processing and cursor
        mock_cursor = MagicMock()
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        mock_procesar_imagen.return_value = 'test_image.jpg'

        # Form data and photo mock
        form_data = {
            'nombre_empleado': 'Employee Name',
            'apellido_empleado': 'Lastname',
            'sexo_empleado': '1',
            'telefono_empleado': '123456789',
            'email_empleado': 'employee@example.com',
            'profesion_empleado': 'Engineer',
            'salario_empleado': '1000'
        }
        foto = MagicMock(filename='photo.jpg')

        # Call the function
        result = procesar_form_empleado(form_data, foto)

        # Assertions
        self.assertEqual(result, 1)  # Assuming one row affected

if __name__ == '__main__':
    unittest.main()
