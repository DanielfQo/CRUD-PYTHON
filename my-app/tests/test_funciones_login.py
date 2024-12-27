import unittest
from unittest.mock import patch, MagicMock
from flask import session
from controllers.funciones_login import recibeInsertRegisterUser, validarDataRegisterLogin, info_perfil_session
from app import app

class TestFuncionesLogin(unittest.TestCase):

    @patch('conexion.conexionBD.connectionBD')
    @patch('my_app.controllers.funciones_login.validarDataRegisterLogin', return_value=True)
    def test_recibeInsertRegisterUser(self, mock_connection):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        result = recibeInsertRegisterUser('John', 'john@example.com', 'password123')
        self.assertEqual(result, True)

    @patch('conexion.conexionBD.connectionBD')
    @patch('controllers.funciones_login.validarDataRegisterLogin', return_value=False)
    def test_validarDataRegisterLogin(self, mock_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'name_surname': 'michael', 'email_user': 'mjticonala@gmail', 'password': '123456'}
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        result = validarDataRegisterLogin('michael ticona', 'mjticonal@gmail.com', '123456')
        self.assertFalse(result)

    @patch('conexion.conexionBD.connectionBD')
    def test_info_perfil_session(self, mock_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'name_surname': 'Urian', 'email_user': 'dev@gmail.com'}]
        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['id'] = 1  # Asegúrate de que la sesión tenga la clave 'id'
            # Verifica que 'id' esté en la sesión después de configurarla
            self.assertIn('id', sess)  # Verifica que 'id' esté en la sesión
            result = info_perfil_session(sess['id'])
            self.assertEqual(result, [{'name_surname': 'Urian', 'email_user': 'dev@gmail.com'}])

  
if __name__ == '__main__':
    unittest.main()
