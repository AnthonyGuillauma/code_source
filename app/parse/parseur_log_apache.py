"""
Module pour parser un fichier log Apache.
"""

import os
from re import match
from datetime import datetime
from parse.fichier_log_apache import FichierLogApache, EntreeLogApache
from donnees.client_informations import ClientInformations
from donnees.requete_informations import RequeteInformations
from donnees.reponse_informations import ReponseInformations


class ParseurLogApache():
    """
    Représente un parseur pour faire une analyse synthaxique d'un fichier
    log Apache.
    Attributes:
        PATTERN_ENTREE_LOG_APACHE (str): Le pattern regex d'une entrée dans un log Apache.
    """

    PATTERN_ENTREE_LOG_APACHE = (
        r'(?P<ip>\S+) (?P<rfc>\S+) (?P<utilisateur>\S+)'
        r' (\[(?P<horodatage>.+?)\]|-) "((?P<methode>\S+) (?P<url>\S+) (?P<protocole>\S+)|-)"'
        r' (?P<code_status>\d+) (?P<taille_octets>\d+|-)'
        r'( "(?P<ancienne_url>.*?)" "(?P<agent_utilisateur>.*?)")?'
    )

    def __init__(self, chemin_log):
        """
        Initialise un nouveau parseur de fichier log Apache et vérifie que
        le fichier passé en paramètre existe.
        Args:
            chemin_log (str): Le chemin du fichier à analyser.
        Raises:
            FileNotFoundError: Si le fichier à analyser est introuvable.
        """
        if not self.__fichier_existe(chemin_log):
            raise FileNotFoundError(f"Le fichier {chemin_log} est introuvable.")
        self.chemin_log = chemin_log

    def __fichier_existe(self, chemin_fichier):
        """
        Vérifie que le chemin passé en paramètre correspond à une fichier existant.
        Returns:
            bool: True s'il existe, False sinon.
        """
        if not os.path.isfile(chemin_fichier):
            return False
        return True
    
    def parse_fichier(self):
        """
        Effectue une analyse syntaxique du fichier de log Apache puis retourne
        une représentation du fichier avec les informations trouvées.
        Returns:
            log_analyse (FichierLogApache): Représentation du fichier.
        Raises:
            FormatLogApacheInvalideException: Format du fichier log invalide.
        """
        log_analyse = FichierLogApache(self.chemin_log)
        numero_ligne = 1
        with open(self.chemin_log, "r") as log:
            for ligne in log:
                try:
                    log_analyse.ajoute_entree(self.parse_entree(ligne))
                    numero_ligne += 1
                except FormatLogApacheInvalideException as ex:
                    raise FormatLogApacheInvalideException(
                        f"Le format de l'entrée à la ligne {numero_ligne}"
                        f"('{ligne}') est invalide."
                    ) from ex
        return log_analyse

    def parse_entree(self, entree):
        """
        Effectue une analyse syntaxique d'une entrée dans un fichier de log
        Apache puis retourne une représentation de l'entrée avec les
        informations trouvées.
        Args:
            entree (str): Entrée à analyser.
        Returns:
            entree_analysee (EntreeLogApache): Représentation de l'entrée.
        Raises:
            FormatLogApacheInvalideException: Format de l'entrée du fichier log invalide.
        """
        # Analyse de l'entrée
        analyse = match(self.PATTERN_ENTREE_LOG_APACHE, entree)
        if not analyse:
            raise FormatLogApacheInvalideException()
        resultat_analyse = analyse.groupdict()
        # Récupération des informations liées au client
        adresse_ip = self.get_information_entree(resultat_analyse, "ip")
        identifiant_rfc = self.get_information_entree(resultat_analyse, "rfc")
        utilisateur = self.get_information_entree(resultat_analyse, "utilisateur")
        agent_utilisateur = self.get_information_entree(resultat_analyse, "agent_utilisateur")
        informations_client = ClientInformations(
            adresse_ip, identifiant_rfc, utilisateur, agent_utilisateur
        )
        # Récupération des informations liées à la requête
        horodatage = self.get_information_entree(resultat_analyse, "horodatage")
        if horodatage:
            horodatage = datetime.strptime(horodatage, "%d/%b/%Y:%H:%M:%S %z")
        methode_http = self.get_information_entree(resultat_analyse, "methode")
        url = self.get_information_entree(resultat_analyse, "url")
        protocole_http = self.get_information_entree(resultat_analyse, "protocole")
        ancienne_url = self.get_information_entree(resultat_analyse, "ancienne_url")
        informations_requete = RequeteInformations(
            horodatage, methode_http, url, protocole_http, ancienne_url
        )
        # Récupération des informations liées à la réponse
        code_statut = self.get_information_entree(resultat_analyse, "code_status")
        if code_statut:
            code_statut = int(code_statut)
        taille_octets = self.get_information_entree(resultat_analyse, "taille_octets")
        if taille_octets:
            taille_octets = int(taille_octets)
        informations_reponse = ReponseInformations(
            code_statut, taille_octets
        )
        return EntreeLogApache(
            informations_client, informations_requete, informations_reponse
        )

    def get_information_entree(self, analyse_regex, nom_information):
        """
        Retourne la valeur de l'information dans l'analyse si elle possède une valeur
        ou None si elle ne possède pas de valeur (égale à - ou vide).
        Args:
            analyse_regex (Match[str]): Résultat du regex de l'analyse.
            nom_information (str): Nom de l'information souhaitée.
        Returns:
            Union[str, None]: La valeur sous forme de chaîne de caractère ou None si
                aucune valeur n'a été trouvée.
        """
        if nom_information in analyse_regex:
            valeur = analyse_regex[nom_information]
            if valeur != "-" and valeur != "":
                return valeur
        return None




class FormatLogApacheInvalideException(Exception):

    def __init__(self, *args):
        super().__init__(*args)