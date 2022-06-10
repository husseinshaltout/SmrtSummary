from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User, auth

class BaseTest(TestCase):
    def setUp(self) -> None:
        self.registerURL = reverse('register')
        self.loginURL = reverse('login')
        self.logoutURL = reverse('logout')
        self.user = {
        'firstname': 'TestFirstName',
        'lastname': 'TestLastName',
        'username': 'username',
        'email': 'username@email.com',
        'password': 'password',
        'password2': 'password',
        }
        self.userAlreadyExist = {
        'firstname': 'TestFirstName',
        'lastname': 'TestLastName',
        'username': 'username',
        'email': 'username1@email.com',
        'password': 'password',
        'password2': 'password',
        }
        self.emailAlreadyExist = {
        'firstname': 'TestFirstName',
        'lastname': 'TestLastName',
        'username': 'username1',
        'email': 'username@email.com',
        'password': 'password',
        'password2': 'password',
        }
        self.userUnmatchingPasswords= {
        'firstname': 'TestFirstName',
        'lastname': 'TestLastName',
        'username': 'username',
        'email': 'username@email.com',
        'password': '123456',
        'password2': '123abc',
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self) -> None:
        response = self.client.get(self.registerURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_can_register_user(self) -> None:
        response = self.client.post(self.registerURL, self.user,format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_username_already_exist(self) -> None:
        response = self.client.post(self.registerURL, self.user,format='text/html')
        response = self.client.post(self.registerURL, self.userAlreadyExist,format='text/html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'That username is taken')
        self.assertRedirects(response, '/accounts/register/')

    def test_email_already_exist(self) -> None:
        response = self.client.post(self.registerURL, self.user,format='text/html')
        response = self.client.post(self.registerURL, self.emailAlreadyExist,format='text/html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'That email is being used')
        self.assertRedirects(response, '/accounts/register/')

    def test_cannot_register_user_with_unmatching_passwords(self) -> None:
        response = self.client.post(self.registerURL, self.userUnmatchingPasswords,format='text/html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Passwords do not match')
        self.assertRedirects(response, '/accounts/register/')


class LoginTest(BaseTest):
    def test_can_view_page_correctly(self) -> None:
        response = self.client.get(self.loginURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_success(self) -> None:
        self.client.post(self.registerURL, self.user,format='text/html')
        user = User.objects.filter(email=self.user['email']).first()
        user.save()
        response = self.client.post(self.loginURL, self.user,format='text/html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'You are now logged in')
        self.assertRedirects(response, '/dashboard/')
    
    def test_invalid_login(self) -> None:
        self.client.post(self.registerURL, self.user,format='text/html')
        self.client.post(self.logoutURL, self.user,format='text/html')
        response = self.client.post(self.loginURL, {'username':'', 'password':'password'}, format='text/html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 3)
        self.assertEqual(str(messages[2]), 'Invalid credentials')
        self.assertRedirects(response, '/accounts/login/')
        
class LogoutTest(BaseTest):
    def test_logout(self) -> None:
        register = self.client.post(self.registerURL, self.user,format='text/html')
        self.assertEqual(register.status_code, 302)
        response = self.client.post(self.logoutURL, self.user,format='text/html')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Logout')
        self.assertRedirects(response, '/')