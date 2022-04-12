# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     is_admin = models.BooleanField('Is admin', default=False)
#     is_customadmin = models.BooleanField('is CustomAdmin', default=False)
#     is_normalmember = models.BooleanField('is NormalMember', default=False)
#     is_advancedmember = models.BooleanField('is advancedMember', default=False)
#     is_active = models.BooleanField(default=False)
#     id = models.BigAutoField(primary_key=True)


# class NormalUser():


import json
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

from devices.models import Device
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save

from asgiref.sync import async_to_sync,sync_to_async
from channels.layers import get_channel_layer


class UserManager(BaseUserManager): 
    def create_user(self, email, full_name, password=None, is_staff=False, is_admin=False, is_normaluser=False, is_advanceduser=False, is_active=True,):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        if not password:
            raise ValueError('Users must have a password')

        if not full_name:
            raise ValueError("User must have a full name")

        user_obj = self.model(            
            email=self.normalize_email(email),
            full_name=full_name,          
        )
        
        
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.normaluser = is_normaluser
        user_obj.advanceduser = is_advanceduser
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_customuser(self, email, full_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            full_name,
            password=password,
        )
        user.staff = True
        user.full_name = full_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  full_name,  password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            full_name,
            password=password,
        )
        user.full_name = full_name
        user.staff = True
        user.admin = True
        user.active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=255,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    normal_user = models.BooleanField(default=False)
    advanced_user = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
 
    # notice the absence of a "Password field", that is built in.
    objects     =   UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their full_name
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email
    
    # def set_avatar(self):
    #     _avatar = self.avatar
    #     if not _avatar:
    #         self.avatar="static/assets/img/avatars/avatar.png"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



    @property
    def is_staff(self):
        "Is the user a custom admin?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


    @property
    def is_normaluser(self):
        "Is the user a admin member?"
        return self.normal_user

    @property
    def is_advanceduser(self):
        "Is the user a admin member?"
        return self.advanced_user

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        """
        return self._generate_jwt_token()

class AllUsers():
    def all_users(self):
        user = get_user_model()
        user.objects.all()

class UserDevices(models.Model):
    user_detail = models.ForeignKey(settings.AUTH_USER_MODEL, default=False, on_delete=models.CASCADE, related_name='user_detail')   
    device_name = models.ForeignKey(Device, default=False,  on_delete=models.CASCADE)
    device_type = models.CharField(max_length=255, blank=True, null=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    # device_images = models.ImageField(upload_to= 'static/assets/img',null=True,blank=True)
    lane1 = models.CharField(max_length=255, blank=True, null=True)
    lane1_status= models.BooleanField(default=False)
    lane2 = models.CharField(max_length=255, blank=True, null=True)
    lane2_status= models.BooleanField(default=False)
    lane3 = models.CharField(max_length=255, blank=True, null=True)
    lane3_status= models.BooleanField(default=False)
    lane4 = models.CharField(max_length=255, blank=True, null=True)
    lane4_status= models.BooleanField(default=False)
    device_status = models.CharField(max_length=255, blank=True, null=True)   
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    lat = models.DecimalField(_('Latitude'), max_digits=10, decimal_places=8, blank=True, null=True)
    lng = models.DecimalField(_('Longitude'), max_digits=11, decimal_places=8, blank=True, null=True)
    pub_date = models.DateTimeField(_('Release date'), auto_now=True)
    class Meta:
        ordering = ['-pub_date']

class UserDetailsFile(models.Model):
    device_images = models.ImageField(upload_to= 'static/assets/img',null=True,blank=True)
    feed = models.ForeignKey(UserDevices, on_delete=models.CASCADE)


class UserProfile(models.Model):
    full_name = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='profile')
    phone_number = models.IntegerField(validators=[MaxValueValidator(12)])
    user_name =  models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.IntegerField(validators=[MaxValueValidator(10)])
    about = models.CharField(max_length=255)
    photo = models.ImageField(upload_to ='static/assets/img', blank=True, null=True)


    def __unicode__(self):
        return '%s' %(self.full_name)

    def create_profile(sender, **kwargs):
        if kwargs["created"]:
            user_profile = UserProfile.objects.create(full_name=kwargs["instance"])
    post_save.connect(create_profile, sender=User)

class NotificationChannel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField()
    sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.id:
        #     self.created_at = timezone.now()
        print('save called')
        channel_layer = get_channel_layer()
        notification_objs =NotificationChannel.objects.all().count()
        data = {'count': notification_objs, 'current_notification': self.message, 'title': self.title}
        async_to_sync(channel_layer.group_send)('notification', {
            'type': 'notification_send',
            'value': json.dumps(data)
        })
        super(NotificationChannel, self).save(*args, **kwargs)
        # return super(NotificationChannel, self).save(*args, **kwargs)
    

    class Meta:
        ordering = ['-created_at']

