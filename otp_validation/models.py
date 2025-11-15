from django.db import models
from work_for_earn.models import Work

class WorkOTP(models.Model):
    work = models.OneToOneField(Work, on_delete=models.CASCADE, null=True, blank=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.work.title}"
