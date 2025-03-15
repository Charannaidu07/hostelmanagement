from django.db import models
from django.contrib.auth.models import User
from datetime import date
import datetime
class Feature(models.Model):
    CATEGORY_CHOICES = [
        ('G', 'For Girls'),
        ('B', 'For Boys'),
    ]

    title = models.CharField(max_length=255) 
    description = models.TextField() 
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

class HostelStay(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    CITY_CHOICES = [
        ('choose', 'Choose'),
        ('Hyderabad', 'Hyderabad'),
        ('Chennai', 'Chennai'),
    ]
    SHARE_CHOICES = [
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    ]
    TYPE_CHOICES = [
        ('choose', 'Choose'),
        ('ac', 'AC'),
        ('nonac', 'Non AC'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, choices=CITY_CHOICES, default='Choose')
    share = models.CharField(max_length=255, choices=SHARE_CHOICES, default='5')
    hosteltype = models.CharField(max_length=255, choices=TYPE_CHOICES, default='Choose')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    house_address = models.TextField()
    parent_mobile = models.CharField(max_length=15)
    your_mobile = models.CharField(max_length=15)
    guardian_no = models.CharField(max_length=15, blank=True, null=True)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    total_months = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  
    room_number = models.CharField(max_length=10, blank=True, null=True)
    payment_due = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    unique_id = models.CharField(max_length=7, unique=True, blank=True, null=True)
    priority1 = models.CharField(max_length=255)
    priority2 = models.CharField(max_length=255, blank=True, null=True)
    priority3 = models.CharField(max_length=255, blank=True, null=True)
    assigned_hostel = models.CharField(max_length=255, blank=True, null=True)  # Final hostel assigned by admin

    def generate_unique_id(self):
        """Generate a 7-digit unique ID where the first two digits represent the year."""
        year = str(date.today().year)[-2:]  # Get last two digits of the year
        id_number = f"{year}{self.id:05d}"  # Format as 'YYXXXXX'
        return id_number

    def update_due(self):
        """Calculate and update payment due (₹7000 per month) only if approved"""
        if self.status == 'approved' and self.check_in:
            today = date.today()
            months_due = (today.year - self.check_in.year) * 12 + (today.month - self.check_in.month)
            total_due = months_due * 7000

            from .models import PaymentHistory  # Import here to avoid circular import
            total_paid = sum(payment.amount_paid for payment in PaymentHistory.objects.filter(user=self.user, verified=True))

            self.payment_due = max(total_due - total_paid, 0)  # Ensure it's not negative
            self.save()

    def save(self, *args, **kwargs):
        """Auto-generate Unique ID on approval"""
        if self.status == 'approved' and not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.location} ({self.status})"

class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    payment_date = models.DateField(auto_now_add=True)
    payment_proof = models.ImageField(upload_to="payments/")  # User uploads proof
    verified = models.BooleanField(default=False)  # Admin verifies payment
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # If payment is verified, reduce due amount
        if self.verified:
            stay = HostelStay.objects.filter(user=self.user).order_by('-check_in').first()
            if stay:
                stay.update_due()
    def __str__(self):
        return f"{self.user.username} - ₹{self.amount_paid} - {'Verified' if self.verified else 'Pending'}"
class Announcement(models.Model):
    title = models.CharField(max_length=255)  # Mandatory field
    description = models.TextField(blank=True, null=True)  # Optional
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin_message=models.TextField(blank=True,null=True)
    @classmethod
    def delete_old_messages(cls):
        threshold_date = timezone.now() - timezone.timedelta(days=20)
        cls.objects.filter(created_at__lt=threshold_date).delete()
    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"


class Outing(models.Model):
    OUT_CHOICES = [
        ('day', 'Day Outing'),
        ('home', 'Home Outing'),
        ('emergency', 'Emergency'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outtype = models.CharField(max_length=100, choices=OUT_CHOICES, default='day')
    outdate = models.DateField(default=datetime.date.today)
    outtime=models.TimeField(default=timezone.now)
    indate = models.DateField(default=datetime.date.today)
    intime = models.TimeField(default=timezone.now)
    reason = models.TextField(blank=True,null=True)
    approved = models.BooleanField(default=False)  # Admin approval required

    def __str__(self):
        return f"{self.user.username} - {self.outdate} - {'Approved' if self.approved else 'Pending'}"