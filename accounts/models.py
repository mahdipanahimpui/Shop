from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField()
    # is active is overrided
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    # USERNAME_FIELD is point to authentication by what
    USERNAME_FIELD = 'phone_number'
    # REQUIRED_FIELDS is just to use cratesuperuser in command, not other places,
    # phone_number is required because is default auth field,
    # password is required because is implemented in AbstractBaseUer
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.email
    

    def has_perm(self, perm, obj=None):
        # user has perm?
        # we handle perm in other place
        return True

    def has_module_perms(self, app_label):
        # is user has perm to modules?
        return True
    
    @property
    def is_staff(self):
        # is user have access to admin pannel
        return self.is_admin