from django.core.management import call_command
from django.core.management.base import CommandError
from gestion_client.models import User, Contrat, Client, Evenement
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import pytest


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_update_evenement_successful(mocker, capsys):
    # Créer un collaborateur fictif pour le test
    collaborateur = User.objects.create(
        nom_complet="Collaborateur Test",
        username="testuser",
        password="testpassword",
        role="gestion"
    )

    # Créer un client fictif pour le test
    client = Client.objects.create(nom_complet='Client Test', email='test@example.com')

    # Créer un commercial fictif pour le test
    commercial = User.objects.create_user(username='testcommercial',
                                          password='testpassword', nom_complet='Test Commercial', role='commercial')

    # Créer un contrat fictif pour le test
    contrat = Contrat.objects.create(client=client, commercial=commercial, montant_total='1000.00',
                                     montant_restant='800.00', statut='En cours')

    # Créer un support fictif pour le test
    support_user = User.objects.create(username='testsupport', role='support')

    evenement = Evenement.objects.create(contrat=contrat, nom='Test Evenement', date_debut='20220101',
                                         date_fin='20220105', support=support_user,
                                         lieu='Lieu test', nombre_participants=50, notes='Notes test')

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
    call_command('update_evenement', str(evenement.id), '--nom', 'Nouveau Nom evenement')

    # Vérification que le collaborateur a été modifié avec succès
    collaborateur.refresh_from_db()
    captured = capsys.readouterr()
    assert f"Événement avec l'ID {evenement.id} mis à jour avec succès." in captured.out


@pytest.mark.django_db
def test_update_evenement_permission_failure(mocker, capsys):
    # Créer un collaborateur fictif pour le test
    collaborateur = User.objects.create(
        nom_complet="Collaborateur Test",
        username="testuser",
        password="testpassword",
        role="commercial"
    )

    # Créer un client fictif pour le test
    client = Client.objects.create(nom_complet='Client Test', email='test@example.com')

    # Créer un commercial fictif pour le test
    commercial = User.objects.create_user(username='testcommercial',
                                          password='testpassword', nom_complet='Test Commercial', role='commercial')

    # Créer un contrat fictif pour le test
    contrat = Contrat.objects.create(client=client, commercial=commercial, montant_total='1000.00',
                                     montant_restant='800.00', statut='En cours')

    # Créer un support fictif pour le test
    support_user = User.objects.create(username='testsupport', role='support')

    evenement = Evenement.objects.create(contrat=contrat, nom='Test Evenement', date_debut='20220101',
                                         date_fin='20220105', support=support_user,
                                         lieu='Lieu test', nombre_participants=50, notes='Notes test')


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
        mocker.patch('gestion_client.permissions.validate_token', return_value=collaborateur)

        # Capture de la sortie standard pour vérification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Création d'une instance de la commande
            try:
                # Capture de la sortie standard pour vérification
                call_command('update_evenement', str(evenement.id), '--nom', 'Nouveau Nom')
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == "Vous n'avez pas la permission d'effectuer cette action."


@pytest.mark.django_db
def test_update_evenement_not_found(mocker, capsys):
    # Créer un utilisateur fictif pour le test (rôle: 'gestion')
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='gestion')

    # ID d'un evenement qui n'existe pas
    evenement_id = 999

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
        mocker.patch('gestion_client.permissions.validate_token', return_value=user)

        # Capture de la sortie d'erreur standard pour vérification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Tentative de mise à jour d'un collaborateur qui n'existe pas
            try:
                call_command('update_evenement', str(evenement_id), '--nom', 'Nouveau evenement')
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == f"L'événement avec l'ID {evenement_id} n'existe pas."
