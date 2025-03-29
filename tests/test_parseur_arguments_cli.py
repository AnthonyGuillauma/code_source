"""
Module des tests unitaires pour le parseur des arguments passés depuis la CLI.
"""

import pytest
from cli.parseur_arguments_cli import ArgumentCLIException


# Données utilisées pour les tests unitaires

chemins_valides = [
    "fichier.log",
    "f1chier.txt",
    "./fichier.log",
    "C:\\Users\\fest\\gros_fichier.log"
]

chemins_invalides = [
    "",
    "f$chier#2.log",
    "fichier txt"
]

sorties_valides = [
    "fichier.json",
    "./fichier.json",
    "C:/Users/fest/fichier.json"
]

arguments_invalides = [
    ["fichier.txt", "-s"],
    ["fichier.txt", "-f", "inutile"],
    ["fichier.txt", "--faux", "inutile"],
    ["fichier.txt", "--faux", "inutile", "-d"],
]

# Tests unitaires

@pytest.mark.parametrize("arguments", arguments_invalides)
def test_parseur_cli_exception_argument_inconnu(parseur_arguments_cli, arguments):
    """
    Vérifie qu'une erreur est retournée lorsque un argument est passé en CLI et qu'il
    n'est pas reconnu.

    Scénarios testés:
        - Demande de parsage d'arguments avec des arguments invalides.

    Asserts:
        - Une exception :class:`ArgumentCLIException` est levée lorsque un argument est invalide.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
        argument (list): Une liste avec des arguments.
    """
    with pytest.raises(ArgumentCLIException):
        arguments = parseur_arguments_cli.parse_args(args=arguments)

@pytest.mark.parametrize("chemin_log", chemins_valides)
def test_parseur_cli_recuperation_chemin_log_valide(parseur_arguments_cli, chemin_log):
    """
    Vérifie que le chemin du log Apache fourni depuis la ligne de commande est bien
    récupéré par le parseur.

    Scénarios testés:
        - Demande de parsage d'un chemin de log.

    Asserts:
        - La valeur du chemin de log est bien récupérée et conforme à l'entrée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
        chemin_log (str): Un chemin de fichier valide.
    """
    arguments = parseur_arguments_cli.parse_args(args=[chemin_log])
    assert arguments.chemin_log == chemin_log

@pytest.mark.parametrize("chemin_log", chemins_invalides)
def test_parseur_cli_exception_chemin_log_invalide(parseur_arguments_cli, chemin_log):
    """
    Vérifie qu'une erreur est retournée lorsque le chemin du log Apache fourni contient
    au moins un caractère non autorisé.

    Scénarios testés:
        - Demande de parsage d'un chemin de log avec un format invalide.

    Asserts:
        - Une exception :class:`ArgumentCLIException` est levée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
        chemin_log (str): Un chemin de fichier invalide.
    """
    with pytest.raises(ArgumentCLIException):
        parseur_arguments_cli.parse_args(args=[chemin_log])

@pytest.mark.parametrize("chemin_sortie", sorties_valides)
def test_parseur_cli_recuperation_chemin_sortie_valide(parseur_arguments_cli, chemin_sortie):
    """
    Vérifie que le chemin du fichier de sortie JSON fourni depuis la ligne de commande est bien
    récupéré par le parseur.

    Scénarios testés:
        - Demande de parsage d'un chemin de fichier de sortie.

    Asserts:
        - La valeur du chemin de sortie est bien récupérée et conforme à l'entrée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
        chemin_sortie (str): Un chemin de fichier de sortie valide.
    """
    arguments = parseur_arguments_cli.parse_args(args=["fichier.txt", "-s", chemin_sortie])
    assert arguments.sortie == chemin_sortie

@pytest.mark.parametrize("chemin_sortie", chemins_invalides)
def test_parseur_cli_exception_chemin_sortie_invalide(parseur_arguments_cli, chemin_sortie):
    """
    Vérifie qu'une erreur est retournée lorsque le chemin du fichier de sortie fourni contient
    au moins un caractère non autorisé.

    Scénarios testés:
        - Demande de parsage d'un chemin de fichier de sortie invalide.

    Asserts:
        - Une exception :class:`ArgumentCLIException` est levée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
        chemin_sortie (str): Un chemin de fichier de fichier invalide.
    """
    with pytest.raises(ArgumentCLIException):
        parseur_arguments_cli.parse_args(args=["fichier.txt", "-s", chemin_sortie])

def test_parseur_cli_recuperation_chemin_sortie_defaut_valide(parseur_arguments_cli):
    """
    Vérifie que le chemin du fichier de sortie JSON par défaut est bien appliqué lorsque
    aucun chemin de sortie n'est donné.

    Scénarios testés:
        - Demande de parsage avec aucun fichier de sortie indiqué.

    Asserts:
        - La bonne valeur par défaut pour le chemin de sortie à été appliquée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
    """
    argument = parseur_arguments_cli.parse_args(args=["fichier.txt"])
    assert argument.sortie == "./analyse-log-apache.json"

def test_parseur_cli_verification_extention_chemin_sortie(parseur_arguments_cli):
    """
    Vérifie qu'une erreur est retournée lorsque le fichier de sortie fourni ne possède
    pas l'extension '.json'.

    Scénarios testés:
        - Demande de parsage d'un fichier de sortie qui n'est pas un fichier .json.

    Asserts:
        - Une exception :class:`ArgumentCLIException` est levée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
    """
    with pytest.raises(ArgumentCLIException):
        parseur_arguments_cli.parse_args(args=["fichier.txt", "-s", "invalide.txt"])
