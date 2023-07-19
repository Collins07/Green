from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_photo = models.ImageField(upload_to='profile_pics/', default='DEFAULT VALUE')
    bio = models.TextField(max_length=300, default="My Bio", blank=True)
    name = models.CharField(blank=True, max_length=120)

    def __str__(self):
        return f'{self.user.username} Profile'


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()
    



class Image(models.Model):
    image = models.ImageField(upload_to='images/',default='DEFAULT VALUE')
    name = models.CharField(max_length=250, blank=True)
    caption = models.CharField(max_length=250, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,  null=True, related_name='posts')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='posts')
    likes = models.IntegerField(default=0)


    class Meta:
       ordering = ['-date_created']


    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()
    

    @classmethod
    def get_image_by_id(cls, image_id):
        images = cls.objects.get(id=image_id)
        return images

class Comment(models.Model):
    comment = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='comments')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user.name} Image'

    class Meta:
        ordering = ["-pk"]    

    def total_likes(self):
        return Image







class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'        
