"""
Module qui contient la classe pour représenter une entrée log Apache.
"""

from dataclasses import dataclass
from donnees.client_informations import ClientInformations
from donnees.requete_informations import RequeteInformations
from donnees.reponse_informations import ReponseInformations


@dataclass
class EntreeLogApache:
    """
    Représente une entrée dans un fichier de log Apache.

    Attributes:
        client (ClientInformations): Les informations du client.
        requete (RequeteInformations): Les informations de la requête.
        reponse (ReponseInformations): Les informations de la réponse.
    """
    client: ClientInformations
    requete: RequeteInformations
    reponse: ReponseInformations

    def __post_init__(self):
        """
        Vérifie le bon type des données de cette classe lors de l'initialisation de l'instance.

        Raises:
            TypeError: Une donnée n'est pas du bon type.
        """
        # Validation des informations
        if not isinstance(self.client, ClientInformations):
            raise TypeError(
                "Les informations du client dans une entrée doivent être"
                "regroupées au sein d'un objet ClientInformations."
            )
        if not isinstance(self.requete, RequeteInformations):
            raise TypeError(
                "Les informations de la requête dans une entrée doivent être"
                "regroupées au sein d'un objet RequeteInformations."
            )
        if not isinstance(self.reponse, ReponseInformations):
            raise TypeError(
                "Les informations de la réponse dans une entrée doivent être"
                "regroupées au sein d'un objet ReponseInformations."
            )
