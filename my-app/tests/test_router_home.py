import unittest
from routers.router_home import app

class TestRouterHome(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_lista_empleados(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True  # Simular usuario autenticado
        response = self.app.get('/lista-de-empleados')
        self.assertEqual(response.status_code, 200)

    def test_view_form_empleado_not_logged_in(self):
        response = self.app.get('/registrar-empleado')
        self.assertEqual(response.status_code, 302)  # Redirige a inicio

if __name__ == '__main__':
    unittest.main()
