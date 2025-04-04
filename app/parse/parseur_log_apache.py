"""
Module pour parser un fichier log Apache.
"""

import os
from re import match
from datetime import datetime
from typing import Optional
from parse.fichier_log_apache import FichierLogApache
from parse.entree_log_apache import EntreeLogApache
from donnees.client_informations import ClientInformations
from donnees.requete_informations import RequeteInformations
from donnees.reponse_informations import ReponseInformations


class ParseurLogApache():
    """
    Représente un parseur pour faire une analyse synthaxique d'un fichier
    log Apache.

    Class-level variables:
        :cvar PATTERN_ENTREE_LOG_APACHE (str): Le pattern regex d'une entrée dans un log Apache.
    """

    PATTERN_ENTREE_LOG_APACHE: str = (
        r'(?P<ip>\S+) (?P<rfc>\S+) (?P<utilisateur>\S+)'
        r' (\[(?P<horodatage>\d{2}\/\w{3}\/\d{4}:\d{1,2}:\d{1,2}:\d{1,2} \+\d{4})\]|-)'
        r' "((?P<methode>\S+) (?P<url>\S+) (?P<protocole>\S+)|-)"'
        r' (?P<code_status>\d+) (?P<taille_octets>\d+|-)'
        r'( "(?P<ancienne_url>.*?)")?( "(?P<agent_utilisateur>.*?)")?'
    )

    def __init__(self, chemin_log):
        """
        Initialise un nouveau parseur de fichier log Apache et vérifie que
        le fichier passé en paramètre existe.

        Args:
            chemin_log (str): Le chemin du fichier à analyser.

        Raises:
            TypeError: Le chemin ``chemin_log`` n'est pas de type ``str``.
            FichierLogApacheIntrouvableException: Si le fichier à analyser est introuvable.
        """
        # Vérification du type du paramètre
        if not isinstance(chemin_log, str):
            raise TypeError("Le chemin du log doit être une chaîne de caractères.")
        # Vérification du chemin
        if not os.path.isfile(chemin_log):
            raise FichierLogApacheIntrouvableException(f"Le fichier {chemin_log} est introuvable.")
        # Ajout du chemin
        self.chemin_log = chemin_log

    def parse_fichier(self) -> FichierLogApache:
        """
        Effectue une analyse syntaxique du fichier de log Apache puis retourne
        une représentation du fichier avec les informations trouvées.

        Returns:
            log_analyse (FichierLogApache): Représentation du fichier.

        Raises:
            FormatLogApacheInvalideException: Format du fichier log invalide.
        """
        # Initialisation de la représentation du fichier
        log_analyse = FichierLogApache(self.chemin_log)
        # Ouverture du log
        with open(self.chemin_log, "r", encoding="utf-8") as log:
            # Parcours des entrées du log
            for numero_ligne, ligne in enumerate(log, start=1):
                try:
                    # Parsage de l'entrée
                    entree = self.parse_entree(ligne)
                    log_analyse.ajoute_entree(entree)
                except FormatLogApacheInvalideException as ex:
                    raise FormatLogApacheInvalideException(
                        f"Le format de l'entrée à la ligne {numero_ligne} "
                        f"('{ligne.strip()}') est invalide."
                    ) from ex

        return log_analyse

    def parse_entree(self, entree: str) -> EntreeLogApache:
        """
        Effectue une analyse syntaxique d'une entrée dans un fichier de log
        Apache puis retourne une représentation de l'entrée avec les
        informations trouvées.

        Args:
            entree (str): Entrée à analyser.

        Returns:
            entree_analysee (EntreeLogApache): Représentation de l'entrée.

        Raises:
            TypeError: L'entrée ``entree`` n'est pas de type :class:`EntreeLogApache`
            FormatLogApacheInvalideException: Format de l'entrée du fichier log invalide.
        """
        # Vérification du type du paramètre
        if not isinstance(entree, EntreeLogApache):
            raise TypeError("L'entrée doit être représentée avec un objet EntreeLogApache")

        # Analyse de l'entrée
        analyse = match(self.PATTERN_ENTREE_LOG_APACHE, entree)
        if not analyse:
            raise FormatLogApacheInvalideException()

        # Extraction des résultats d'analyse
        resultat_analyse = analyse.groupdict()

        # Récupération des informations liées au client
        informations_client = self._extraire_informations_client(resultat_analyse)

        # Récupération des informations liées à la requête
        informations_requete = self._extraire_informations_requete(resultat_analyse)

        # Récupération des informations liées à la réponse
        informations_reponse = self._extraire_informations_reponse(resultat_analyse)

        # Retour des informations regroupées dans l'objet EntreeLogApache
        return EntreeLogApache(
            informations_client, informations_requete, informations_reponse
        )

    def _extraire_informations_client(self, analyse_regex: dict) -> ClientInformations:
        """
        Extrait les informations liées au client depuis l'analyse regex d'une entrée.

        Args:
            analyse_regex (dict): Analyse regex d'une entrée.

        Returns:
            ClientInformations: Les informations du client.

        Raises:
            TypeError: L'analyse ``analyse_regex`` n'est pas un ``dict``.
            FormatLogApacheInvalideException: L'adresse IP n'est pas présente dans l'analyse.
        """
        # Vérification du type du paramètre
        if not isinstance(analyse_regex, dict):
            raise TypeError("L'analyse du regex doit être un dictionnaire.")

        # Adresse IP
        adresse_ip = self.get_information_entree(analyse_regex, "ip")
        if adresse_ip is None:
            raise FormatLogApacheInvalideException("L'adresse IP est obligatoire.")
        # Identifiant RFC
        identifiant_rfc = self.get_information_entree(analyse_regex, "rfc")
        # Nom de l'utilisateur
        utilisateur = self.get_information_entree(analyse_regex, "utilisateur")
        # User-Agent
        agent_utilisateur = self.get_information_entree(analyse_regex, "agent_utilisateur")

        return ClientInformations(
            adresse_ip, identifiant_rfc, utilisateur, agent_utilisateur
        )

    def _extraire_informations_requete(self, analyse_regex: dict) -> RequeteInformations:
        """
        Extrait les informations liées à la requête depuis l'analyse regex d'une entrée.

        Args:
            analyse_regex (dict): Analyse regex d'une entrée.

        Returns:
            RequeteInformations: Les informations de la requête.

        Raises:
            TypeError: L'analyse ``analyse_regex`` n'est pas un ``dict``.
            FormatLogApacheInvalideException: L'horodatage n'est pas présente dans l'analyse.
        """
        # Vérification du type du paramètre
        if not isinstance(analyse_regex, dict):
            raise TypeError("L'analyse du regex doit être un dictionnaire.")

        # Horodatage
        horodatage = self.get_information_entree(analyse_regex, "horodatage")
        if horodatage:
            horodatage = datetime.strptime(horodatage, "%d/%b/%Y:%H:%M:%S %z")
        if horodatage is None:
            raise FormatLogApacheInvalideException("L'horodatage est obligatoire.")
        # Méthode HTTP
        methode_http = self.get_information_entree(analyse_regex, "methode")
        # URL de la ressource
        url = self.get_information_entree(analyse_regex, "url")
        # Protocole HTTP
        protocole_http = self.get_information_entree(analyse_regex, "protocole")
        # URL de la précédente ressource demandée
        ancienne_url = self.get_information_entree(analyse_regex, "ancienne_url")

        return RequeteInformations(
            horodatage, methode_http, url, protocole_http, ancienne_url
        )

    def _extraire_informations_reponse(self, analyse_regex: dict) -> ReponseInformations:
        """
        Extrait les informations liées à la réponse depuis l'analyse regex d'une entrée.

        Args:
            analyse_regex (dict): Analyse regex d'une entrée.

        Returns:
            TypeError: L'analyse ``analyse_regex`` n'est pas un ``dict``.
            ReponseInformations: Les informations de la réponse.
        """
        # Vérification du type du paramètre
        if not isinstance(analyse_regex, dict):
            raise TypeError("L'analyse du regex doit être un dictionnaire.")

        # Code de statut
        code_statut = self.get_information_entree(analyse_regex, "code_status")
        code_statut = int(code_statut)
        # Taille de la réponse
        taille_octets = self.get_information_entree(analyse_regex, "taille_octets")
        if taille_octets:
            taille_octets = int(taille_octets)

        return ReponseInformations(
            code_statut, taille_octets
        )

    def get_information_entree(self, analyse_regex: dict, nom_information: str) -> Optional[str]:
        """
        Retourne la valeur de l'information dans l'analyse si elle possède une valeur
        ou None si elle ne possède pas de valeur (égale à - ou vide).

        Args:
            analyse_regex (Match[str]): Résultat du regex de l'analyse.
            nom_information (str): Nom de l'information souhaitée.
        
        Returns:
            Optional[str]: La valeur sous forme de chaîne de caractère ou None si
                aucune valeur n'a été trouvée.

        Raises:
            TypeError: Un paramètre n'a pas le bon type.
        """
        # Vérification du type des paramètres
        if not isinstance(analyse_regex, dict):
            raise TypeError("L'analyse du regex doit être un dictionnaire.")
        if not isinstance(nom_information, str):
            raise TypeError("Le nom de l'information doit être une chaîne de caractères.")

        # Récupération de l'information
        valeur = analyse_regex.get(nom_information)
        return valeur if valeur not in ("", "-") else None

class ParsageLogApacheException(Exception):
    """
    Exception représentant une erreur lors du parsage du fichier
    de log Apache.
    """
    def __init__(self, *args):
        super().__init__(*args)

class FichierLogApacheIntrouvableException(ParsageLogApacheException):
    """
    Exception représentant une erreur lorsque le fichier de log Apache
    est introuvable.
    """

class FormatLogApacheInvalideException(ParsageLogApacheException):
    """
    Exception représentant une erreur dans le format du fichier
    de log Apache fourni.
    """
