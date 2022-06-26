from django.test import RequestFactory, TestCase
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user

from .models import User


# Create your tests here.
class SSOTesting(TestCase):
    
    # create mock user
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="user123", email="user123@gmail.com", password="123"
        )
    
    # login route: if not logged in render login page
    def test_login_get(self):
        c = Client()
        response = c.get('/sso/login')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/login.html")
    
    # login route: redirect the user to dashboard if user already logged in
    def test_login_get_loggedin(self):
        c = Client()
        c.login(username="user123", password="123")
        response = c.get('/sso/login')
        self.assertRedirects(response, reverse("livequiz:index"), status_code=302)
    
    # login route: valid log in post request, then redirect to dashboard
    def test_login_post_valid(self):
        c = Client()
        response = c.post("/sso/login", {"username": "user123", "password": "123",})
        user = get_user(c)
        self.assertTrue(user, user.is_authenticated)
        self.assertRedirects(response, reverse("livequiz:index"), status_code=302)
    
    # login route: invalid log in, do not log in and rerender same page with message
    def test_login_post_invalid(self):
        c = Client()
        response = c.post("/sso/login", {"username": "user123", "password": "456",})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/login.html")
        self.assertIsInstance(response.context["message"], str)
        
    # logout route: log the user out and render logout page
    def test_logout_get_loggedin(self):
        c = Client()
        c.login(username="user123", password="123")
        response = c.get('/sso/logout')
        user = get_user(c)
        self.assertTrue(user.is_anonymous)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/logout.html")
    
    # logout route: logged out user should only see the page and nothing happens
    def test_logout_get_loggedout(self):
        c = Client()
        response = c.get('/sso/logout')
        user = get_user(c)
        self.assertTrue(user.is_anonymous)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/logout.html")
    
    # register route: if not logged in render register page
    def test_register_get(self):
        c = Client()
        response = c.get('/sso/register')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/register.html")
        
    # register route: if logged in redirect to dashboard
    def test_register_get_loggedin(self):
        c = Client()
        c.login(username="user123", password="123")
        response = c.get('/sso/register')
        self.assertRedirects(response, reverse("livequiz:index"), status_code=302)
        
    # register post case1: email cannot be empty 
    def test_register_post_case1(self):
        c = Client()
        response = c.post("/sso/register", {"username": "user456", "email": "",})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/register.html")
        self.assertIsInstance(response.context["message"], str)
        
    # register post case2: username cannot be empty 
    def test_register_post_case2(self):
        c = Client()
        response = c.post("/sso/register", {"username": "", "email": "user456@gmail.com",})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/register.html")
        self.assertIsInstance(response.context["message"], str)
    
    # register post case3: password does not match confirmation
    def test_register_post_case3(self):
        c = Client()
        response = c.post("/sso/register", {"username": "user456", "email": "user456@gmail.com",
                                            "password": "123", "confirmation": "456"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/register.html")
        self.assertIsInstance(response.context["message"], str)
    
    # register post case4: password too simple
    def test_register_post_case4(self):
        c = Client()
        response = c.post("/sso/register", {"username": "user456", "email": "user456@gmail.com",
                                            "password": "12345", "confirmation": "12345"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/register.html")
        self.assertIsInstance(response.context["message"], str)
    
    # register post case5: username already taken
    def test_register_post_case5(self):
        c = Client()
        response = c.post("/sso/register", {"username": "user123", "email": "user456@gmail.com",
                                            "password": "fs7&3kdfs903.", "confirmation": "fs7&3kdfs903."})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sso/register.html")
        self.assertIsInstance(response.context["message"], str)
        
    # register post case6: all fields filled, not clashing with existing username, hard password
    def test_register_post_case6(self):
        c = Client()
        response = c.post("/sso/register", {"username": "user456", "email": "user456@gmail.com",
                                            "password": "fs7&3kdfs903.", "confirmation": "fs7&3kdfs903."})
        user = get_user(c)
        self.assertFalse(user.is_anonymous)
        self.assertRedirects(response, reverse("livequiz:index"), status_code=302)
    
    # comingsoon route: render coming soon page
    def test_comingsoon_view(self):
        c = Client()
        response = c.get('/sso/comingsoon')
        user = get_user(c)
        self.assertTrue(user.is_anonymous)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout/comingsoon.html")
