from django.core.management import call_command
from django.core.management.base import CommandError
from gestion_client.models import User, Client, Contrat
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import pytest


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_update_contrat_successful(mocker, capsys):
    # Créer un collaborateur fictif pour le test
    collaborateur = User.objects.create(
        nom_complet="Collaborateur Test",
        username="testuser",
        password="testpassword",
        role="gestion"
    )

    commercial = User.objects.create_user(username='comtest',
                                          nom_complet='Commercial Test', role='commercial')

    client = Client.objects.create(nom_complet="CLient A", email="clientA@gmail.com",
                                   telephone="0606060606", entreprise="Entreprise A",
                                   commercial=commercial)

    contrat = Contrat.objects.create(client=client,
                                     commercial=commercial,
                                     montant_total=1000,
                                     montant_restant=500,
                                     statut='attente signature',
                                     date_creation=2023-12-12)

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='gestion')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=collaborateur)

    # Capture de la sortie standard pour vérification
    call_command('update_contrat', str(contrat.id), '--statut', 'signé')

    # Vérification que le contrat a été modifié avec succès
    collaborateur.refresh_from_db()
    captured = capsys.readouterr()
    assert f"Contrat avec l'ID {contrat.id} mis à jour avec succès." in captured.out


@pytest.mark.django_db
def test_update_collaborateur_permission_failure(mocker, capsys):
    # Créer un collaborateur fictif pour le test
    collaborateur = User.objects.create(
        nom_complet="Collaborateur Test",
        username="testuser",
        password="testpassword",
        role="support"
    )

    commercial = User.objects.create_user(username='comtest',
                                          nom_complet='Commercial Test', role='commercial')

    client = Client.objects.create(nom_complet="CLient A", email="clientA@gmail.com",
                                   telephone="0606060606", entreprise="Entreprise A",
                                   commercial=commercial)

    contrat = Contrat.objects.create(client=client,
                                     commercial=commercial,
                                     montant_total=1000,
                                     montant_restant=500,
                                     statut='attente signature',
                                     date_creation=2023-12-12)

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
                call_command('update_contrat', str(contrat.id), '--statut', 'signé')
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == "Vous n'avez pas la permission d'effectuer cette action."


@pytest.mark.django_db
def test_update_contrat_not_found(mocker, capsys):
    # Créer un collaborateur fictif pour le test
    collaborateur = User.objects.create(
        nom_complet="Collaborateur Test",
        username="testuser",
        password="testpassword",
        role="gestion"
    )

    commercial = User.objects.create_user(username='comtest',
                                          nom_complet='Commercial Test', role='commercial')

    client = Client.objects.create(nom_complet="CLient A", email="clientA@gmail.com",
                                   telephone="0606060606", entreprise="Entreprise A",
                                   commercial=commercial)

    contrat = Contrat.objects.create(client=client,
                                     commercial=commercial,
                                     montant_total=1000,
                                     montant_restant=500,
                                     statut='attente signature',
                                     date_creation=2023-12-12)

    # ID d'un collaborateur qui n'existe pas
    user_id = 999

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='gestion')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=collaborateur)

        # Capture de la sortie d'erreur standard pour vérification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Tentative de mise à jour d'un collaborateur qui n'existe pas
            try:
                call_command('update_contrat', str(user_id), '--statut', 'signé')
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == f"Collaborateur avec l'ID {user_id} non trouvé"


@pytest.mark.django_db
def test_update_contrat_not_authenticated(mocker, capsys):
    # Créer un collaborateur fictif pour le test
    collaborateur = User.objects.create(
        nom_complet="Collaborateur Test",
        username="testuser",
        password="testpassword",
        role="gestion"
    )

    commercial = User.objects.create_user(username='comtest',
                                          nom_complet='Commercial Test', role='commercial')

    client = Client.objects.create(nom_complet="CLient A", email="clientA@gmail.com",
                                   telephone="0606060606", entreprise="Entreprise A",
                                   commercial=commercial)

    contrat = Contrat.objects.create(client=client,
                                     commercial=commercial,
                                     montant_total=1000,
                                     montant_restant=500,
                                     statut='attente signature',
                                     date_creation=2023-12-12)

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='gestion')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=None)

        # Capture de la sortie standard pour vérification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Création d'une instance de la commande
            try:
                # Capture de la sortie standard pour vérification
                call_command('update_contrat', str(contrat.id), '--statut', 'signé')
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == "Token invalide. Veuillez vous connecter."
