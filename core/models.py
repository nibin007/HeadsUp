from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Likedby(models.Model):
    username = models.CharField(max_length=100)
    def __str__(self):
        return self.username
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images',blank=True,null=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    likedby=models.ManyToManyField(User,related_name='liked_posts')
    comments = models.ManyToManyField(Comment, related_name='post_comments')
    def __str__(self):

        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class DiaryModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=100)
    content = models.TextField()
    posted_date = models.DateTimeField()

    def date_for_chart(self):
        return self.posted_date.strftime('%b %e')

    def __str__(self):
        return self.note

    def summary(self):
        if len(self.content) > 100:
            return self.content[:100] + '  ...'
        return self.content[:100]
    
class ReportModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason=models.TextField()
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.reason
