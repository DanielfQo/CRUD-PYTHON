import unittest
from unittest.mock import patch, MagicMock
from app import app
from controllers.funciones_home import (
    sql_lista_empleadosBD, procesar_form_empleado, buscarEmpleadoBD
)
from controllers.funciones_login import (
    recibeInsertRegisterUser, validarDataRegisterLogin, info_perfil_session
)

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


class TestFuncionesLogin(unittest.TestCase):

    @patch('controllers.funciones_login.connectionBD')
    def test_recibeInsertRegisterUser(self, mock_connection):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        result = recibeInsertRegisterUser('John Doe', 'john@example.com', 'password123')
        self.assertEqual(result, 1)

    @patch('controllers.funciones_login.connectionBD')
    def test_validarDataRegisterLogin(self, mock_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        result = validarDataRegisterLogin('John Doe', 'john@example.com', 'password123')
        self.assertTrue(result)

    @patch('controllers.funciones_login.connectionBD')
    def test_info_perfil_session(self, mock_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'name_surname': 'John Doe', 'email_user': 'john@example.com'}]
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        result = info_perfil_session()
        self.assertEqual(result, [{'name_surname': 'John Doe', 'email_user': 'john@example.com'}])


class TestRouterHome(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_lista_empleados(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True
        response = self.app.get('/lista-de-empleados')
        self.assertEqual(response.status_code, 200)

    def test_view_form_empleado_not_logged_in(self):
        response = self.app.get('/registrar-empleado')
        self.assertEqual(response.status_code, 302)  # Redirige a inicio


class TestRouterLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_inicio_logged_in(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_inicio_not_logged_in(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.app.post('/login', data={
            'email_user': 'john@example.com',
            'pass_user': 'password123'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True
        response = self.app.get('/closed-session')
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
