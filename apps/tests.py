""" Products resolution tests. """
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.models import UserProfile, Country_City, Country, Sale_Statistics
from faker import Faker
import random
User = get_user_model()
fake = Faker()


def generate_password():
    """ this function used for genrate unique sela key"""
    code = ''.join([str(random.randint(0, 999)).zfill(4) for _ in range(2)])
    return code


list_of_product = ['Computers']


class UserModelTest(APITestCase):
    """ Tests the accounts database model. """

    @classmethod
    def setUpTestData(cls):
        """ set up the user table, user details table, for use in multiple tests. """

        _u1 = User.objects.create_user(email='aashish.soni@systematixindia.com', first_name=fake.first_name(),
                                       last_name=fake.last_name(), is_active=True, password='sipl@1234')
        _u2 = User.objects.create_user(email=fake.email(), first_name=fake.first_name(),
                                       last_name=fake.last_name(), is_active=True, password=generate_password())
        country = Country.objects.create(country_name=fake.country)
        country_city = Country_City.objects.create(
            country=country, name=fake.city, Population='320120')
        UserProfile.objects.filter(user_id=_u1.id).update(gender=random.choice(
            ["Male", "Female"]), country=country_city.country.id, city=country_city.id)
        UserProfile.objects.filter(user_id=_u2.id).update(gender=random.choice(
            ["Male", "Female"]), country=country_city.country.id, city=country_city.id)
        Sale_Statistics.objects.create(product=random.choice(list_of_product), date=fake.date(
        ), sales_number=fake.random_digit(), revenue=fake.pyfloat(), user=_u1)

    def test_user_login(self):
        """ Test user login API. """
        data = {"email": "aashish.soni@systematixindia.com",
                "password": 'sipl@1234'}
        response2 = self.client.post("/api/v1/login/", data)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_user_profile_get(self):
        """ This function used for get user profile. """
        token = Token.objects.get(
            user__email="aashish.soni@systematixindia.com")
        test_user = User.objects.get(
            email="aashish.soni@systematixindia.com").id
        response2 = self.client.get(
            "/api/v1/users/" + str(test_user) + "/", HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_user_profile_update(self):
        """ This function used for update user profile. """
        token = Token.objects.get(
            user__email="aashish.soni@systematixindia.com")
        # country=country_city.country.id, city=country_city.id
        data = {
            "email": fake.email,
            "first_name": fake.first_name,
            "last_name": fake.last_name,
            "gender": random.choice(["Male", "Female"]),
            "age": 6,
            "country": 1,
            "city": 1
        }
        test_user = User.objects.get(
            email="aashish.soni@systematixindia.com").id
        response2 = self.client.patch(
            "/api/v1/users/" + str(test_user) + "/", data, HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_countries_get(self):
        """ This function for get countries get. """
        token = Token.objects.get(
            user__email="aashish.soni@systematixindia.com")
        response2 = self.client.get(
            "/api/v1/countries/", HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_sales_data_get(self):
        """ This function for get countries get. """
        token = Token.objects.get(
            user__email="aashish.soni@systematixindia.com")
        response2 = self.client.get(
            "/api/v1/sales/", HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_sales_data_post(self):
        """ This function for post sales data. """
        token = Token.objects.get(
            user__email="aashish.soni@systematixindia.com")
        data = {
            "date": fake.date(),
            "product": 'Bulldog clip',
            "sales_number": fake.random_digit(),
            "revenue": fake.pyfloat(),
            'user_id': User.objects.get(email="aashish.soni@systematixindia.com").id
        }
        response2 = self.client.post(
            "/api/v1/sales/", data, HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_sales_data_put(self):
        """ This function for update sales data. """
        token = Token.objects.get(
            user__email="aashish.soni@systematixindia.com")
        data = {
            "date": fake.date(),
            "product": random.choice(list_of_product),
            "sales_number": fake.random_digit(),
            "revenue": fake.pyfloat()
        }
        test_user = Sale_Statistics.objects.get(
            product=random.choice(list_of_product)).id
        response2 = self.client.put(
            "/api/v1/sales/" + str(test_user) + "/", data, HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_sales_data_patch(self):
        """ This function for update sales data. """
        token = Token.objects.get(
            user__email="aashish.soni@systematixindia.com")
        data = {
            "date": fake.date(),
            "product": random.choice(list_of_product),
            "sales_number": fake.random_digit(),
            "revenue": fake.pyfloat(),
            "user_id": User.objects.get(email="aashish.soni@systematixindia.com").id
        }
        test_user = Sale_Statistics.objects.get(
            product=random.choice(list_of_product)).id
        response2 = self.client.patch(
            "/api/v1/sales/" + str(test_user) + "/", data, HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


    def test_sales_data_delete(self):
        """ This function for update sales data. """
        token = Token.objects.get(
            user__email="aashish.soni@systematixindia.com")

        test_user = Sale_Statistics.objects.get(
            product=random.choice(list_of_product)).id
        response2 = self.client.delete(
            "/api/v1/sales/" + str(test_user) + "/", HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_statistics_average_data(self):
        """ This function used for user statistics average data. """
        token = Token.objects.get(
            user__email="aashish.soni@systematixindia.com")
        response2 = self.client.get(
            "/api/v1/sale_statistics/", HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        """ This function used for user logout. """
        token = Token.objects.get(
            user__email="aashish.soni@systematixindia.com")
        response2 = self.client.post(
            "/api/v1/logout_view/", HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
