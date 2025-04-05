"""
Module pour analyser les arguments passés en ligne de commande.
"""

from argparse import ArgumentParser, Namespace
from re import match
from typing import Optional


class ParseurArgumentsCLI(ArgumentParser):
    """
    Représente un parseur pour analyser les arguments passés en ligne
    de commande pour l'application.
    """

    def __init__(self):
        """
        Initialise uparseur pour analyser les arguments passés en ligne de commande.
        """
        super().__init__(
            description="LogBuster, l'analyseur de log Apache.", allow_abbrev=False,
        )
        self.__set_arguments()

    def __set_arguments(self) -> None:
        """
        Définit les arguments attendus par l'application.

        Returns:
            None
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
        self.add_argument(
            "-i",
            "--ip",
            type=str,
            help="L'adresse IP que doivent avoir les entrées à analyser."
        )
        self.add_argument(
            "-c",
            "--code-statut-http",
            type=int,
            help="Le code de statut http que doivent avoir les entrées à analyser."
        )

    def parse_args(self,
                   args: Optional[list] = None,
                   namespace: Optional[Namespace] = None) -> Namespace:
        """
        Récupère les arguments passés en ligne de commande puis vérifie
        que leur format est conforme à ceux attendus.

        Args:
            args (Optional[list]): Liste des arguments passés en paramètre. 
                Si ``None``, les arguments de la ligne de commande sont utilisés.
            namespace (Optional[Namespace]): Un espace de noms (namespace) 
                pour stocker les résultats. Si ``None``, un nouvel espace de noms est créé.

        Returns:
            Namespace: L'objet contenant les arguments analysés et leurs valeurs.
        
        Raises:
            ArgumentCLIException: Si une erreur se produit lors du parsing des arguments 
                (par exemple, si un argument inconnu est fourni ou si son format est invalide).
        """
        # Vérification du type des paramètres
        if args is not None and not isinstance(args, list):
            raise TypeError("Les arguments doivent soit être None, soit être dans une liste.")
        if namespace is not None and not isinstance(args, Namespace):
            raise TypeError("L'espace de noms doit soit être None, soit être un objet Namespace.")

        # Analyse des arguments
        try:
            arguments_parses = super().parse_args(args, namespace)
        except SystemExit as ex: #Arguments inconnus
            raise ArgumentCLIException() from ex

        # Vérification syntaxique des arguments
        regex_chemin = r"^[a-zA-Z0-9:_\\\-.\/]+$"

        if not match(regex_chemin, arguments_parses.chemin_log):
            raise ArgumentCLIException(
                "Le chemin du fichier log doit uniquement contenir les caractères autorisés. "
                "Les caractères autorisés sont les minuscules, majuscules, chiffres ou les "
                "caractères spéciaux suivants: _, \\, -, /."
            )

        if not match(regex_chemin, arguments_parses.sortie):
            raise ArgumentCLIException(
                "Le chemin du fichier de sortie doit uniquement contenir les caractères "
                "autorisés. Les caractères autorisés sont les minuscules, majuscules, "
                "chiffres ou les caractères spéciaux suivants: _, \\, -, /."
            )

        if not arguments_parses.sortie.endswith(".json"):
            raise ArgumentCLIException(
                "Le fichier de sortie doit obligatoirement être un fichier au format json."
            )

        return arguments_parses


class ArgumentCLIException(Exception):
    """
    Représente une erreur lorsque un argument passé en ligne de commande
    est inconnu ou que son format est invalide.
    """

    def __init__(self, *args):
        super().__init__(*args)
