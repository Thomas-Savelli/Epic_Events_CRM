from gestion_client.auth_utils import validate_token, load_token
from django.core.management.base import CommandError
# from functools import wraps
# from gestion_client.models import User
# from django.core.exceptions import PermissionDenied


def require_login(command_func):
    def wrapper(*args, **kwargs):
        token = load_token()

        if not token:
            raise CommandError("L'utilisateur n'est pas connecté. Veuillez vous connecter.")

        user = validate_token(token)

        if user is None:
            raise CommandError("Token invalide. Veuillez vous connecter.")

        return command_func(*args, **kwargs)

    return wrapper
