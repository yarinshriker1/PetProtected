from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse,resolve
from .views import *
import json


class SharePlaceViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username="test", first_name='test', last_name='tester',
                                             email='test@test.com', password='password')
        self.user.profile.phone_number = '123'
        self.user.save()
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        view = resolve('/')
        self.assertEquals(view.func, home_page)
        self.assertTemplateUsed(response, 'home.html')
        
    def test_about_us_page(self):
        response = self.client.get('/about_us')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        view = resolve('/about_us')
        self.assertEquals(view.func, about_us_page)
        self.assertTemplateUsed(response, 'about_us.html')

        
    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        view = resolve('/login')
        self.assertEquals(view.func, login_page)
        self.assertTemplateUsed(response, 'login.html')

        
    def test_register_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        view = resolve('/register')
        self.assertEquals(view.func, register_page)
        self.assertTemplateUsed(response, 'register.html')
        

        
    def test_profile_page(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        view = resolve('/profile')
        self.assertEquals(view.func, profile_page)
        self.assertTemplateUsed(response, 'profile_page.html')


    def test_management_page(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/management')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        view = resolve('/management')
        self.assertEquals(view.func, management_page)
        self.assertTemplateUsed(response, 'management.html')
      
    def test_get_categories(self):
        response = self.client.get('/get_categories')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {
            'categories': ['Games', 'Clothes', 'Food', 'Textile']
        })
        
        
    def test_get_status(self):
        response = self.client.get('/get_status')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {
            'status': ['Like New', 'Good', 'Slightly damaged', 'Requires repair']
        })


    def test_get_posts__by_category(self):
        for category in Category.objects.all():
            Post.objects.create(
                author=self.user,
                category=category,
                title='post title',
                description='desc',
                status=Product.objects.get(title='Good')
            )
        response = self.client.get('/get_posts?category=Games', content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['posts']), 1)
        expected_post = Post.objects.get(category__title='Games')
        actual_post = response.json()['posts'][0]
        self.assertEqual(expected_post.id, actual_post['id'])
        
        
    def test_get_posts__by_author_id(self):
        User.objects.create_user(username="other", first_name='other', last_name='last',
                                 email='other@other.com', password='password')

        for user in User.objects.all():
            Post.objects.create(
                author=user,
                category=Category.objects.get(title='Games'),
                title='post title',
                description='desc',
                status=Product.objects.get(title='Good')
            )

        response = self.client.get('/get_posts?author__id=' + str(self.user.id), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['posts']), 1)
        expected_post = Post.objects.get(author=self.user)
        actual_post = response.json()['posts'][0]
        self.assertEqual(expected_post.id, actual_post['id'])

    def test_get_posts__by_favorite(self):
        post = Post.objects.create(
            author=self.user,
            category=Category.objects.get(title='Games'),
            title='first',
            description='desc',
            status=Product.objects.get(title='Good')
        )
        Post.objects.create(
            author=self.user,
            category=Category.objects.get(title='Games'),
            title='second',
            description='desc',
            status=Product.objects.get(title='Good')
        )
        Favorite.objects.create(
            user=self.user,
            post=post
        )
        # only authenticated user can ask favorite posts
        self.client.login(username=self.user.username, password='password')
        response = self.client.get('/get_posts?is_favorite=true', content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['posts']), 1)
        actual_post = response.json()['posts'][0]
        self.assertEqual(post.id, actual_post['id'])
        self.assertTrue(actual_post['is_favorite'])


    def test_get_reviews(self):
        review = Review.objects.create(
            Fullname='review',
            title='title',
            description='desc',
            email='test@test.com'
        )
        response = self.client.get('/get_reviews')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {
            'reviews': [
                {
                    'id': review.id,
                    'Fullname': review.Fullname,
                    'title': review.title,
                    'description': review.description,
                    'email': review.email
                }
            ]
        })
        
        
    def test_create_post(self):
        # only authenticated user can create post
        self.client.login(username=self.user.username, password='password')

        data = json.dumps({'title': 'title',
                           'description': 'desc',
                           'category': 'Games',
                           'status': 'Good'
                           })
        response = self.client.post('/create_post', data={'data': data})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'success': True})
        self.assertEqual(Post.objects.count(), 1)
        created_obj = Post.objects.first()
        self.assertEqual(created_obj.title, 'title')
        self.assertEqual(created_obj.description, 'desc')
        self.assertEqual(created_obj.category.title, 'Games')
        self.assertEqual(created_obj.status.title, 'Good')

        

    def test_create_review(self):
        # only authenticated user can create post
        self.client.login(username=self.user.username, password='password')

        response = self.client.post('/create_review', content_type="application/json",
                                    data={
                                        'Fullname': 'test',
                                        'title': 'title',
                                        'description': 'desc',
                                        'email': 'test@test.com'
                                    })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'success': True})
        self.assertEqual(Review.objects.count(), 1)
        created_obj = Review.objects.first()
        self.assertEqual(created_obj.Fullname, 'test')
        self.assertEqual(created_obj.title, 'title')
        self.assertEqual(created_obj.description, 'desc')
        self.assertEqual(created_obj.email, 'test@test.com')
        
    def test_edit_profile(self):
        # only authenticated user can edit profile
        self.client.login(username=self.user.username, password='password')
        response = self.client.post('/edit_profile', content_type="application/json",
                                    data={
                                        'first_name': 'new first',
                                        'last_name': 'new last'
                                    })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'success': True})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'new first')
        self.assertEqual(self.user.last_name, 'new last')

        
    def test_change_password(self):
        # only authenticated user can change password
        self.client.login(username=self.user.username, password='password')
        old_pass = self.user.password
        response = self.client.post('/change_password', content_type="application/json",
                                    data={
                                        'password': '123123',
                                        'password2': '123123'
                                    })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'success': True})
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.password, old_pass)
