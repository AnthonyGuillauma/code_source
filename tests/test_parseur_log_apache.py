"""
Module des tests unitaires pour le parseur de fichier de log Apache.
"""

import pytest
from re import match
from datetime import datetime, timezone, timedelta
from conftest import lignes_valides, lignes_invalides
from parse.parseur_log_apache import ParseurLogApache, FormatLogApacheInvalideException


# Tests unitaires

def test_parseur_log_exception_fichier_introuvable():
    """
    Vérifie qu'une exception est bien levée lorsque le chemin du fichier
    passé dans le constructeur n'est pas trouvé.

    Scénarios testés:
        - Création d'une instance avec un chemin invalide.

    Asserts:
        - Une exception :class:`FileNotFoundError` est levée.
    """
    with pytest.raises(FileNotFoundError):
        parseur = ParseurLogApache("fichier/existe/pas.txt")

@pytest.mark.parametrize("parseur_log_apache", [False], indirect=["parseur_log_apache"])
def test_parseur_log_exception_fichier_invalide(parseur_log_apache):
    """
    Vérifie qu'une exception est bien levée lorsque le format d'un fichier n'est
    pas valide (une entrée invalide).

    Scénarios testés:
        - Parsage d'un fichier invalide.

    Asserts:
        - Une exception :class:`FormatLogApacheInvalideException` est levée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurLogApache`.
    """
    with pytest.raises(FormatLogApacheInvalideException):
        fichier = parseur_log_apache.parse_fichier()

@pytest.mark.parametrize("ligne_invalide", lignes_invalides)
def test_parseur_log_exception_entree_invalide(parseur_log_apache, ligne_invalide):
    """
    Vérifie qu'une exception est bien levée lorsque le format d'une entrée
    est invalide.
    
    Scénarios testés:
        - Parsage d'une entrée invalide.

    Asserts:
        - Une exception :class:`FormatLogApacheInvalideException` est levée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurLogApache`.
        ligne_invalide (str): L'entrée à analyser.
    """
    with pytest.raises(FormatLogApacheInvalideException):
        parseur_log_apache.parse_entree(ligne_invalide)

def test_parseur_log_nombre_entrees_valide(parseur_log_apache):
    """
    Vérifie que le nombre d'entrées trouvé correspond au nombre de ligne dans le log.

    Scénarios testés:
        - Parsage d'un fichier et récupération du nombre d'entrées dans ce dernier.

    Asserts:
        - Le nombre d'entrées récupéré est égale au nombre attendu.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurLogApache`.
    """
    fichier_log = parseur_log_apache.parse_fichier()
    assert len(fichier_log.entrees) == len(lignes_valides)

@pytest.mark.parametrize("nom_information, retour_attendu", [
    ("ip", "192.168.1.1"),
    ("rfc", None),
    ("horodatage", "12/Jan/2025:10:15:32 +0000"),
    ("Existe pas !", None)
])
def test_parseur_log_regex_recuperation_information_entree(parseur_log_apache, 
                                                           nom_information, 
                                                           retour_attendu):
    """
    Vérifie que la récupération des informations à partir d'un résultat de regex fonctionne
    correctement et que toutes valeurs introuvables ou égales à - renvoient None.

    Scénarios testés:
        - Récupération d'une information avec une valeur.
        - Récupération d'une information sans valeur (égale à -).
        - Récupération d'une information inexistante.

    Asserts:
        - La valeur retournée est égale à celle attendue. 
    
    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurLogApache`.
        nom_information (str): Nom de l'information à récupérer.
        retour_attendu (Union[None, str]): La valeur attendue de l'information.
    """
    ligne = '192.168.1.1 - - [12/Jan/2025:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 532'
    analyse = match(parseur_log_apache.PATTERN_ENTREE_LOG_APACHE, ligne)
    resultat_analyse = analyse.groupdict()
    assert parseur_log_apache.get_information_entree(resultat_analyse, nom_information) == retour_attendu

def test_parsage_entree_valide(parseur_log_apache):
    """
    Vérifie qu'une entrée est correctement analysée et que les informations partent
    au bon endroit avec le bon typage.

    Scénarios testés:
        - Parsage d'une entrée valide et récupération des valeurs trouvées.

    Asserts:
        - Les valeurs sont égales à celles attendues. 

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurLogApache`.
    """
    ligne = '192.168.1.1 - - [12/Jan/2025:10:15:32 +0000] "GET /index.html HTTP/1.1" ' \
    '200 532 "/home" "Chrome/133.0.0.0"'
    entree = parseur_log_apache.parse_entree(ligne)
    assert entree.client.adresse_ip == "192.168.1.1"
    assert entree.client.identifiant_rfc == None
    assert entree.client.nom_utilisateur == None
    assert entree.client.agent_utilisateur == "Chrome/133.0.0.0"
    assert entree.requete.horodatage == datetime(2025, 1, 12, 10, 15, 32, 
                                                 tzinfo=timezone(timedelta(hours=0)))
    assert entree.requete.methode_http == "GET"
    assert entree.requete.url == "/index.html"
    assert entree.requete.protocole_http == "HTTP/1.1"
    assert entree.requete.ancienne_url == "/home"
    assert entree.reponse.code_statut_http == 200
    assert entree.reponse.taille_octets == 532
