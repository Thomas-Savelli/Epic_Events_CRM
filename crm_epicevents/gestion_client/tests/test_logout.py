import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_logout_user_connected(mocker):
    # Mock pour simuler un utilisateur connecté
    mocker.patch('gestion_client.auth_utils.load_token', return_value=('test_token', 'expiration_date'))

    # Mock pour simuler la suppression du fichier .token
    mock_remove = mocker.patch('os.remove')

    # Appel de la commande de déconnexion
    call_command('logout')

    # Vérifications
    mock_remove.assert_called_once_with('.token')
