from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Course
class UserRegistrationLoginTests(APITestCase):

    def test_user_registration(self):
        url = reverse('register')  
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')     
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], "User created successfully.")
        
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
    
    def test_user_registration(self):
        User.objects.create(username='existinguser', password='password123')
        
        url = reverse('register')
        data = {
            'username': 'existinguser',
            'password': 'newpassword'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Username is already taken.")
    
    def test_user_login(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        
        url = reverse('user_login')  
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    
    def test_user_invalid(self):
        url = reverse('user_login')  
        data = {
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid credentials.')


class CourseTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_course(self):
        url = reverse('course-list')  
        data = {
            'title': 'Test Course',
            'description': 'This is a test course.'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Course')
        self.assertEqual(response.data['description'], 'This is a test course.')
    
    def test_course_list(self):
        Course.objects.create(title='Course 1', description='Test course 1')
        Course.objects.create(title='Course 2', description='Test course 2')
        
        url = reverse('course-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_course_update(self):
        course = Course.objects.create(title='Old Course', description='Old description')
        url = reverse('course-update', kwargs={'pk': course.id})
        
        data = {
            'title': 'Updated Course',
            'description': 'Updated description'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Course')
        self.assertEqual(response.data['description'], 'Updated description')
    
    def test_course_delete(self):
        course = Course.objects.create(title='Course to be deleted', description='Description')
        url = reverse('course-delete', kwargs={'pk': course.id})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(id=course.id)
