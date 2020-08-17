"""Users models."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Model User"""

    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'Ese email ya fue registrado.'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="El telefono debe ser un numero entero dentro del rango: +999999999."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    created = models.DateTimeField(
        'created at',
        auto_now_add=True
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True
    )

    is_verified = models.BooleanField(
        'verified',
        default=True,
        help_text='Es True cuando el usuario verifica su cuenta'
    )

    def __str__(self):
        return self.username

class Profile(models.Model):
    """Profile model."""

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )
    biography = models.TextField(max_length=500, blank=True)

    # Stats
    posts = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user)
