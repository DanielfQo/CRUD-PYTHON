import unittest
from app import app

class TestRouterLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_inicio_logged_in(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True  # Usuario autenticado
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
            sess['conectado'] = True  # Usuario autenticado
        response = self.app.get('/closed-session')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
