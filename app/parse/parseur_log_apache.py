"""
Module pour parser un fichier log Apache.
"""

import os
from re import match, compile
from datetime import datetime


class ParseurLogApache():
    """
    Représente un parseur pour faire une analyse synthaxique d'un fichier
    log Apache.
    Attributes:
        PATTERN_ENTREE_LOG_APACHE (str): Le pattern regex d'une entrée dans un log Apache.
    """

    PATTERN_ENTREE_LOG_APACHE = (
        r'(?P<ip>\S+) (?P<rfc>\S+) (?P<user>\S+)'
        r' (\[(?P<timestamp>.+?)\]|-) "((?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)|-)"'
        r' (?P<status>\d+) (?P<size>\d+|-)'
        r'( "(?P<referer>.*?)" "(?P<user_agent>.*?)")?'
    )

    def __init__(self, chemin_log):
        """
        Initialise un nouveau parseur de fichier log Apache et vérifie que
        le fichier passé en paramètre existe.
        Args:
            chemin_log (str): Le chemin du fichier à analyser.
        Raises:
            FileNotFoundError: Si le fichier à analyser est introuvable.
        """
        if not self.__fichier_existe(chemin_log):
            raise FileNotFoundError(f"Le fichier {chemin_log} est introuvable.")
        self.chemin_log = chemin_log

    def __fichier_existe(self, chemin_fichier):
        """
        Vérifie que le chemin passé en paramètre correspond à une fichier existant.
        Returns:
            bool: True s'il existe, False sinon.
        """
        if not os.path.isfile(chemin_fichier):
            return False
        return True