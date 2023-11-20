from django.db import models
from datetime import date

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BookClub(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Comment(models.Model):
    bookclub = models.ForeignKey(BookClub, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    pub_date = models.DateField()

    def __str__(self):
        return f"{self.user.name}'s comment on {self.bookclub.name} ({self.pub_date})"
