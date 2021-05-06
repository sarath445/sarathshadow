
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserAccounts(AbstractUser):
    phone=models.IntegerField(null=True)

class Blogs(models.Model):
    user=models.ForeignKey(UserAccounts,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='media/blog_img/',default="media/blog_img/img.jpg")
    title=models.CharField(max_length=100)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    user=models.ForeignKey(UserAccounts,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Headline(models.Model):
  title = models.CharField(max_length=200)
  image = models.URLField(null=True, blank=True)
  url = models.TextField()
  def __str__(self):
    return self.title

class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "cities"    

