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
    """
    Vérifie que la méthode affiche_message affiche correctement les messages avec la bonne
    couleur dans le terminal.

    Scénarios testés:
        - Passage d'un message à la méthode.

    Asserts:
        - Le message est le même que celui fourni avec la bonne couleur.

    Args:
        mocker (MockerFixture): Fixture qui permet de modifier le stdout.
        afficheur_cli (AfficheurCLI): Fixture pour l'instance de la classe ``AfficheurCLI``.
        message (str): Message à afficher.
    """
    # Remplacement de la sortie standard par un StringIO (nommé sortie_cli)
    with mocker.patch("sys.stdout", new_callable=StringIO) as sortie_cli:
        afficheur_cli.affiche_message(message)
        assert sortie_cli.getvalue() == afficheur_cli.COULEUR_MESSAGE_NORMAL + message + "\n"

def test_afficheur_cli_exception_affiche_message_type(afficheur_cli):
    """
    Vérifie que la méthode affiche_message lève une exception TypeError
    lorsque l'argument fourni n'est pas une chaîne de caractères.

    Scénarios testés:
        - Passage d'un entier à la méthode.

    Asserts:
        - Vérifie que l'exception TypeError est levée.

    Args:
        afficheur_cli (AfficheurCLI): Fixture pour l'instance de la classe ``AfficheurCLI``.
    """
    with pytest.raises(TypeError):
        afficheur_cli.affiche_message(123)

@pytest.mark.parametrize("message, exception", [
    ("Un message d'erreur !", Exception("Erreur générale !")),
    ("Erreur de typage !", TypeError("Une variable str était attendue !")),
    ("Erreur dans la recherche !", FileNotFoundError("Fichier non trouvé !"))
])
def test_afficheur_cli_affiche_erreur(mocker, afficheur_cli, message, exception):
    """
    Vérifie que la méthode affiche_erreur affiche correctement les messages d'erreur
    dans le terminal avec la couleur adéquate.

    Scénarios testés:
        - Affichage d'erreurs avec différents types d'exceptions.

    Asserts:
        - Vérifie que le message d'erreur et l'exception sont bien affichés.

    Args:
        mocker (MockerFixture): Fixture pour modifier le stdout.
        afficheur_cli (AfficheurCLI): Fixture pour l'instance de la classe ``AfficheurCLI``.
        message (str): Message d'erreur à afficher.
        exception (Exception): Exception associée à l'erreur.
    """
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
    """
    Vérifie que la méthode affiche_erreur lève une exception TypeError
    lorsque les arguments ne sont pas du bon type.

    Scénarios testés:
        - Passage d'un mauvais type pour le paramètre ``message``.
        - Passage d'un mauvais type pour le paramètre ``exception``.

    Asserts:
        - Vérifie que l'exception TypeError est levée.

    Args:
        afficheur_cli (AfficheurCLI): Fixture pour l'instance de la classe ``AfficheurCLI``.
        message (Any): Valeur incorrecte à tester.
        exception (Any): Valeur incorrecte à tester.
    """
    with pytest.raises(TypeError):
        afficheur_cli.affiche_erreur(message, exception)

@pytest.mark.parametrize("message", messages)
def test_afficheur_cli_reecrire_ligne(mocker, afficheur_cli, message):
    """
    Vérifie que la méthode reecrire_ligne affiche correctement un message
    sur la même ligne du terminal.

    Scénarios testés:
        - Affichage de plusieurs messages.

    Asserts:
        - Vérifie que la sortie standard contient le message formaté.

    Args:
        mocker (MockerFixture): Fixture pour modifier le stdout.
        afficheur_cli (AfficheurCLI): Fixture pour l'instance de la classe ``AfficheurCLI``.
        message (str): Message à afficher.
    """
    # Remplacement de la sortie standard par un StringIO (nommé sortie_cli)
    with mocker.patch("sys.stdout", new_callable=StringIO) as sortie_cli:
        afficheur_cli.reecrire_ligne(message)
        assert sortie_cli.getvalue() == "\r" + afficheur_cli.COULEUR_MESSAGE_NORMAL + message

def test_afficheur_cli_exception_reecrire_ligne_type(afficheur_cli):
    """
    Vérifie que la méthode reecrire_ligne lève une exception TypeError
    lorsqu'un argument de type incorrect est fourni.

    Scénarios testés:
        - Passage d'un entier au lieu d'une chaîne de caractères.

    Asserts:
        - Vérifie que l'exception TypeError est levée.

    Args:
        afficheur_cli (AfficheurCLI): Fixture pour l'instance de la classe ``AfficheurCLI``.
    """
    with pytest.raises(TypeError):
        afficheur_cli.reecrire_ligne(123)

def test_afficheur_cli_lance_animation_chargement(mocker, afficheur_cli):
    """
    Vérifie que la méthode lance_animation_chargement démarre bien un thread
    pour l'animation de chargement.

    Scénarios testés:
        - Lancement de l'animation de chargement.

    Asserts:
        - Vérifie que le thread est bien initialisé et actif.

    Args:
        mocker (MockerFixture): Fixture pour modifier les méthodes internes.
        afficheur_cli (AfficheurCLI): Fixture pour l'instance de la classe ``AfficheurCLI``.
    """
    mocker.patch.object(afficheur_cli, "_animation_chargement", side_effect=lambda: sleep(10))
    assert afficheur_cli._thread_chargement is None
    afficheur_cli.lance_animation_chargement()
    assert afficheur_cli._thread_chargement is not None
    assert afficheur_cli._thread_chargement.is_alive()

def test_afficheur_cli_exception_stop_animation_chargment_type_invalide(afficheur_cli):
    """
    Vérifie que la méthode stop_animation_chargement renvoie une erreur lorsque le type
    de son paramètre est invalide.

    Scénarios testés:
        - Paramètre ``erreur`` avec un mauvais type.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        afficheur_cli (AfficheurCLI): Fixture pour l'instance de la classe ``AfficheurCLI``.
    """
    with pytest.raises(TypeError):
        afficheur_cli.stop_animation_chargement("False")

def test_afficheur_cli_stop_animation_chargement_terminee(afficheur_cli):
    """
    Vérifie que la méthode stop_animation_chargement arrête correctement l'animation en
    cas de demande d'arrêt suite à une fin de chargement normale.

    Scénarios testés:
        - Arrêt normal de l'animation de chargement.

    Asserts:
        - Vérifie que le thread est bien arrêté.
        - Vérifie que le flag d'arrêt normale est activé.

    Args:
        afficheur_cli (AfficheurCLI): Fixture pour l'instance de la classe ``AfficheurCLI``.
    """
    afficheur_cli.lance_animation_chargement()
    afficheur_cli.stop_animation_chargement()
    assert afficheur_cli._thread_chargement is None
    assert afficheur_cli._thread_chargement is None
    assert afficheur_cli._thread_chargement_termine.is_set()

def test_afficheur_cli_stop_animation_chargement_erreur(afficheur_cli):
    """
    Vérifie que la méthode stop_animation_chargement arrête correctement l'animation en
    cas de demande d'arrêt suite à une erreur.

    Scénarios testés:
        - Arrêt normal de l'animation de chargement.

    Asserts:
        - Vérifie que le thread est bien arrêté.
        - Vérifie que le flag d'arrêt d'erreur est activé.

    Args:
        afficheur_cli (AfficheurCLI): Fixture pour l'instance de la classe ``AfficheurCLI``.
    """
    afficheur_cli.lance_animation_chargement()
    afficheur_cli.stop_animation_chargement(True)
    assert afficheur_cli._thread_chargement is None
    assert afficheur_cli._thread_chargement_erreur.is_set()