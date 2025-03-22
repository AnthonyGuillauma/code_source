"""
Module qui contient les classes pour représenter un fichier log Apache.
"""


class FichierLogApache:
    """
    Représente un fichier de log Apache.
    """

    def __init__(self, chemin):
        self.chemin = chemin
        self.entrees = []

    def ajoute_entree(self, entree):
        """
        Ajoute une entrée à la liste des entrées du fichier.
        Args:
            entree (EntreeLogApache): L'entrée à ajouter.
        Returns:
            None
        """
        self.entrees.append(entree)



class EntreeLogApache:
    """
    Représente une entrée dans un fichier de log Apache.
    """
    def __init__(self, 
                 informations_client,
                 informations_requete,
                 informations_reponse
                 ):
        self.client = informations_client
        self.requete = informations_requete
        self.reponse = informations_reponse