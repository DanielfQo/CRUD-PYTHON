import unittest
from unittest.mock import patch, MagicMock
from controllers.funciones_login import recibeInsertRegisterUser, validarDataRegisterLogin, info_perfil_session
from app import app

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

        with app.test_request_context():  # Contexto de solicitud
            result = info_perfil_session()
            self.assertEqual(result, [{'name_surname': 'John Doe', 'email_user': 'john@example.com'}])

if __name__ == '__main__':
    unittest.main()
