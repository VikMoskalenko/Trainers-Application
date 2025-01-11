from email.headerregistry import Group

from django.contrib.auth.models import User
from django.test import TestCase, Client

from trainer.models import Service, Category


# Create your tests here.
class TrainerTest(TestCase):
    fixtures = ['fixture1.json']

    # and also you can reuse category model from this json file from db
    def show_all_trainers(self):
        client = Client()
        response = client.get('/trainer/')
        self.assertEqual(response.status_code, 200)

    def test_all_services(self ):
        client = Client()
        response = client.get('/service/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/service/?trainer_id=1/')
        self.assertEqual(response.status_code, 200)

    def test_trainer_add_service(self):
        #anonumys user
        client = Client()
        response = client.get('/service/',{'name': 1, 'category': 1,  'price': 1, 'duration': 30, 'level': 1})
        self.assertEqual(response.status_code, 403)

        #client
        Group.objects.create(name='client')
        user = User.objects.create_user(
            username='tester',
            password='1111',
            first_name='tester',
            last_name='tester',
            email='user1@example.com',)
        user.groups.add(Group.objects.get(name='client'))
        user.save()
        client.login(username='tester', password='1111')
        response = client.get('/service/', {'name': 1, 'category': 1, 'price': 1, 'duration': 30, 'level': 1})
        self.assertEqual(response.status_code, 403)

        #trainer
        Group.objects.create(name='trainer')
        user = User.objects.create_user(
            username='trainer',
            password='1111',
            first_name='tester',
            last_name='tester',
            email='user2@example.com', )
        user.groups.add(Group.objects.get(name='trainer'))
        user.save()

        categor = Category.objects.create(name='cat')
        categor.save()

        client.login(username='trainer', password='1111')
        response = client.get('/service/', {'name': 1, 'category': categor.id, 'price': 1, 'duration': 30, 'level': 1})

        self.assertEqual(response.status_code, 200)

        created_service = Service.objects.get(name='1').first()
        self.assertEqual(created_service.trainer.username, 'trainer')
        self.assertEqual(created_service.trainer.price, '100')




