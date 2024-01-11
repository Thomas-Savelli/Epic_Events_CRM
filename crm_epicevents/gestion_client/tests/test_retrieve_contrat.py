import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from gestion_client.models import User, Contrat, Client
from datetime import datetime, timedelta
from unittest.mock import patch
from io import StringIO
import sys


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_retrieve_contrat_connected_user(mocker):
    # Créer un utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='support')

    commercial_a = User.objects.create_user(username='commerA',
                                            nom_complet='Commercial A', role='commercial')

    commercial_b = User.objects.create_user(username='commerB',
                                            nom_complet='Commercial B', role='commercial')

    client_a = Client.objects.create(nom_complet="CLient A", email="clientA@gmail.com",
                                     telephone="0606060606", entreprise="Entreprise A",
                                     commercial=commercial_a)
    client_b = Client.objects.create(nom_complet="CLient B", email="clientB@gmail.com",
                                     telephone="0707070707", entreprise="Entreprise B",
                                     commercial=commercial_b)

    contrat1 = Contrat.objects.create(client=client_a,
                                      commercial=commercial_a,
                                      montant_total=1000,
                                      montant_restant=500,
                                      statut='attente signature',
                                      date_creation=2023-12-12)

    contrat2 = Contrat.objects.create(client=client_b,
                                      commercial=commercial_b,
                                      montant_total=5000,
                                      montant_restant=2000,
                                      statut='signé',
                                      date_creation=2023-12-23)
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
        mocker.patch('gestion_client.permissions.validate_token', return_value=user)

        expected_output = "Listes des Contrats\n"
        # Rediriger la sortie standard
        original_stdout = StringIO()
        sys.stdout = original_stdout

        # Appel de la fonction handle de la commande avec capture de la sortie
        call_command('retrieve_contrat')

        # Récupération de la sortie standard capturée
        captured_output = original_stdout.getvalue().strip()

        # Rétablir la sortie standard originale
        sys.stdout = sys.__stdout__

        # Vérification de la sortie standard
        assert expected_output.strip() in captured_output.strip()


@pytest.mark.django_db
def test_retrieve_contrat_with_filters(mocker):
    # Créer un utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='commercial')

    # Créer des clients fictifs pour le test
    client_a = Client.objects.create(nom_complet="Client A", email="clientA@gmail.com",
                                     telephone="0606060606", entreprise="Entreprise A",
                                     commercial=user)

    client_b = Client.objects.create(nom_complet="Client B", email="clientB@gmail.com",
                                     telephone="0707070707", entreprise="Entreprise B",
                                     commercial=user)

    # Créer des contrats fictifs pour le test
    contrat1 = Contrat.objects.create(client=client_a,
                                      commercial=user,
                                      montant_total=1000,
                                      montant_restant=500,
                                      statut='attente signature',
                                      date_creation=datetime(2023, 12, 12))

    contrat2 = Contrat.objects.create(client=client_b,
                                      commercial=user,
                                      montant_total=5000,
                                      montant_restant=2000,
                                      statut='signé',
                                      date_creation=datetime(2023, 12, 23))

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
        mocker.patch('gestion_client.permissions.validate_token', return_value=user)

        expected_output1 = "Listes des Contrats\n"
        expected_output2 = "Listes des Contrats\n"

        # Rediriger la sortie standard
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        # Appel de la fonction handle de la commande avec capture de la sortie pour la première recherche
        call_command('retrieve_contrat', '--client', 'Client A')
        # Récupération de la sortie standard capturée
        captured_output1 = sys.stdout.getvalue().strip()

        # Appel de la fonction handle de la commande avec capture de la sortie pour la deuxième recherche
        call_command('retrieve_contrat', '--montant_total', '5000')
        # Récupération de la sortie standard capturée
        captured_output2 = sys.stdout.getvalue().strip()

        # Rétablir la sortie standard originale
        sys.stdout = original_stdout

        # Vérification de la sortie standard pour la première recherche
        assert expected_output1.strip() in captured_output1.strip()
        assert "Client A" in captured_output1

        # Vérification de la sortie standard pour la deuxième recherche
        assert expected_output2.strip() in captured_output2.strip()
        assert "Client B" in captured_output2
        assert "5000" in captured_output2


@pytest.mark.django_db
def test_retrieve_contrat_unauthenticated_user(mocker):
    # Créer un utilisateur fictif qui n'est pas connecté
    user = User.objects.create_user(username='unauthenticated_user', password='testpassword')

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value=None)

        # Mock de la fonction load_token pour retourner un token invalide
        mocker.patch('gestion_client.permissions.load_token', return_value=None)

        expected_output = "L'utilisateur n'est pas connecté. Veuillez vous connecter."

        # Rediriger la sortie standard
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            # Appel de la fonction handle de la commande avec capture de la sortie
            call_command('retrieve_contrat')
        except CommandError as e:
            # Capturer l'erreur et vérifier si elle correspond à ce qui est attendu
            assert str(e) == expected_output
