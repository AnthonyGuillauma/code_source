"""
Module pour analyser les arguments passés en ligne de commande.
"""

from argparse import ArgumentParser


class ParseurArgumentsCLI(ArgumentParser):
    """
    Représente un parseur pour analyser les arguments passés en ligne
    de commande pour l'application.
    """

    def __init__(self):
        super().__init__(
            description="LogBuster, l'analyseur de log Apache.", allow_abbrev=False
        )
        self.__set_arguments()

    def __set_arguments(self):
        """
        Définit les arguments attendus par l'application.
        """
        # -- Argument obligatoire --
        self.add_argument(
            "chemin_log",
            type=str,
            help="Chemin du fichier log Apache à analyser."
        )
        # -- Argument optionnel --
        self.add_argument(
            "-s",
            "--sortie",
            type=str,
            default="./analyse-log-apache.json",
            help="Fichier JSON où sera écrit l'analyse. Par défaut, un fichier avec le "
            "nom 'analyse-log-apache.json' dans le repertoire courant sera crée.",
        )

    def parse_args(self, args=None, namespace=None):
        """
        Analyse, vérifie et retourne les arguments fournis en ligne de commande.
        """
        # Analyse des arguments
        try:
            arguments_parses = super().parse_args(args, namespace)
        except Exception as ex:
            raise ArgumentCLIException(str(ex)) from ex

        # Vérification syntaxique des arguments
        if not arguments_parses.sortie.endswith(".json"):
            raise ArgumentCLIException(
                "Le fichier de sortie doit obligatoirement être un fichier au format json."
            )
        
        return arguments_parses


class ArgumentCLIException(Exception):
    """
    Représente une erreur liée l'analyse d'un argument en ligne de commande.
    """

    def __init__(self, *args):
        super().__init__(*args)
