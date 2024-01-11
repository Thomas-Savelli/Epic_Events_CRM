# gestion_client/tests/unit/test_login.py
from gestion_client.management.commands.login import Command
from unittest.mock import patch
from gestion_client.models import User
import pytest


@pytest.fixture
def custom_input():
    return lambda _: "testpassword" if "Mot de passe" in _ else "testuser"


@pytest.mark.django_db
def test_login_command_success(custom_input, capfd):
    # Créezation d'un utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpassword', nom_complet='Test User')

    # Données de sortie attendues pour le test
    expected_output = f'Connexion réussie! Bonjour : {user.nom_complet}'

    # Utilisation de capfd pour capturer la sortie standard
    with patch('builtins.input', side_effect=custom_input), \
         patch('gestion_client.management.commands.login.getpass.getpass', return_value='testpassword'):

        # Création d'une instance de la commande
        cmd = Command()

        # Appel de la fonction handle de la commande
        cmd.handle()

    # Récupération de la sortie capturée
    captured_output = capfd.readouterr().out

    # Vérification que le message attendu est dans la sortie capturée
    assert expected_output in captured_output


@pytest.mark.django_db
def test_login_command_failed(custom_input, capfd):
    # Création d'un utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpassword', nom_complet='Test User')

    # Données de sortie attendues pour le test
    expected_output = "Échec de l'authentification"

    # Utilisation du patch pour simuler l'échec de la fonction d'authentification
    with patch('gestion_client.management.commands.login.authenticate', return_value=None), \
         patch('builtins.input', side_effect=custom_input), \
         patch('gestion_client.management.commands.login.getpass.getpass', return_value='testpassword'):

        # Création de l' instance de la commande
        cmd = Command()

        # Appel de la fonction handle de la commande
        cmd.handle()

    # Récupération de la sortie capturée
    captured_output = capfd.readouterr().out

    # Vérification si le message attendu est dans la sortie capturée
    assert expected_output in captured_output
