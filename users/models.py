from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.




class CustomUserManager(BaseUserManager):

    #Create user function
    def create_user(self, email, phone, password=None):
        if not email:
            raise ValueError('Email is Required')
        if not phone:
            raise ValueError('Phone number is required')
        if not password:
            raise ValueError('Password is Required')

        user = self.model(
            email = self.normalize_email(email),
            phone = phone,
            password = password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #create supersuser
    def create_superuser(self, email, phone, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            phone = phone,
            password = password
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = PhoneNumberField(unique=True)
    date_joined = models.DateField(_("date_joined"), auto_now=False, auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    

#User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return f'{self.user.email} profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    

    

    