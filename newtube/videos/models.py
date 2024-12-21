from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MinLengthValidator

# Create your models here.



class Video(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])])
    preview = models.ImageField(upload_to='preview')
    likes = models.ManyToManyField('User', blank=True, related_name='like')
    dislikes = models.ManyToManyField('User', blank=True, related_name='dislike')
    views = models.PositiveIntegerField(default=0)
    tags = models.ForeignKey('Tags', on_delete=models.SET_DEFAULT, default='', related_name='cats')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='profile')

    def number_of_likes(self):
        return self.likes.count()
    
    def number_of_dislikes(self):
        return self.dislikes.count()


    def __str__(self):
        return self.title

class Tags(models.Model):
    title = models.CharField(unique=True)

    def __str__(self):
        return self.title

class User(AbstractUser):
    name_channel = models.CharField(unique=True)
    channel_description = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='user/avatar/')
    subscribers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='subscriptions')

    def number_of_subscribers(self):
        return self.subscribers.count()

    def __str__(self):
        return self.username

class Comment(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    text = models.TextField(blank=False)

    def __str__(self):
        return self.text