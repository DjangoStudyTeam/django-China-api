from django.dispatch import Signal

# New user has registered. Args: user, request.
user_registered = Signal()
