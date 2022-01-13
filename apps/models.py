from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Country(models.Model):
    country_name = models.CharField(max_length=120, null=False, blank=False)


class Country_City(models.Model):
    country = models.ForeignKey(Country, related_name='city_details', on_delete=models.CASCADE)
    City = models.CharField(max_length=120, blank=False, null=False)
    Population = models.CharField(max_length=120, null=True, blank=True)



class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    gender = models.CharField(max_length=200, blank=True, null=True)
    age = models.CharField(max_length=500, blank=True, null=True)
    country = models.ForeignKey(Country, related_name='country', on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(Country_City, related_name='country_city', on_delete=models.SET_NULL, blank=True, null=True)


class Sale_Statistics(models.Model):
    user = models.ForeignKey(User, related_name='User_data', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    product = models.CharField(max_length=120, null=False, blank=False)
    sales_number = models.IntegerField()
    revenue = models.FloatField()


@receiver(post_save, sender=User)
def create_auth_token(instance=None, created=False, **kwargs):
    """ create user token """
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    """ creating user profile instance of user """
    if created:
        UserProfile.objects.create(user=instance)
