from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils.timezone import now

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    available_copies = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=now() + timedelta(days=14))
    returned = models.BooleanField(default=False)

    def calculate_fine(self):
        if self.returned or now() <= self.due_date:
            return 0
        days_overdue = (now() - self.due_date).days
        return days_overdue * 5  
