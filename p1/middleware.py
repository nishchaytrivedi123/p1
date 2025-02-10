# middleware.py
from p1.models import WeddingGuest
import time
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('guest_id')
        if user_id:
            try:
                guest = WeddingGuest.objects.get(id=user_id)
                request.user = guest
            except WeddingGuest.DoesNotExist:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        response = self.get_response(request)
        return response

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the last activity timestamp from the session
        last_activity = request.session.get('last_activity')

        # Check if the session has expired based on 30 minutes of inactivity
        if last_activity and (time.time() - last_activity > settings.SESSION_COOKIE_AGE):
            logout(request)  # Log the user out if the session has expired
            return redirect('login')  # Redirect to the login page after logout

        # Update the last activity timestamp
        request.session['last_login'] = time.time()

        # Process the request and return the response
        response = self.get_response(request)
        return response
