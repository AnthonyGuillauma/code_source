"""
Module relatif aux informations de la requete dans un fichier de log Apache.
"""


class RequeteInformations:

    def __init__(self,
                 horodatage,
                 methode_http,
                 url,
                 protocole_http,
                 ancienne_url
                 ):
        self.horodatage = horodatage
        self.methode_http = methode_http
        self.url = url
        self.protocole_http = protocole_http
        self.ancienne_url = ancienne_url