import unittest
from flask import Flask, session
from app import app

class TestFuncionales(unittest.TestCase):
    def setUp(self):
        # Configuración inicial
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        app.config['TESTING'] = True

    def tearDown(self):
        # Limpiar el contexto después de las pruebas
        self.app_context.pop()

    ### FUNCIONES DE router_login.py ###
    def test_inicio_sin_sesion(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'base_login.html', response.data)

    def test_inicio_con_sesion(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True
            sess['id'] = 1
            sess['name_surname'] = "Usuario Prueba"
            sess['email_user'] = "usuario@prueba.com"
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'base_cpanel.html', response.data)

    def test_login_usuario_valido(self):
        response = self.app.post('/login', data={
            'email_user': 'usuario@prueba.com',
            'pass_user': '123456'
        })
        self.assertEqual(response.status_code, 302)  # Redirige al inicio

    def test_login_usuario_invalido(self):
        response = self.app.post('/login', data={
            'email_user': 'usuario@invalido.com',
            'pass_user': 'incorrecta'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'datos incorrectos', response.data)

    def test_cerrar_sesion(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True
        response = self.app.get('/closed-session')
        self.assertEqual(response.status_code, 302)
        with self.app as client:
            response = client.get('/')
            self.assertNotIn('conectado', session)

    ### FUNCIONES DE router_home.py ###
    def test_lista_empleados_sin_sesion(self):
        response = self.app.get('/lista-de-empleados')
        self.assertEqual(response.status_code, 302)  # Redirige a inicio

    def test_lista_empleados_con_sesion(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True
        response = self.app.get('/lista-de-empleados')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lista_empleados.html', response.data)

    def test_registrar_empleado(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True
        response = self.app.post('/form-registrar-empleado', data={
            'nombre': 'Empleado Prueba',
            'email': 'empleado@prueba.com'
        })
        self.assertEqual(response.status_code, 302)

    ### FUNCIONES DE funciones_login.py ###
    def test_recibe_insert_register_user(self):
        from controllers.funciones_login import recibeInsertRegisterUser
        resultado = recibeInsertRegisterUser(
            "Usuario Prueba",
            "usuario@prueba.com",
            "123456"
        )
        self.assertTrue(resultado)

    def test_validar_data_register_login(self):
        from controllers.funciones_login import validarDataRegisterLogin
        resultado = validarDataRegisterLogin(
            "Usuario Prueba",
            "usuario@prueba.com",
            "123456"
        )
        self.assertTrue(resultado)

    ### FUNCIONES DE funciones_home.py ###
    def test_procesar_form_empleado(self):
        from controllers.funciones_home import procesar_form_empleado
        resultado = procesar_form_empleado(
            {
                'nombre': 'Empleado Test',
                'email': 'empleado@test.com',
                'cargo': 'Tester'
            },
            'foto_test.jpg'
        )
        self.assertTrue(resultado)

    def test_sql_lista_empleadosBD(self):
        from controllers.funciones_home import sql_lista_empleadosBD
        empleados = sql_lista_empleadosBD()
        self.assertIsInstance(empleados, list)

    def test_sql_detalles_empleadosBD(self):
        from controllers.funciones_home import sql_detalles_empleadosBD
        detalles = sql_detalles_empleadosBD(1)  # ID del empleado
        self.assertIsInstance(detalles, dict)

if __name__ == "__main__":
    unittest.main()
