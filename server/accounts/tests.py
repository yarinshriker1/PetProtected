from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


class AccountsViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        
    def test_register_user(self):
        response = self.client.post('/accounts/register',
                                    content_type="application/json",
                                    data={
                                        'email': "test@test.com",
                                        'username': "test",
                                        'first_name': 'first test',
                                        'last_name': 'last test',
                                        'password': 'password',
                                        'phone_number': '111111111',
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        self.assertEqual(User.objects.count(), 2)  # admin + created user
        created_user = User.objects.get(username="test")
        self.assertEqual(created_user.email, "test@test.com")
        self.assertEqual(created_user.first_name, "first test")
        self.assertEqual(created_user.last_name, "last test")
        self.assertEqual(created_user.profile.phone_number, '111111111')
        self.assertTrue(created_user.is_authenticated)

        
    def test_get_users(self):
        test_user = User.objects.create_user(username='test', password='password', last_name="last test",
                                             first_name="first test", email="test@test.com")
        self.client.login(username=test_user.username, password='password')
        response = self.client.get('/accounts/get_users') # {'users': [{'name'...}]}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['users']), 1)

        responded_user = response.json()['users'][0]  # {'name'...}

        self.assertEqual(test_user.username, responded_user['username'])
        self.assertEqual(test_user.email, responded_user['email'])
        self.assertEqual(test_user.first_name, responded_user['first_name'])
        self.assertEqual(test_user.last_name, responded_user['last_name'])
        self.assertEqual(test_user.profile.phone_number, responded_user['profile__phone_number'])
        self.assertEqual(0, responded_user['amount_posts'])
        
        
    def test_login_user(self):
        test_user = User.objects.create_user(username='test', password='password')
        response = self.client.post('/accounts/login',
                                    content_type="application/json",
                                    data={
                                        'username': 'test',
                                        'password': 'password'
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        self.assertTrue(test_user.is_authenticated)

        
    def test_logout_user(self):
        test_user = User.objects.create_user(username='test', password='password')
        self.client.login(username=test_user.username, password='password')
        response = self.client.post('/accounts/logout',
                                    content_type="application/json")
        self.assertEqual(response.status_code, 302)
        
        
    def test_delete_user(self):
        test_user = User.objects.create_user(username='test', password='password', last_name="last test",
                                             first_name="first test", email="test@test.com")
        self.client.login(username='admin', password='admin')
        response = self.client.delete(path='/accounts/delete_user?user_id=' + str(test_user.id))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='test').exists())

