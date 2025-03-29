"""
Module pour l'analyse statistique d'un fichier log Apache.
"""

from collections import Counter
from parse.fichier_log_apache import FichierLogApache


class AnalyseurLogApache:
    """
    Représente un analysateur pour faire une analyse statistique d'un fichier
    log Apache et créer des statistiques à partir de ce dernier.
    Attributes:
        fichier (FichierLogApache): Le fichier de log Apache à analyser.
        nombre_par_top (int): Le nombre maximal d'éléments à inclure dans
            les statistiques des classements (tops).
    """

    def __init__(self, fichier_log_apache: FichierLogApache, nombre_par_top: int = 3):
        """
        Initialise un nouveau analysateur de fichier log Apache.
        Args:
            fichier_log_apache (FichierLogApache): Le fichier à analyser.
            nombre_par_top (int): Le nombre maximal d'éléments à inclure dans
                les statistiques des classements (tops). Par défaut, sa valeur est égale à ``3``.
        Raises:
            TypeError: Si l'argument ``fichier_log_apache`` n'est pas une instance de :class:`FichierLogApache`
                ou si l'argument ``nombre_par_top`` n'est pas un entier.
            ValueError: Si l'argument ``nombre_par_top`` est inférieur à ``0``.
        """
        if not isinstance(fichier_log_apache, FichierLogApache):
            raise TypeError("La représentation du fichier doit être de type FichierLogApache.")
        if not isinstance(nombre_par_top, int) or isinstance(nombre_par_top, bool):
            raise TypeError("Le nombre par top doit être un entier.")
        if nombre_par_top < 0:
            raise ValueError("Le nombre par top doit être supérieur ou égale à 0.")
        self.fichier = fichier_log_apache
        self.nombre_par_top = nombre_par_top

    def _get_repartition_elements(self,
                          liste_elements: list, 
                          nom_elements: str, 
                          mode_top_classement: bool = False) -> list:
        """
        Retourne le top 'n' des éléments qui apparaissent le plus dans la liste.
        Args:
            liste_elements (list): La liste des éléments.
            nom_elements (str): Le nom des éléments.
            mode_top_classement (bool): Indique si la méthode doit retourner ou non le top
                'n' des éléments les plus présents, où 'n' est égale à l'attribut
                :attr:`nombre_par_top`. Par défaut, ce mode est désactivé (valeur à ``False``).
        Returns:
            list: Une liste de dictionnaires contenant, pour chaque élément :
                - Sa valeur.
                - Son nombre total d'apparitions.
                - Son taux d'apparition dans la liste.
                La liste est triée dans l'ordre décroissant selon le nombre d'apparitions.  
                Si ``mode_top_classement`` est défini à ``True``, elle contient au maximum 
                :attr:`nombre_par_top` éléments, mais peut en contenir moins s'il y a moins 
                de :attr:`nombre_par_top` éléments distincts.
        """
        if not isinstance(liste_elements, list):
            raise TypeError("La liste des éléments doit être une instance du type list.")
        if not isinstance(nom_elements, str):
            raise TypeError("Le nom des éléments doit être une chaîne de caractères")
        if not isinstance(mode_top_classement, bool):
            raise TypeError("L'indication de l'activation du mode 'top_classement' doi être un booléen.")
        
        total_elements = len(liste_elements)
        compteur_elements = Counter(liste_elements)
        top_elements = compteur_elements.most_common(self.nombre_par_top if mode_top_classement else None)
        return [
            {nom_elements: element, "total": total, "taux": total / total_elements * 100}
            for element, total in top_elements
        ]
    
    def get_analyse_complete(self) -> dict:
        """
        Retourne l'analyse complète du fichier de log Apache.
        Returns:
            dict: L'analyse sous forme d'un dictionnaire.
                Le dictionnaire suit la structure suivante:
                - chemin: chemin du fichier
                - statistiques:
                    - requetes:
                        - top_urls: voir :meth:`get_top_urls`
                        - repartition_code_statut_http: voir :meth:`get_total_par_code_statut_http`
        """
        return {
            "chemin": self.fichier.chemin,
            "statistiques": {
                "total_entrees": self.get_total_entrees(),
                "requetes": {
                    "top_urls": self.get_top_urls(),
                    "repartition_code_statut_http": self.get_total_par_code_statut_http()
                }
            }
        }

    def get_total_entrees(self) -> int:
        """
        Retourne le nombre total d'entrées dans le fichier.
        Returns:
            int: Le nombre total d'entrées.
        """
        return len(self.fichier.entrees)
    
    def get_top_urls(self) -> list:
        """
        Retourne le top :attr:`nombre_par_top` des urls les plus demandées.
        Returns:
            list: Une liste de dictionnaires où chaque clé contient :
                - url: L'URL demandée.
                - total: Le nombre total de fois où cette URL a été demandée.
                - taux: Le pourcentage de demandes correspondant à cette URL.
                La liste est triée dans l'ordre décroissant du nombre total d'apparitions.
        """
        return self._get_repartition_elements(
            [entree.requete.url for entree in self.fichier.entrees],
            "url",
            True
        )
    
    def get_total_par_code_statut_http(self) -> list:
        """
        Retourne la répartition des réponses par code de statut htpp retourné.
        Returns:
            list: Une liste de dictionnaires où chaque clé contient :
                - code: Le code de statut http.
                - total: Le nombre total de fois où ce code a été demandée.
                - taux: Le pourcentage de demandes correspondant à ce code.
                La liste est triée dans l'ordre décroissant du nombre total d'apparitions.
        """
        return self._get_repartition_elements(
            [entree.reponse.code_statut_http for entree in self.fichier.entrees],
            "code"
        )