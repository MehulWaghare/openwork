# work_for_earn/models.py
from django.db import models
from django.contrib.auth.models import User

class Work(models.Model):
    CATEGORY_CHOICES = [
        ('Physical', 'Physical'),
        ('Online', 'Online'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_works')
    accepted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='accepted_works')
    title = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='work_images/', blank=True, null=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='Physical')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    end_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
