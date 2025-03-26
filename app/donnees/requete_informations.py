"""
Module relatif aux informations de la requete dans un fichier de log Apache.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class RequeteInformations:
    """
    Représente les informations de la requête HTTP à partir d'une entrée d'un log Apache.

    Cette classe regroupe les données extraites d'une entrée de log,
    qui concernent les informations techniques sur la requête émise au
    serveur Apache.

    Attributes:
        horodatage (datetime): L'horodatage de la requête.
        methode_http (Optional[str]): La méthode HTTP utilisée.
            Peut être None si non fournie.
        url (Optional[str]): L'URL cible de la requête.
            Peut être None si non fournie.
        protocole_http (Optional[str]): Le protocole HTTP utilisé.
            Peut être None si non fournie.
        ancienne_url (Optional[str]): L'URL de provenance (referrer).
            Peut être None si non fournie.

    Raises:
        TypeError: Si les attributs ne sont pas du type attendu ou None.
    """
    horodatage: datetime
    methode_http: Optional[str]
    url: Optional[str]
    protocole_http: Optional[str]
    ancienne_url: Optional[str]

    def __post_init__(self):
        # Vérification de l'horodatage
        if not isinstance(self.horodatage, datetime):
            raise TypeError("L'horodatage doit être de type datetime.")
        # Vérification de la méthode HTTP
        if self.methode_http != None and not isinstance(self.methode_http, str):
            raise TypeError("La méthode HTTP doit être une chaine de caractère ou None.")
        # Vérification de la ressource demandée
        if self.url != None and not isinstance(self.url, str):
            raise TypeError("L'URL doit être une chaine de caractère ou None.")
        # Vérification du protocole HTTP
        if self.protocole_http != None and not isinstance(self.protocole_http, str):
            raise TypeError("Le protocole HTTP doit être une chaine de caractère ou None.")
        # Vérification de l'ancienne URL
        if self.ancienne_url != None and not isinstance(self.ancienne_url, str):
            raise TypeError("L'ancienne URL doit être une chaine de caractère ou None.")