import unittest
from routers.router_login import app

class TestRouterLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_inicio_logged_in(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True  # Usuario autenticado
            sess['id'] = 1  # Add user id to session
            sess.modified = True
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_inicio_not_logged_in(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.app.post('/login', data={
            'email_user': 'john@example.com',
            'pass_user': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        with self.app.session_transaction() as sess:
            sess['conectado'] = True  # Usuario autenticado
            sess['id'] = 1
            sess['name_surname'] = 'John Doe'
            sess['email'] = 'john.doe@example.com'

        response = self.app.get('/closed-session')
        self.assertEqual(response.status_code, 302)
        
        with self.app.session_transaction() as sess:
            self.assertNotIn('conectado', sess)
            self.assertNotIn('id', sess)
            self.assertNotIn('name_surname', sess)
            self.assertNotIn('email', sess)

if __name__ == '__main__':
    unittest.main()
