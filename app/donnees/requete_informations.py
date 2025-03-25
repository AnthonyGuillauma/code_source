"""
Module relatif aux informations de la requete dans un fichier de log Apache.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class RequeteInformations:
    """
    Représente les informations de la requête HTTP dans un log Apache.

    Attributes:
        horodatage (datetime): L'horodatage de la requête.
        methode_http (str): La méthode HTTP utilisée.
        url (str): L'URL cible de la requête.
        protocole_http (str): Le protocole HTTP utilisé.
        ancienne_url (Optional[str]): L'URL de provenance (referrer).
            Peut être None si non fournie.

    Raises:
        TypeError: Si les attributs ne sont pas du type attendu ou None.
    """
    horodatage: datetime
    methode_http: str
    url: str
    protocole_http: str
    ancienne_url: Optional[str]

    def __post_init__(self):
        # Vérification de l'horodatage
        if not isinstance(self.horodatage, datetime):
            raise TypeError("L'horodatage doit être de type datetime.")
        # Vérification de la méthode HTTP
        if not isinstance(self.methode_http, str):
            raise TypeError("La méthode HTTP doit être une chaine de caractère.")
        # Vérification de la ressource demandée
        if not isinstance(self.url, str):
            raise TypeError("L'URL doit être une chaine de caractère.")
        # Vérification du protocole HTTP
        if not isinstance(self.protocole_http, str):
            raise TypeError("Le protocole HTTP doit être une chaine de caractère.")
        # Vérification de l'ancienne URL
        if self.ancienne_url != None and not isinstance(self.ancienne_url, str):
            raise TypeError("L'ancienne URL doit être une chaine de caractère ou None.")