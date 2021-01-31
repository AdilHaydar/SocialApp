from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
# Create your models here.

def upload_to(instance,filename):
    return '%s/%s/%s'%('users_avatar',instance.email,filename)

def validate_email(value):
    if not '@' in value:
        raise ValidationError(_('%(value)s is not an invalid mail address'), params={'value':value})

def validate_username(value):
    if len(value) < 3:
        raise ValidationError(_("%(value)s is can't be less than 3 characters."), params={'value':value})


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        
        user.username = username
        user.set_password(password) 
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user
        
    def create_superuser(self, username, password=None, **extra_fields):
        email = input('Email: ')

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
        user.set_password(password)
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length = 15, validators=[validate_username], unique=True)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name = 'Email Address', validators=[validate_email], max_length=255)
    info = models.TextField(null=True, blank = True)
    web_page = models.URLField(null = True, blank = True)
    is_banned = models.BooleanField(default=False, verbose_name = 'Banned')
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True)
    active = models.BooleanField(default = True)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = "User"

            
    @property
    def get_image_or_default(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/media/def_image/default-user-image.png'

    def __str__(self):
        return self.username

    def pathName(self):
        return '/'+self.username+'/'

    def get_short_name(self):
        pass

    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
       return self.admin

    def has_module_perms(self, app_label):
       return self.admin

    def get_likes_list(self):
        return self.likes.values_list('post',flat = True)


class UserUpdateModel(models.Model):
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name = "Email",
    )
    
    birthday = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True)



class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name='followers',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

        ordering = ["-created"]

    def __str__(self):
        return (self.user_id.username+" follow "+self.following_user_id.username)

    #https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
    