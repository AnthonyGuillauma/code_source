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

    Args:
        code_statut_http (int): Le code de statut HTTP.
        taille_octets (Optional[int]): La taille de la réponse en octets.
            Peut être None si non fournie.
    """

    code_statut_http: int
    taille_octets: Optional[int]

    def __post_init__(self):
        """
        Vérifie le bon type des données de cette classe lors de l'initialisation de l'instance.

        Raises:
            TypeError: Une donnée n'est pas du bon type.
        """
        # Vérification du code de statut HTTP
        if (not isinstance(self.code_statut_http, int)
        or isinstance(self.code_statut_http, bool)):
            raise TypeError("Le code de statut HTTP doit être un entier.")
        # Vérification de la taille de la réponse (en octets)
        if (self.taille_octets is not None
            and not isinstance(self.taille_octets, int)
            or isinstance(self.taille_octets, bool)):
            raise TypeError("La taille en octets doit être un entier ou None.")
