import jwt
import json
import os
from datetime import datetime
from gestion_client.models import User
from django.conf import settings


TOKEN_FILE_PATH = ".token"


def load_token():
    try:
        with open(TOKEN_FILE_PATH, 'r') as token_file:
            data = json.load(token_file)
            return data['token'], datetime.utcfromtimestamp(data['expiration_time'])
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None, None


def generate_token(user, expiration_time):
    token = jwt.encode({'user_id': user.id, 'exp': expiration_time},
                       settings.SECRET_KEY, algorithm='HS256')

    # Enregistrement du token dans le fichier
    with open(TOKEN_FILE_PATH, 'w') as token_file:
        token_file.write(json.dumps({
                    'token': token,
                    'expiration_time': expiration_time.timestamp(),
                    'user_id': user.id,
                    'user_role': user.role,
                    'user_name': user.nom_complet,
                }))
    return token


def validate_token(token):
    token, expiration_time = load_token()

    if token and expiration_time and expiration_time > datetime.utcnow():
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            return user
        except jwt.ExpiredSignatureError:
            # Si le token est expiré, supprimer le fichier
            os.remove(TOKEN_FILE_PATH)
            return None
        except jwt.InvalidTokenError:
            return None
        except User.DoesNotExist:
            return None
    return None
