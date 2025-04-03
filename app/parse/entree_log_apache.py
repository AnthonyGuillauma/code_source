"""
Module qui contient la classe pour représenter une entrée log Apache.
"""

from donnees.client_informations import ClientInformations
from donnees.requete_informations import RequeteInformations
from donnees.reponse_informations import ReponseInformations

class EntreeLogApache:
    """
    Représente une entrée dans un fichier de log Apache.

    Attributes:
        informations_client (ClientInformations): Les informations du client.
        informations_requete (RequeteInformations): Les informations de la requête.
        informations_reponse (ReponseInformations): Les informations de la réponse.
    """
    def __init__(self, 
                 informations_client: ClientInformations,
                 informations_requete: RequeteInformations,
                 informations_reponse: ReponseInformations
                 ):

        # Validation des informations
        if not isinstance(informations_client, ClientInformations):
            raise TypeError("Les informations du client dans une entrée doivent être"
                "regroupées au sein d'un objet ClientInformations.")
        if not isinstance(informations_client, ClientInformations):
            raise TypeError("Les informations de la requête dans une entrée doivent être"
                "regroupées au sein d'un objet RequeteInformations.")
        if not isinstance(informations_client, ClientInformations):
            raise TypeError("Les informations de la réponse dans une entrée doivent être"
                "regroupées au sein d'un objet ReponseInformations.")

        # Récupération des informations
        self.client = informations_client
        self.requete = informations_requete
        self.reponse = informations_reponse