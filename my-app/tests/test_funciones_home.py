import unittest
from unittest.mock import patch, MagicMock
from controllers.funciones_home import sql_lista_empleadosBD, procesar_form_empleado, buscarEmpleadoBD

class TestFuncionesHome(unittest.TestCase):

    @patch('controllers.funciones_home.connectionBD')
    def test_sql_lista_empleadosBD(self, mock_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'John Doe'}]
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        result = sql_lista_empleadosBD()
        self.assertEqual(result, [{'id': 1, 'name': 'John Doe'}])

    @patch('controllers.funciones_home.connectionBD')
    def test_buscarEmpleadoBD(self, mock_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'id': 2, 'name': 'Jane Doe'}]
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        result = buscarEmpleadoBD('Jane')
        self.assertEqual(result, [{'id': 2, 'name': 'Jane Doe'}])

    @patch('controllers.funciones_home.guardar_imagen')
    @patch('controllers.funciones_home.connectionBD')
    def test_procesar_form_empleado(self, mock_connection, mock_guardar_imagen):
        mock_cursor = MagicMock()
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        mock_guardar_imagen.return_value = '/path/to/image.jpg'

        form_data = {'name': 'Employee Name', 'email': 'employee@example.com'}
        foto = MagicMock()
        result = procesar_form_empleado(form_data, foto)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
