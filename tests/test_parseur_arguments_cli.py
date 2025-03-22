"""
Module des tests unitaires pour le parseur des arguments passés depuis la CLI.
"""

import pytest
from cli.parseur_arguments_cli import ParseurArgumentsCLI, ArgumentCLIException

# Données utilisées pour les tests unitaires

@pytest.fixture
def parseur_arguments_cli():
    """
    Fixture pour initialiser le parseur d'arguments CLI.
    Retourne une instance de la classe ParseurArgumentsCLI pour être utilisée dans les tests.
    Returns:
        ParseurArgumentsCLI: Une instance de la classe ParseurArgumentsCLI.
    """
    return ParseurArgumentsCLI()

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

# Tests unitaires

@pytest.mark.parametrize("chemin_log", chemins_valides)
def test_recuperation_chemin_log_valide(parseur_arguments_cli, chemin_log):
    """
    Vérifie que le chemin du log Apache fourni depuis la ligne de commande est bien
    récupéré par le parseur.
    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe ParseurArgumentsCLI.
        chemin_log (str): Un chemin de fichier valide.
    Returns:
        None
    """
    arguments = parseur_arguments_cli.parse_args(args=[chemin_log])
    assert arguments.chemin_log == chemin_log

@pytest.mark.parametrize("chemin_log", chemins_invalides)
def test_exception_chemin_log_invalide(parseur_arguments_cli, chemin_log):
    """
    Vérifie qu'une erreur est retournée lorsque le chemin du log Apache fourni contient
    au moins un caractère non autorisé.
    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe ParseurArgumentsCLI.
        chemin_log (str): Un chemin de fichier invalide.
    Returns:
        None
    """
    with pytest.raises(ArgumentCLIException):
        parseur_arguments_cli.parse_args(args=[chemin_log])

@pytest.mark.parametrize("chemin_sortie", sorties_valides)
def test_recuperation_chemin_sortie_valide(parseur_arguments_cli, chemin_sortie):
    """
    Vérifie que le chemin du fichier de sortie JSON fourni depuis la ligne de commande est bien
    récupéré par le parseur.
    Args:
        parseur_arguments_cli: Fixture pour l'instance de la classe ParseurArgumentsCLI
    Returns:
        None
    """
    arguments = parseur_arguments_cli.parse_args(args=["fichier.txt", "-s", chemin_sortie])
    assert arguments.sortie == chemin_sortie

@pytest.mark.parametrize("chemin_sortie", chemins_invalides)
def test_exception_chemin_sortie_invalide(parseur_arguments_cli, chemin_sortie):
    """
    Vérifie qu'une erreur est retournée lorsque le chemin du fichier de sortie fourni contient
    au moins un caractère non autorisé.
    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe ParseurArgumentsCLI.
        chemin_sortie (str): Un chemin de fichier invalide.
    Returns:
        None
    """
    with pytest.raises(ArgumentCLIException):
        parseur_arguments_cli.parse_args(args=["fichier.txt", "-s", chemin_sortie])

def test_recuperation_chemin_sortie_defaut_valide(parseur_arguments_cli):
    """
    Vérifie que le chemin du fichier de sortie JSON par défaut est bien appliqué lorsque
    aucun chemin de sortie n'est donné.
    Args:
        parseur_arguments_cli: Fixture pour l'instance de la classe ParseurArgumentsCLI
    Returns:
        None
    """
    argument = parseur_arguments_cli.parse_args(args=["fichier.txt"])
    assert argument.sortie == "./analyse-log-apache.json"

def test_verification_extention_chemin_sortie(parseur_arguments_cli):
    """
    Vérifie qu'une erreur est retournée lorsque le fichier de sortie fourni ne possède
    pas l'extension '.json'.
    Args:
        parseur_arguments_cli: Fixture pour l'instance de la classe ParseurArgumentsCLI
    Returns:
        None
    """
    with pytest.raises(ArgumentCLIException):
        parseur_arguments_cli.parse_args(args=["fichier.txt", "-s", "invalide.txt"])
