from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    surname = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$')])

    def __str__(self):
        return f'{self.user.username} Profile'
    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()