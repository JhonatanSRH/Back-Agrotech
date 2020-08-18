"""Users serialiezers."""

#Django REST framework
from rest_framework import serializers

# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator
from django.template.loader import render_to_string

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from apps.users.models import User, Profile

# Utilities
import jwt


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""

        model = Profile
        fields = (
            'picture',
            'biography',
            'posts',
            'comments'
        )
        read_only_fields = (
            'posts',
            'comments'
        )


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  'profile'
                  )


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer."""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="El telefono debe ser un numero entero dentro del rango: +999999999."
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Comprueba que las contraseñas coincidan."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Crea el usuario y el perfil."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=True)
        Profile.objects.create(user=user)
        return user

    def gen_verification_token(user):
        """Create JWT token that the user can use to verify its account."""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()

    def send_confirmation_email(self, user_pk):
        try:
            user = User.objects.get(pk=user_pk)
            verification_token = self.gen_verification_token(user)
            subject = 'Bienvenido @{}! Debes verificar tu cuenta para empezar a usar AgroTech.'.format(user.username)
            from_email = 'AgroTech <noreply@agrotech.com>'
            print(user)
            content = {'token': verification_token, 'user': user}
            """
            content = render_to_string(
                'emails/users/account_verification.html',
                {'token': verification_token, 'user': "pacheco"}
            )"""
            msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
            #msg.attach_alternative(content, "text/html")
            msg.send()
        except Exception as error:
            print(error)


class UserLoginSerializer(serializers.Serializer):
    """User login serializer."""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credenciales invalidas')
        if not user.is_verified:
            raise serializers.ValidationError('La cuenta aún no se ha activado')
        self.context['user'] = user
        return data


    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verifica si el token es valido."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('El link de verificación expiró.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Token invalido')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Token invalido')

        self.context['payload'] = payload
        return data

    def save(self):
        """Verifica el usuario."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
