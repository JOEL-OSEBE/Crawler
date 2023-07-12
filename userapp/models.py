# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db import models
import datetime
import jwt


class UserManager(BaseUserManager):
    """
    Override the `create_user` function which we will use
    to create `User` objects.
    """
    def create_user(self, username, first_name, last_name,  email, date_of_birth, country,
                    password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')
        if first_name is None:
            raise TypeError('Users must have an first name.')
        if last_name is None:
            raise TypeError('Users must have an last name.')
        if date_of_birth is None:
            raise TypeError('Users must include their date of birth.')
        if country is None:
            raise TypeError('Users must have an country name.')

        date_of_birth = str(date_of_birth)
        user = self.model(username=username, email=self.normalize_email(email),
                          first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
                          country=country)

        user.set_password(password)
        user.save()

        return user

    def create_admin(self, username, email, country, staff_no, password=None):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.model(
            email=email, password=password, username=username, is_admin=True,
            country=country, staff_no=staff_no
        )
        user.set_password(password)
        user.save()

        return user

    def create_superadmin(self, username, email, country, staff_no, password=None):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.model(
            email=email, password=password,
            username=username, country=country, staff_no=staff_no, is_admin=True,
            is_superadmin=True
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.model(
            email=email, password=password,
            username=username, is_admin=True,
            is_superuser=True, is_superadmin=True
        )
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.

    # Other fields
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(db_index=True, unique=True)
    date_of_birth = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    staff_no = models.CharField(max_length=200, null=True)
    
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    deactivate_at = models.DateTimeField(auto_now_add=True)
    activate_at = models.DateTimeField(auto_now_add=True)
    last_logout = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    login_status = models.CharField(max_length=200)
    login_frequency = models.IntegerField(default=0)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.username

    #get user token
    @property
    def token(self):
        
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 5 days into the future.
        """
        date_time = datetime.datetime.now() + datetime.timedelta(days=5)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(date_time.strftime('%s')),
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'email': self.email,
            'login_frequency': self.login_frequency

        }, settings.SECRET_KEY, algorithm='HS256')

        token = token.encode()
        return token.decode('utf-8')

class CrawlerModel(models.Model):
    title = models.CharField(max_length=200, unique=True)
    source = models.CharField(max_length=200)
    text = models.TextField()
    tokens = models.IntegerField()
    date = models.CharField(max_length=200)
    url = models.CharField(max_length=200, unique=True)