from functools import wraps
from gestion_client.models import Collaborateur


def gestion_collaborateur_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        collaborateur = request.user
        # Vérifiez le rôle du collaborateur avant de permettre l'action
        if collaborateur.role == 'gestion':
            return func(*args, **kwargs)
        else:
            print("Vous n'avez pas l'autorisation d'effectuer cette action.")
            return None  # Ou retournez une valeur appropriée selon votre logique

    return wrapper


def commercial_collaborateur_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        collaborateur = request.user

        # Vérifiez le rôle du collaborateur avant de permettre l'action
        if collaborateur.role == 'commercial':
            return func(*args, **kwargs)
        else:
            print("Vous n'avez pas l'autorisation d'effectuer cette action.")
            return None  # Ou retournez une valeur appropriée selon votre logique

    return wrapper


def support_collaborateur_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        collaborateur = request.user

        # Vérifiez le rôle du collaborateur avant de permettre l'action
        if collaborateur.role == 'support':
            return func(*args, **kwargs)
        else:
            print("Vous n'avez pas l'autorisation d'effectuer cette action.")
            return None  # Ou retournez une valeur appropriée selon votre logique

    return wrapper
