from email.headerregistry import Group
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.test import TestCase, Client
import booking
from trainer.models import Services, Category, Trainer_description, Trainer_Schedule
from booking.models import Booking
from django.utils.dateparse import parse_datetime
import datetime
from django.urls import reverse
# Create your tests here.
class TrainerTest(TestCase):
    fixtures = ['fixture1.json']

class TrainerPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.create(name='Trainer')
        self.trainer_user = User.objects.create_user(username='trainer', password='password')
        trainer_group = Group.objects.get(name='Trainer')
        self.trainer_user.groups.add(trainer_group)
        self.regular_user = User.objects.create_user(username='user', password='password')
        self.category = Category.objects.create(name='Fitness')
        self.service = Services.objects.create(
            level='1',
            duration=60,
            price=50,
            category=self.category,
            trainer=self.trainer_user
        )
        self.trainer_description = Trainer_description.objects.create(trainer=self.trainer_user, text="Trainer")

        self.trainer_schedule = Trainer_Schedule.objects.create(
            trainer=self.trainer_user,
            datetime_start=datetime.datetime.now(),
            datetime_end=datetime.datetime.now() + datetime.timedelta(hours=1)
        )

    def test_trainer_page_as_trainer(self):
        self.client.login(username='trainer', password='password')
        response = self.client.get(reverse('trainer_page', args=[self.trainer_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainer.html')
        self.assertIn('categories', response.context)
        self.assertIn('services', response.context)

    def test_trainer_page_as_regular_user(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('trainer_page', args=[self.trainer_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')
        self.assertIn('trainer_data', response.context)
        self.assertIn('trainer_schedule', response.context)


class TrainerRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.create(name="Trainer")

    def test_trainer_registration_get(self):
            response = self.client.get(reverse('trainer_registration'))
            self.assertEqual(response.status_code, 200, 302)
            self.assertTemplateUsed(response, 'trainer_signup.html')

    def test_trainer_registration_post(self):
            response = self.client.post(reverse('trainer_registration'), {
                'username': 'new_trainer',
                'password1': 'password',
                'password2': 'password',
                'email': 'trainer@example.com'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue(User.objects.filter(username='new_trainer').exists())



class TrainerServiceTest(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.create(name='Trainer')
        self.trainer_user = User.objects.create_user(username='trainer', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')
        trainer_group = Group.objects.get(name='Trainer')
        self.trainer_user.groups.add(trainer_group)
        self.category = Category.objects.create(name='Fitness')
        self.service = Services.objects.create(
            level='1',
            duration=60,
            price=50,
            category=self.category,
            trainer=self.trainer_user
        )
        self.trainer_schedule = Trainer_Schedule.objects.create(
            trainer=self.trainer_user,
            datetime_start=datetime.datetime.now(),
            datetime_end=datetime.datetime.now() + datetime.timedelta(hours=1)
        )

    def test_trainer_service_get(self):
        self.client.login(username='trainer', password='password')
        url = reverse('trainer_service', args=[self.trainer_user.id, self.service.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainer_service_page.html')
        self.assertIn('specific_service', response.context)
        self.assertIn('available_times', response.context)

    def test_trainer_service_post(self):
        self.client.login(username='user', password='password')
        url = reverse('trainer_service', args=[self.trainer_user.id, self.service.id])
        booking_start = datetime.datetime.now() + datetime.timedelta(days=1)
        booking_start_str = booking_start.strftime('%Y-%m-%dT%H:%M:%S')

        response = self.client.post(url, {
            'booking_start': booking_start_str
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            booking.models.Booking.objects.filter(
                trainer=self.trainer_user,
                user=self.regular_user,
                service=self.service,
                datetime_start=parse_datetime(booking_start_str)
            ).exists()
        )

    def test_service_page_get(self):
        url = reverse('service_page')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainer_service_page.html')
        self.assertIn('services', response.context)
        self.assertEqual(len(response.context['services']), 1)

    def test_service_page_post(self):
        self.client.login(username='trainer', password='password')
        url = reverse('service_page')
        form_data = {
            'level': '2',
            'duration': 90,
            'price': 100,
            'category': self.category.id
        }
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Services.objects.filter(level='2', duration=90, price=100).exists())




