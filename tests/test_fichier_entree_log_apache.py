"""
Module des tests unitaires pour la classe de représentation d'un fichier de log
ou celle d'une entrée d'un log.
"""

import pytest
from datetime import datetime
from parse.fichier_log_apache import FichierLogApache
from parse.entree_log_apache import EntreeLogApache
from donnees.client_informations import ClientInformations
from donnees.requete_informations import RequeteInformations
from donnees.reponse_informations import ReponseInformations


@pytest.mark.parametrize("chemin, entrees", [
    (False, []),
    ("Chemin", False)
])
def test_fichier_log_exception_type_invalide(chemin, entrees):
    """
    Vérifie que l'initialisation d'un FichierLogApache renvoie une erreur lorsque le type
    de son paramètre est invalide.

    Scénarios testés:
        - Paramètre ``chemin`` avec un mauvais type.
        - Paramètre ``entrees`` avec un mauvais type.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        chemin (any): Le chemin du fichier.
        entrees (any): Les entrées du fichier.
    """
    with pytest.raises(TypeError):
        fichier = FichierLogApache(chemin, entrees)

def test_fichier_log_exception_ajoute_entree_type_invalide(fichier_log_apache):
    """
    Vérifie que la méthode ajoute_entree retourne une erreur lorsque son paramètre
    n'est pas du type attendu.

    Scénarios testés:
        - Paramètre ``entree`` avec un mauvais type.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        fichier_log_apache (FichierLogApache): Fixture pour l'instance 
            de la classe :class:`FichierLogApache`.
    """
    with pytest.raises(TypeError):
        fichier_log_apache.ajoute_entree(False)

@pytest.mark.parametrize("client, requete, reponse", [
    (False,
     RequeteInformations(datetime(1, 1, 1), "GET", "/", "HTTP/1.1", "/"),
     ReponseInformations(0, 0)),
    (ClientInformations("1.1.1.1", "RFC", "test", "google"),
     False,
     ReponseInformations(0, 0)),
    (ClientInformations("1.1.1.1", "RFC", "test", "google"),
     RequeteInformations(datetime(1, 1, 1), "GET", "/", "HTTP/1.1", "/"),
     False)
])
def test_entree_log_exception_type_invalide(client, requete, reponse):
    """
    Vérifie que l'initialisation d'un EntreeLogApache renvoie une erreur lorsque le type
    de son paramètre est invalide.

    Scénarios testés:
        - Paramètre ``client`` avec un mauvais type.
        - Paramètre ``requete`` avec un mauvais type.
        - Paramètre ``reponse`` avec un mauvais type.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        client (any): Les informations du client sur cette entrée.
        requete (any): Les informations de la requête sur cette entrée.
        reponse (any): Les informations de la réponse sur cette entrée.
    """
    with pytest.raises(TypeError):
        entree = EntreeLogApache(client, requete, reponse)