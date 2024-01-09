from gestion_client.models import Client, Contrat, Evenement
from gestion_client.auth_utils import validate_token, load_token
from django.core.management.base import CommandError
from functools import wraps
import json


def require_login(command_func):
    # Permission qui s'assure que le collaborateur est bien connecté
    def wrapper(*args, **kwargs):
        token = load_token()

        if not token:
            raise CommandError("L'utilisateur n'est pas connecté. Veuillez vous connecter.")

        user = validate_token(token)

        if user is None:
            raise CommandError("Token invalide. Veuillez vous connecter.")

        return command_func(*args, **kwargs)

    return wrapper


def get_user_role_from_token():
    # Récupérer aprés connexion dans .token le role de l'utilisateur connecté
    try:
        with open('.token', 'r') as token_file:
            data = json.load(token_file)
            return data.get('user_role', '')
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return ''


def get_user_id_from_token():
    # Récupérer aprés connexion dans .token l'id du collaborateur connecté
    try:
        with open('.token', 'r') as token_file:
            data = json.load(token_file)
            return data.get('user_id', '')
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return ''


def require_team_commercial(view_func):
    # Permissions qui s'assure que le collaborateur fait bien parti de la team commercial
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_role = get_user_role_from_token()
        if user_role != "commercial":
            raise CommandError("Vous n'avez pas la permission d'effectuer cette action.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def require_team_commercial_and_client_access(view_func):
    # Permissions qui s'assure que le collaborateur fait bien parti de la team commercial et est associé au client
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Vérifie le rôle de l'utilisateur
        user_role = get_user_role_from_token()
        if user_role != "commercial":
            raise CommandError("Vous n'avez pas la permission d'effectuer cette action.")

        # Vérifie si l'utilisateur est associé au client
        user_id = get_user_id_from_token()
        client_id = kwargs.get('client_id')  # s'assure d'avoir l'ID du client dans les paramètres de la vue

        try:
            client = Client.objects.get(id=client_id, commercial_id=user_id)
        except Client.DoesNotExist:
            raise CommandError("Accés refusé. Vous n'êtes pas le Commercial assigné à ce client.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def require_commercial_contrat_access_or_team_gestion(view_func):
    """Permission qui s'assure que l'utilisateur est un commercial
    qui est lié au client du contrat ou un membre de l'equipe gestion"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Vérifie le rôle de l'utilisateur
        user_role = get_user_role_from_token()
        user_id = get_user_id_from_token()

        if user_role == "commercial":
            # Si l'utilisateur est un commercial, vérifie s'il est lié au client du contrat
            contrat_id = kwargs['contrat_id']

            try:
                contrat = Contrat.objects.get(id=contrat_id, commercial_id=user_id)
            except Contrat.DoesNotExist:
                raise CommandError("Accès refusé. Vous n'êtes pas le Commercial assigné à ce contrat.")
        elif user_role == "gestion":
            # Si l'utilisateur fait partie de l'équipe gestion, autorise l'accès
            pass
        else:
            raise CommandError("Vous n'avez pas la permission d'effectuer cette action.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def require_commercial_event_access(views_func):
    # Permission qui s'assure que le commerciale soit bien lié au client du contrat
    @wraps(views_func)
    def _wrapped_view(request, *args, **kwargs):
        # Vérifie le rôle de l'utilisateur
        user_role = get_user_role_from_token()
        if user_role != "commercial":
            raise CommandError("Vous n'avez pas la permission d'effectuer cette action.")
        # Vérifie si l'utilisateur est associé au client de l'evenement
        user_id = get_user_id_from_token()
        contrat_id = kwargs.get('contrat_id')

        try:
            contrat = Contrat.objects.get(id=contrat_id, commercial_id=user_id)
        except Contrat.DoesNotExist:
            raise CommandError("Accès refusé. Vous n'êtes pas le Commercial assigné à cet événement.")

        return views_func(request, *args, **kwargs)

    return _wrapped_view


def require_team_gestion(view_func):
    # Permissions qui s'assure que le collaborateur fait bien parti de la team commercial
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_role = get_user_role_from_token()
        if user_role != "gestion":
            raise CommandError("Vous n'avez pas la permission d'effectuer cette action.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def require_support_event_access_or_team_gestion(view_func):
    """Permission qui s'assure que l'utilisateur est un support
    qui est lié à l'évenement ou un membre de l'equipe gestion"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_role = get_user_role_from_token()

        if user_role == "support":
            user_id = get_user_id_from_token()
            evenement_id = kwargs['evenement_id']

            try:
                evenement = Evenement.objects.get(id=evenement_id, support_id=user_id)
            except Evenement.DoesNotExist:
                raise CommandError("Accès refusé. Vous n'êtes pas le Collaborateur Support assigné à cet événement.")

        elif user_role == "gestion":
            # Accés authorisé pour l'équipe gestion
            pass

        else:
            raise CommandError("Vous n'avez pas la permission d'effectuer cette action.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
