"""
Module relatif aux informations de la réponse dans un fichier de log Apache.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ReponseInformations:
    """
    Représente les informations de la réponse HTTP à partir d'une entrée d'un log Apache.

    Cette classe regroupe les données extraites d'une entrée de log,
    qui concernent les informations techniques sur la réponse émise par
    le serveur Apache au client.

    Attributes:
        code_statut_http (int): Le code de statut HTTP.
        taille_octets (Optional[int]): La taille de la réponse en octets.
            Peut être None si non fournie.

    Raises:
        TypeError: Si les attributs ne sont pas du type int.
    """

    code_statut_http: int
    taille_octets: Optional[int]

    def __post_init__(self):
        # Vérification du code de statut HTTP
        if not isinstance(self.code_statut_http, int):
            raise TypeError("Le code de statut HTTP doit être un entier.")
        # Vérification de la taille de la réponse (en octets)
        if self.taille_octets != None and not isinstance(self.taille_octets, int):
            raise TypeError("La taille en octets doit être un entier ou None.")
