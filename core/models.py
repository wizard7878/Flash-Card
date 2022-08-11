from django.db import models

# Create your models here.

class User(models.Model):
    telegram_user_id = models.IntegerField()
    username = models.CharField(max_length=225)

    def __str__(self) -> str:
        return self.username


class Category(models.Model):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    english = models.CharField(max_length=250)
    persian = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.english