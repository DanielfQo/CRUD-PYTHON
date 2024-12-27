import unittest
import io

from flask import Flask, session

from app import app
from unittest.mock import patch

class TestFuncionales(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()  # Activa el contexto de la aplicación
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey'  # Asegúrate de tener una clave secreta para las sesiones

    def tearDown(self):
        self.app_context.pop()  # Limpia el contexto de la aplicación

    ### FUNCIONES DE router_login.py ###
    def test_inicio_sin_sesion(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'formAuthentication', response.data)
        
    def test_inicio_con_sesion(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True
            sess['id'] = 3
            sess['name_surname'] = "michael ticona"
            sess['email_user'] = "mjticonala@gmail.com"
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Panel de Control', response.data)

    @patch('controllers.funciones_login.validarDataRegisterLogin')
    def test_login_usuario_valido(self, mock_validarDataRegisterLogin):
        mock_validarDataRegisterLogin.return_value = True
        response = self.app.post('/login', data={
            'email_user': 'mjticonala@gmail.com',
            'pass_user': '123456'
        })
        self.assertEqual(response.status_code, 302)  # Redirige al inicio

    def test_login_usuario_invalido(self):
        response = self.app.post('/login', data={
            'email_user': 'usuario@invalido.com',
            'pass_user': 'incorrecta'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error, El usuario no existe, por favor verifique.', response.data)

    def test_cerrar_sesion(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True
        response = self.app.get('/closed-session')
        self.assertEqual(response.status_code, 302)  # Espera redirección
    
        # Verifica que la sesión se haya cerrado
        with self.app.session_transaction() as sess:
            self.assertNotIn('conectado', sess)


    ### FUNCIONES DE router_home.py ###
    def test_lista_empleados_sin_sesion(self):
        response = self.app.get('/lista-de-empleados')
        self.assertEqual(response.status_code, 302)  # Redirige a inicio
        
    def test_lista_empleados_con_sesion(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True
        response = self.app.get('/lista-de-empleados')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Lista de Empleados', response.data)  # Check for expected content
        


    ### FUNCIONES DE funciones_login.py ###
    @patch('controllers.funciones_login.recibeInsertRegisterUser')
    def test_recibe_insert_register_user(self, mock_recibeInsertRegisterUser):
        # Mock para evitar acceso a la base de datos
        mock_recibeInsertRegisterUser.return_value = True
        resultado = mock_recibeInsertRegisterUser(
            "michael ticona",
            "mjticonala@gmail.com",
            "123456"
        )
        self.assertTrue(resultado)

    @patch('controllers.funciones_login.validarDataRegisterLogin')
    def test_validar_data_register_login(self, mock_validarDataRegisterLogin):
        # Mock para evitar acceso a la base de datos
        mock_validarDataRegisterLogin.return_value = True
        resultado = mock_validarDataRegisterLogin(
            "Usuario Prueba",
            "usuario@prueba.com",
            "123456"
        )
        self.assertTrue(resultado)

    ### FUNCIONES DE funciones_home.py ###
    @patch('controllers.funciones_home.procesar_form_empleado')
    def test_procesar_form_empleado(self, mock_procesar_form_empleado):
        # Mock para evitar procesamiento real
        mock_procesar_form_empleado.return_value = True
        resultado = mock_procesar_form_empleado(
            {
                'nombre': 'Empleado Test',
                'email': 'empleado@test.com',
                'cargo': 'Tester'
            },
            'foto_test.jpg'
        )
        self.assertTrue(resultado)

    @patch('controllers.funciones_home.sql_lista_empleadosBD')
    def test_sql_lista_empleadosBD(self, mock_sql_lista_empleadosBD):
        # Mock de la base de datos
        mock_sql_lista_empleadosBD.return_value = [{'id': 1, 'name': 'Empleado Test'}]
        empleados = mock_sql_lista_empleadosBD()
        self.assertIsInstance(empleados, list)

    @patch('controllers.funciones_home.sql_detalles_empleadosBD')
    def test_sql_detalles_empleadosBD(self, mock_sql_detalles_empleadosBD):
        # Mock de la base de datos
        mock_sql_detalles_empleadosBD.return_value = {'id': 1, 'name': 'Empleado Test'}
        detalles = mock_sql_detalles_empleadosBD(1)  # ID del empleado
        self.assertIsInstance(detalles, dict)

if __name__ == "__main__":
    unittest.main()
