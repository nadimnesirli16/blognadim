from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=20)
    slug = models.SlugField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    views_count=models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     content = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     active=models.BooleanField(default=True)
     
     def __str__(self):
        return self.title
     
class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes" )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')




