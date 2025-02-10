# myapp/backends.py
from django.contrib.auth.backends import BaseBackend
from p1.models import WeddingGuest

class WeddingGuestAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Retrieve the WeddingGuest object by first_name (username) and last_name (password)
            guest = WeddingGuest.objects.get(first_name=username)

            # Here you can implement your custom password check
            if guest.last_name == password:  # Simple plain-text password check (use hashed passwords in production)
                return guest  # Returning the WeddingGuest object itself as the authenticated user
        except WeddingGuest.DoesNotExist:
            return None  # Return None if the user is not found

    def get_user(self, user_id):
        try:
            return WeddingGuest.objects.get(id=user_id)
        except WeddingGuest.DoesNotExist:
            return None
