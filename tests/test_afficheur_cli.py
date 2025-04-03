"""
Modules des tests unitaires pour l'affichage d'informations dans la CLI.
"""

import pytest
from time import sleep
from io import StringIO
from cli.afficheur_cli import AfficheurCLI

# Données
messages = [
    "Un message normal",
    "Test\r avec des \ncaractères\t spéciaux",
    "Test d'un message très long" * 1000,
    "\033[31mTest avec couleur\033[0m",
    "🎉 Test avec des unicodes 🎉"
]

# Tests unitaires

@pytest.mark.parametrize("message", messages)
def test_afficheur_cli_affiche_message(mocker, afficheur_cli, message):
    # Remplacement de la sortie standard par un StringIO (nommé sortie_cli)
    with mocker.patch("sys.stdout", new_callable=StringIO) as sortie_cli:
        afficheur_cli.affiche_message(message)
        assert sortie_cli.getvalue() == afficheur_cli.COULEUR_MESSAGE_NORMAL + message + "\n"

def test_afficheur_cli_exception_affiche_message_type(afficheur_cli):
    with pytest.raises(TypeError):
        afficheur_cli.affiche_message(123)

@pytest.mark.parametrize("message, exception", [
    ("Un message d'erreur !", Exception("Erreur générale !")),
    ("Erreur de typage !", TypeError("Une variable str était attendue !")),
    ("Erreur dans la recherche !", FileNotFoundError("Fichier non trouvé !"))
])
def test_afficheur_cli_affiche_erreur(mocker, afficheur_cli, message, exception):
    # Remplacement de la sortie standard par un StringIO (nommé sortie_cli)
    with mocker.patch("sys.stdout", new_callable=StringIO) as sortie_cli:
        afficheur_cli.affiche_erreur(message, exception)
        assert sortie_cli.getvalue() == (afficheur_cli.COULEUR_MESSAGE_ERREUR + 
                                         message + "\n" + str(exception) + "\n")

@pytest.mark.parametrize("message, exception", [
    (False, Exception("Erreur générale !")),
    ("Erreur de typage !", False)
])  
def test_afficheur_cli_exception_affiche_erreur_type(afficheur_cli, message, exception):
    with pytest.raises(TypeError):
        afficheur_cli.affiche_erreur(message, exception)

@pytest.mark.parametrize("message", messages)
def test_afficheur_cli_reecrire_ligne(mocker, afficheur_cli, message):
    # Remplacement de la sortie standard par un StringIO (nommé sortie_cli)
    with mocker.patch("sys.stdout", new_callable=StringIO) as sortie_cli:
        afficheur_cli.reecrire_ligne(message)
        assert sortie_cli.getvalue() == "\r" + afficheur_cli.COULEUR_MESSAGE_NORMAL + message

def test_afficheur_cli_exception_reecrire_ligne_type(afficheur_cli):
    with pytest.raises(TypeError):
        afficheur_cli.reecrire_ligne(123)

def test_afficheur_cli_lance_animation_chargement(mocker, afficheur_cli):
    mocker.patch.object(afficheur_cli, "_animation_chargement", side_effect=lambda: sleep(10))
    assert afficheur_cli._thread_chargement is None
    afficheur_cli.lance_animation_chargement()
    assert afficheur_cli._thread_chargement is not None
    assert afficheur_cli._thread_chargement.is_alive()

def test_afficheur_cli_stop_animation_chargement_terminee(mocker, afficheur_cli):
    afficheur_cli.lance_animation_chargement()
    afficheur_cli.stop_animation_chargement()
    assert afficheur_cli._thread_chargement is None
    assert afficheur_cli._thread_chargement is None
    assert afficheur_cli._thread_chargement_termine.is_set()

def test_afficheur_cli_stop_animation_chargement_erreur(mocker, afficheur_cli):
    afficheur_cli.lance_animation_chargement()
    afficheur_cli.stop_animation_chargement(True)
    assert afficheur_cli._thread_chargement is None
    assert afficheur_cli._thread_chargement_erreur.is_set()