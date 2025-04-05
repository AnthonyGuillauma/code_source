"""
Module pour les filtres lors d'une analyse d'un fichier log Apache.
"""

from typing import Optional
from parse.entree_log_apache import EntreeLogApache


class FiltreLogApache:
    """
    Représente le filtre à appliquer lors d'une analyse d'un fichier de log Apache.

    Attributes:
        adresse_ip (Optional[str]): L'adresse IP que doit avoir une entrée pour
            pouvoir passer le filtre. Si sa valeur est ``None``, ce filtre ne sera
            pas appliqué.
        code_statut_http (Optional[int]): Le code de statut http que doit avoir une entrée
            pour pouvoir passer le filtre. Si sa valeur est ``None``, ce filtre ne sera
            pas appliqué.
    """

    def __init__(self, filtre_adresse_ip: Optional[str], filtre_code_statut_http: Optional[int]):
        """
        Initalise le filtre à appliquer lors d'une analyse.

        Args:
            filtre_adresse_ip (Optional[str]): L'adresse IP que doit avoir une entrée pour
                pouvoir passer le filtre. Si sa valeur est ``None``, cette vérification ne sera
                pas appliqué.
            filtre_code_statut_http (Optional[int]): Le code de statut http que doit 
                avoir une entrée pour pouvoir passer le filtre. Si sa valeur est ``None``,
                cette vérification ne sera pas appliqué.

        Raises:
            TypeError: Les paramètres ne sont pas du type attendu.
        """
        # Vérification des paramètres
        if filtre_adresse_ip is not None and not isinstance(filtre_adresse_ip, str):
            raise TypeError("L'adresse IP dans un filtre doit être une chaîne de caractère.")
        if filtre_code_statut_http is not None and not isinstance(filtre_code_statut_http, int):
            raise TypeError("Un code de statut http dans un filtre doit être un entier.")

        # Ajout des filtres
        self.adresse_ip = filtre_adresse_ip
        self.code_statut_htpp = filtre_code_statut_http

    def entree_passe_filtre(self, entree: EntreeLogApache) -> bool:
        """
        Indique si l'entrée passée en paramètre passe le filtre.

        Args:
            entree (EntreeLogApache): L'entrée à vérifier.

        Returns:
            bool: True si l'entrée passe le filtre, False sinon.

        Raises:
            TypeError: L'``entrée`` n'est pas de type :class:`EntreeLogApache`
        """
        # Vérification du paramètre
        if not isinstance(entree, EntreeLogApache):
            raise TypeError("L'entrée à vérifier pour le filtre doit être de type EntreeLogApache")

        # Vérification que l'entrée passe le filtre
        # Application du filtre sur l'adresse IP si activé
        if self.adresse_ip is not None:
            if self.adresse_ip != entree.client.adresse_ip:
                return False
        # Application du filtre sur le code de statut http si activé
        if self.code_statut_htpp is not None:
            if self.code_statut_htpp != entree.reponse.code_statut_http:
                return False

        return True

    def get_dict_filtre(self) -> dict:
        """
        Retourne le filtre sous forme d'un dictionnaire.
        Les clés représentent le champs d'une entrée et leur valeur la valeur
        que doit avoir ce champs. Si la valeur d'un filtre est ``None``, cela signifie que
        cette vérification n'est pas activé.

        Returns:
            dict: Les filtres sous forme d'un dictionnaire.
        """
        return {
            "adresse_ip": self.adresse_ip,
            "code_statut_http": self.code_statut_htpp
        }
