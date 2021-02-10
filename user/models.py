from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Group
# Create your models here.


def upload_to(instance,filename):
    return '%s/%s/%s'%('users_picture',instance.username,filename)

def validate_email(value):
    if not '@' in value:
        raise ValidationError(_('%(value)s is not an invalid mail address'), params={'value':value})

def validate_username(value):
    if len(value) < 3:
        raise ValidationError(_("%(value)s is can't be less than 3 characters."), params={'value':value})


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )

        group = Group.objects.get(name='customer')
        user.group = group
        user.username = username
        user.set_password(password) 
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user
        
    def create_superuser(self, username, password=None, **extra_fields):
        email = input('Email: ')
        name = input('Name: ')
        surname = input('Surname: ')

        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email)
        )
        
        user.username = username
        user.name = name
        user.surname = surname
        user.set_password(password)
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    group = models.ForeignKey(Group, verbose_name='Group', on_delete=models.SET_NULL, null=True, related_name='user')
    username = models.CharField(verbose_name="Username",max_length = 15, validators=[validate_username], unique=True)
    name = models.CharField(verbose_name="name",max_length=20, blank=False, null=False)
    surname = models.CharField(verbose_name="surname",max_length=20, blank=False, null=False)
    picture = models.ImageField(verbose_name="Picture",null=True, blank=True,upload_to=upload_to)
    email = models.EmailField(unique=True, verbose_name = 'Email Address', validators=[validate_email], max_length=255)
    phone = PhoneNumberField(verbose_name="Phone",null=True, blank=True, unique=True)
    gender = models.CharField(verbose_name="Gender",max_length=10, null=True, blank=True, default='')
    active = models.BooleanField(default = True)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = "User"


    def __str__(self):
        return self.username


    def get_full_name(self):
        return self.name+' '+self.surname

    @property
    def is_staff(self):
        return self.staff
    @property
    def is_superuser(self):
        return self.admin
    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        if self.is_superuser and self.is_active:
            return True
        if self.group:
            if perm in self.group.permissions.values_list('codename',flat=True):
                return True
            return False

    def has_module_perms(self, app_label):
       return self.admin


class UserUpdateModel(models.Model):
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name = "Email",
    )


