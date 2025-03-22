"""
Module relatif aux informations de la réponse dans un fichier de log Apache.
"""


class ReponseInformations:

    def __init__(self,
                 code_status_http,
                 taille_octets
                 ):
        self.code_status_http = code_status_http
        self.taille_octets = taille_octets
