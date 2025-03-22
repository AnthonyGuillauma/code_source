"""
Module relatif aux informations d'un client dans un fichier de log Apache.
"""


class ClientInformations:

    def __init__(self,
                 adresse_ip,
                 identifiant_rfc,
                 nom_utilisateur,
                 agent_utilisateur
                 ):
        self.adresse_ip = adresse_ip
        self.identifiant_rfc = identifiant_rfc
        self.nom_utilisateur = nom_utilisateur
        self.agent_utilisateur = agent_utilisateur