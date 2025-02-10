from django.db import models
from django.utils import timezone

class Family(models.Model):
    family_name = models.CharField(max_length=255)
    number_of_guests = models.PositiveIntegerField(default=1)  # Number of additional guests they are bringing
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.family_name

class WeddingGuest(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='guests')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rsvp_status = models.BooleanField(default=False)  # True means attending, False means not attending
    dietary_restrictions = models.TextField(blank=True, null=True)  # Optional, can be left blank
    email = models.EmailField(unique=True, blank=True, null=True)  # Email address, must be unique
    created_at = models.DateTimeField(auto_now_add=True)  # When the record was created
    updated_at = models.DateTimeField(auto_now=True)  # When the record was last updated
    last_login = models.DateTimeField(default=timezone.now)
    message = models.CharField(max_length=250,  blank=True, null=True)
    is_rsvped = models.BooleanField(default=False) # True means they have already made their decisions
    staying_at_hotel = models.BooleanField(default=False) # True means staying at hotel

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_authenticated(self):
        # This is a simplified version. You can customize it as per your needs.
        # Assuming that if the guest exists and is active, they're authenticated.
        return self.pk is not None