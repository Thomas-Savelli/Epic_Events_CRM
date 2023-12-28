from functools import wraps
from django.contrib.auth import authenticate


def authenticate_user(request):
    print("Bienvenue dans l'application ! Veuillez vous connecter.")
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    user = authenticate(request, username=username, password=password)

    if user is None:
        print("L'authentification a échoué. Veuillez réessayer.")
        return None

    return user


def gestion_collaborateur_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        collaborateur = request.user

        # Si l'utilisateur n'est pas authentifié, demandez l'authentification
        if not collaborateur.is_authenticated:
            collaborateur = authenticate_user(request)

            # Si l'authentification échoue, interrompez l'exécution de la fonction
            if collaborateur is None:
                return None

        # Vérifiez le rôle du collaborateur avant de permettre l'action
        if collaborateur.role == 'gestion':
            return func(request, *args, **kwargs)
        else:
            print("Vous n'avez pas l'autorisation d'effectuer cette action.")
            return None  # Ou retournez une valeur appropriée selon votre logique

    return wrapper
