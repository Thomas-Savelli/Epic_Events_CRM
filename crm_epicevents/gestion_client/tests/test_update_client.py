from django.core.management import call_command
from django.core.management.base import CommandError
from gestion_client.models import User, Client
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import pytest


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_update_client_successful(mocker, capsys):
    # Créer un collaborateur fictif pour le test
    commercial = User.objects.create(
        nom_complet="Collaborateur Test",
        username="testuser",
        password="testpassword",
        role="commercial"
    )

    client = Client.objects.create(nom_complet="test client", email="testmail@gmail.com",
                                   telephone="0909090909", entreprise="entreprise test",
                                   date_creation="20231210", commercial=commercial)

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='commercial')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=commercial)

    # Capture de la sortie standard pour vérification
    call_command('update_client', str(client.id), '--nom_complet', 'Nouveau Nom')

    # Vérification que le client a été modifié avec succès
    commercial.refresh_from_db()
    captured = capsys.readouterr()
    assert f"Le client avec l'ID {client.id} a été modifié avec succès." in captured.out


@pytest.mark.django_db
def test_update_client_permission_failure(mocker, capsys):
    # Créer un collaborateur fictif pour le test
    collaborateur = User.objects.create(
        nom_complet="Collaborateur Test",
        username="testuser",
        password="testpassword",
        role="support"
    )

    client = Client.objects.create(nom_complet="test client", email="testmail@gmail.com",
                                   telephone="0909090909", entreprise="entreprise test",
                                   date_creation="20231210", commercial=collaborateur)

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='support')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=collaborateur)

        # Capture de la sortie standard pour vérification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Création d'une instance de la commande
            try:
                # Capture de la sortie standard pour vérification
                call_command('update_client', str(client.id), '--nom_complet', 'Nouveau Nom')
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == "Vous n'avez pas la permission d'effectuer cette action."


@pytest.mark.django_db
def test_update_client_not_authenticated(mocker, capsys):
    # Créer un collaborateur fictif pour le test
    collaborateur = User.objects.create(
        nom_complet="Collaborateur Test",
        username="testuser",
        password="testpassword",
        role="gestion"
    )

    client = Client.objects.create(nom_complet="test client", email="testmail@gmail.com",
                                   telephone="0909090909", entreprise="entreprise test",
                                   date_creation="20231210", commercial=collaborateur)

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value=None)

        # Capture de la sortie standard pour vérification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Création d'une instance de la commande
            try:
                # Capture de la sortie standard pour vérification
                call_command('update_client', str(client.id), '--nom_complet', 'Nouveau Nom')
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == "Vous n'avez pas la permission d'effectuer cette action."
