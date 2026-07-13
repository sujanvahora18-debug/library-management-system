from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    total_copies = models.PositiveSmallIntegerField(default=3)
    available_copies = models.PositiveSmallIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        self.total_copies = 3
        if self.available_copies > self.total_copies:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)


class Member(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    joined_at = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class Borrow(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    borrow_date = models.DateField(default=timezone.now)
    due_date = models.DateField(blank=True)
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-borrow_date"]

    def __str__(self):
        return f"{self.member} -> {self.book}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.borrow_date + timedelta(days=7)
        super().save(*args, **kwargs)

    @property
    def is_returned(self):
        return self.return_date is not None

    @property
    def days_late(self):
        if not self.return_date or self.return_date <= self.due_date:
            return 0
        return (self.return_date - self.due_date).days

    @property
    def computed_fine(self):
        return Decimal(self.days_late * 5)


class Fine(models.Model):
    borrow = models.OneToOneField(Borrow, on_delete=models.CASCADE, related_name="fine")
    days_late = models.PositiveIntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Fine ${self.amount} for {self.borrow.member}"

# Create your models here.
