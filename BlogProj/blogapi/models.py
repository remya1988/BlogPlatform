from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

class Blog(models.Model):
    blog_title=models.CharField(max_length=200)
    content=models.TextField(max_length=500)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="images")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(null=True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(null=True)



