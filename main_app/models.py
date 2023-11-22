from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

def get_default_user_id():
    # Your logic to determine the default user ID goes here
    # For example, you can get the ID of the first user in the database
    return User.objects.first().id

class BookClub(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    members = models.ManyToManyField(User)
    discussion = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, 
        related_name='created_bookclubs'
        )
    def __str__(self):
        return self.name

class Comment(models.Model):
    bookclub = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s comment on {self.bookclub.name} ({self.pub_date})"
