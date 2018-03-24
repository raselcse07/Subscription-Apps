from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db.models.signals import post_save





USERNAME_REGEX="^[a-zA-Z0-9_.]*$"


class MyUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        # Creates and saves a User with the given username,email and password.

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        
        # Creates and saves a User with the given username,email and password.
    

        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):

    username            = models.CharField(

                                        max_length=120,
                                        validators=[RegexValidator(

                                                regex=USERNAME_REGEX,
                                                message="Username must be Alphanumeric or contain any of the follwoing : '_ .'",
                                                code="Invalid Username"
                                            )],
                                        unique=True
                                    )
    email               = models.EmailField(
                                        verbose_name='email address',
                                        max_length=255,
                                        unique=True,
                                    )
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_admin            = models.BooleanField(default=False)
    account_status      = models.BooleanField(default=True)
    is_paymentchecker   = models.BooleanField(default=False)
    is_userchecker      = models.BooleanField(default=False)
    objects             = MyUserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their username
        return self.username

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):

        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

