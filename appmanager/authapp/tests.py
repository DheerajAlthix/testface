from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserProfile, ABHAUser, OTPRequest
from appmanager.doctor.models import HealthCareProvider
from datetime import date

class AuthAppTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client = APIClient()
        
        # Create test doctor
        self.doctor = HealthCareProvider.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Doctor',
            dob='1990-01-01',
            address={'street': '123 Test St', 'city': 'Test City'},
            HPR_ID='TEST123',
            email='doctor@example.com',
            contact_number='1234567890',
            gender='Male',
            service_type='General Medicine'
        )

    def test_welcome_endpoint(self):
        """Test the welcome endpoint"""
        url = reverse('welcome')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)

    def test_login_success(self):
        """Test successful login"""
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_doctor_signup(self):
        """Test doctor signup"""
        url = reverse('doctor-signup')
        data = {
            'username': 'newdoctor',
            'email': 'doctor@example.com',
            'password': 'doctorpass123',
            'first_name': 'New',
            'last_name': 'Doctor',
            'dob': '1990-01-01',
            'address': {'street': '123 Test St', 'city': 'Test City'},
            'hpr_id': 'TEST123',
            'contact_number': '1234567890',
            'gender': 'Male',
            'service_type': 'General Medicine'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)

    def test_patient_signup(self):
        """Test patient signup"""
        url = reverse('patient-signup')
        data = {
            'username': 'newpatient',
            'email': 'patient@example.com',
            'password': 'patientpass123',
            'first_name': 'New',
            'last_name': 'Patient'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)

    def test_user_profile_update(self):
        """Test user profile update"""
        # First login to get token
        login_url = reverse('login')
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['access']
        
        # Set up client with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Update profile
        url = reverse('user_profile_view')
        data = {
            'dob': '1990-01-01',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'zipcode': '123456',
            'adharnumber': '123456789012',
            'abhaid': '123456789012',
            'contactnumber': '1234567890',
            'gender': 'Male'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_google_login(self):
        """Test Google login"""
        url = reverse('google_login')
        data = {
            'token': 'dummy_google_token'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Should fail with invalid token

    def test_abha_user(self):
        """Test ABHA user endpoint"""
        url = reverse('session')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Missing client_id
        
        # Test with client_id
        response = self.client.get(f'{url}?client_id=test_client')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # User not found

    def test_otp_request(self):
        """Test OTP request"""
        url = reverse('verify_phone_user')
        data = {
            'contact': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Invalid request format

    def test_otp_verify(self):
        """Test OTP verification"""
        # First request OTP
        otp_url = reverse('verify_phone_user')
        otp_data = {
            'contact': '1234567890'
        }
        otp_response = self.client.post(otp_url, otp_data, format='json')
        self.assertEqual(otp_response.status_code, status.HTTP_400_BAD_REQUEST)  # Invalid request format
        
        # Verify OTP
        url = reverse('validate_token')
        data = {
            'txn_id': 'dummy_txn_id',
            'otp': '123456'  # Dummy OTP
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Invalid request format

    def test_profile_api(self):
        """Test profile API"""
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Missing clientId
        
        # Test with clientId
        response = self.client.get(f'{url}?clientId=test_client')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Profile not found

    def test_token_refresh(self):
        """Test token refresh"""
        # First login to get refresh token
        login_url = reverse('login')
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # Refresh token
        url = reverse('token_refresh')
        data = {
            'refresh': refresh_token
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
