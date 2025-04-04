"""
Module relatif aux informations d'un client dans un fichier de log Apache.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ClientInformations:
    """
    Représente les informations d'un client à partir d'une entrée d'un log Apache.

    Cette classe regroupe les données extraites d'une entrée de log,
    qui concernent le client ayant effectué la requête au serveur Apache.

    Args:
        adresse_ip (str): L'adresse IP du client.
        identifiant_rfc (Optional[str]): L'identifiant RFC du client. 
            Peut être None si non fournie.
        nom_utilisateur (Optional[str]): Le nom de l'utilisateur authentifié. 
            Peut être None si non fournie.
        agent_utilisateur (Optional[str]): L'agent utilisateur (User-Agent). 
            Peut être None si non fournie.

    Raises:
        TypeError: Si les attributs ne sont pas de type `str` ou `None`.
    """
    adresse_ip: str
    identifiant_rfc: Optional[str]
    nom_utilisateur: Optional[str]
    agent_utilisateur: Optional[str]

    def __post_init__(self):
        # Validation de l'adresse IP
        if not isinstance(self.adresse_ip, str):
            raise TypeError("L'adresse IP est obligatoire et doit être une chaîne de caractères.")
        # Validation de l'identifiant RFC
        if self.identifiant_rfc is not None and not isinstance(self.identifiant_rfc, str):
            raise TypeError("L'identifiant RFC doit être une chaîne de caractères ou None.")
        # Validation du nom d'utilisateur
        if self.nom_utilisateur is not None and not isinstance(self.nom_utilisateur, str):
            raise TypeError("Le nom d'utilisateur doit être une chaîne de caractères ou None.")
        # Validation de l'agent utilisateur
        if self.agent_utilisateur is not None and not isinstance(self.agent_utilisateur, str):
            raise TypeError("L'agent utilisateur doit être une chaîne de caractères ou None.")
