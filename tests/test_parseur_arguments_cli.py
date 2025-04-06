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
    "./",
    "./dossier/",
    "C:/Users/fest/dossier/"
]

arguments_invalides = [
    ["fichier.txt", "-s"],
    ["fichier.txt", "-f", "inutile"],
    ["fichier.txt", "--faux", "inutile"],
    ["fichier.txt", "--faux", "inutile", "-d"],
]

# Tests unitaires

@pytest.mark.parametrize("args, namespace", [
    (False, None),
    (None, False)
])
def test_parseur_cli_exception_parse_args_type_invalide(parseur_arguments_cli, args, namespace):
    """
    Vérifie que la méthode parse_args renvoie une erreur lorsque le type
    d'un de ses paramètres est invalide.

    Scénarios testés:
        - Paramètre ``args`` avec un mauvais type.
        - Paramètre ``namespace`` avec un mauvais type.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
        args (Optional[list]): Une liste avec des arguments.
        namespace (Optional[Namespace]): L'espace de nom où stocker les arguments.
    """
    with pytest.raises(TypeError):
        parseur_arguments_cli.parse_args(args, namespace)

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
    Vérifie que le chemin du dossier de sortie fourni depuis la ligne de commande est bien
    récupéré par le parseur.

    Scénarios testés:
        - Demande de parsage d'un chemin de dossier de sortie.

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
    Vérifie qu'une erreur est retournée lorsque le chemin du dossier de sortie fourni contient
    au moins un caractère non autorisé.

    Scénarios testés:
        - Demande de parsage d'un chemin du dossier de sortie invalide.

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
    Vérifie que le chemin du dossier de sortie par défaut est bien appliqué lorsque
    aucun dossier de sortie n'est donné.

    Scénarios testés:
        - Demande de parsage avec aucun dossier de sortie indiqué.

    Asserts:
        - La bonne valeur par défaut pour le chemin de sortie à été appliquée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
    """
    argument = parseur_arguments_cli.parse_args(args=["fichier.txt"])
    assert argument.sortie == "./"

@pytest.mark.parametrize("adresse_ip", [
    ("127.0.0.1"), ("192.168.0.0"), ("10.0.0.8")
])
def test_parseur_cli_recuperation_filtre_adresse_ip_valide(parseur_arguments_cli, adresse_ip):
    """
    Vérifie que le filtre sur l'adresse IP fourni depuis la ligne de commande est bien
    récupéré par le parseur.

    Scénarios testés:
        - Ajout d'un filtre sur l'adresse IP dans les arguments de la CLI.

    Asserts:
        - La valeur de l'adresse IP est bien récupérée et conforme à l'entrée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
        adresse_ip (str): Le filtre sur l'adresse IP.
    """
    arguments = parseur_arguments_cli.parse_args(args=["fichier.txt", "-i", adresse_ip])
    assert arguments.ip == adresse_ip

@pytest.mark.parametrize("code_statut_http", [
    ("200"), ("302"), ("404")
])
def test_parseur_cli_recuperation_filtre_code_statut_http_valide(parseur_arguments_cli,
                                                                 code_statut_http):
    """
    Vérifie que le filtre sur le code de statut http fourni depuis la ligne de commande est bien
    récupéré par le parseur.

    Scénarios testés:
        - Ajout d'un filtre sur le code de statut http dans les arguments de la CLI.

    Asserts:
        - La valeur du code de statut http est bien récupérée et conforme à l'entrée.
        - La valeur du code de statut http est bien convertie en entier.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
        code_statut_http (str): Le filtre sur le code de statut http.
    """
    arguments = parseur_arguments_cli.parse_args(args=["fichier.txt", "-c", code_statut_http])
    assert arguments.code_statut_http == int(code_statut_http)

@pytest.mark.parametrize("code_statut_http_invalide", [
    ("test"), ("invalide")
])
def test_parseur_cli_exception_recuperation_filtre_code_statut_http_invalide(
    parseur_arguments_cli,
    code_statut_http_invalide):
    """
    Vérifie qu'une erreur se produit lorsque le filtre sur le code de statut http n'est pas
    convertisable en un entier.

    Scénarios testés:
        - Ajout d'un filtre sur le code de statut http invalide dans les arguments de la CLI.

    Asserts:
        - Une exception :class:`ArgumentCLIException` est levée.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurArgumentsCLI`.
        code_statut_http_invalide (str): Le filtre invalide sur le code de statut http.
    """
    with pytest.raises(ArgumentCLIException):
        arguments = parseur_arguments_cli.parse_args(
            args=["fichier.txt", "-c", code_statut_http_invalide])