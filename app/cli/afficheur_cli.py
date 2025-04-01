"""
Module pour les intéractions avec la ligne de commande.
"""

import sys
from json import load
from time import sleep
from random import choice
import colorama
import threading


class AfficheurCLI:
    """
    Représente une classe pour afficher des informations dans la ligne de commande.

    Attributes:
        COULEUR_MESSAGE_NORMAL (str): La couleur pour les messages normaux en CLI.
        COULEUR_MESSAGE_ERREUR (str): La couleur pour les messages d'erreur en CLI.
        _thread_chargement (Union[None,Thread]): Le thread de l'animation de chargement.
        _thread_chargement_demande_arret (Event): L'évènement pour demander au thread de
            l'animation de chargement de s'arrêter.
        _animations_actuelles (dict): Les éléments visuels pour l'animation de chargement.
    """
    COULEUR_MESSAGE_NORMAL = colorama.Fore.WHITE
    COULEUR_MESSAGE_ERREUR = colorama.Fore.RED

    def __init__(self):
        """
        Initialise un objet pour afficher des informations dans la ligne de commande.
        """
        # Initialise les variables pour le chargement
        self._thread_chargement = None
        self._thread_chargement_demande_arret = threading.Event()
        # Récupère les animations
        with open("assets/animations.json", "r", encoding="utf-8") as animations:
            elements_animations = load(animations)
        # Choisis une animation au hasard parmi chaque catégorie d'animation
        self._animations_actuelles = {
            "chasseur": choice(elements_animations["chasseurs"]),
            "fantome": choice(elements_animations["fantomes"]),
            "rayon_laser": elements_animations["rayons_laser"]
        }

    def reecrire_ligne(self, message: str):
        """
        Permet d'écrire des caractères par dessus la dernière ligne dans la
        ligne de commande.

        Args:
            message (str): Les caractères à afficher.

        Returns:
            None

        Raises:
            TypeError: Le paramètre ``message`` n'est pas une chaîne de caractères.
        """
        # Validation du paramètre
        if not isinstance(message, str):
            raise TypeError("Le message pour la réécriture doit être une chaîne de caractères.")
        # Ecriture du message
        sys.stdout.write("\r" + self.COULEUR_MESSAGE_NORMAL + message)
        sys.stdout.flush()

    def affiche_message(self, message: str):
        """
        Permet d'écrire un message commun dans la ligne de commande avec la bonne
        couleur.

        Args:
            message (str): Le message à afficher.

        Returns:
            None

        Raises:
            TypeError: Le paramètre ``message`` n'est pas une chaîne de caractères.
        """
        # Validation du paramètre
        if not isinstance(message, str):
            raise TypeError("Le message doit être une chaîne de caractères.")
        # Ecriture du message
        print(self.COULEUR_MESSAGE_NORMAL + message, flush=True)

    def affiche_erreur(self, message: str, exception: Exception):
        """
        Permet d'écrire un message d'erreur dans la ligne de commande avec la bonne
        couleur.

        Args:
            message (str): Le message à afficher.
            exception (Exception): L'exception à afficher.

        Returns:
            None

        Raises:
            TypeError: Le paramètre ``message`` n'est pas une chaîne de caractères ou
                le paramètre ``exception`` n'est pas une instance de la classe :class:`Exception`.
        """
        # Validation des paramètres
        if not isinstance(message, str):
            raise TypeError("Le message d'erreur doit être une chaîne de caractères.")
        if not isinstance(exception, Exception):
            raise TypeError("L'exception à afficher doit être une instance de Exception.")
        # Ecriture du message
        print(self.COULEUR_MESSAGE_ERREUR + f"{message}\n{exception}", flush=True, end="\r")

    def lance_animation_chargement(self):
        """
        Lance une animation de chargement dans la ligne de commande via un thread non bloquant.
        Si l'animation de chargement est déjà en cours, cette méthode ne fait rien.

        Returns:
            None
        """
        # Si le thread est déjà lancé, annulation de l'animation
        if self._thread_chargement and self._thread_chargement.is_alive():
            return
        # On réinitialise la demande d'arrêt
        self._thread_chargement_demande_arret.clear()
        # Initialisation du thread pour le chargement
        self._thread_chargement = threading.Thread(target=self.__animation_chargement)
        # Lancement du thread pour le chargement
        self._thread_chargement.start()
        
    def __animation_chargement(self):
        """
        Lance l'animation de chargement en boucle jusqu'à la demande d'arrêt via
        l'attribut :attr:`_thread_chargement_demande_arret`.

        Returns:
            None
        """
        # Eléments de l'animation de chargement
        chasseur_chargement = self._animations_actuelles["chasseur"][0]
        fantome_chargement = self._animations_actuelles["fantome"][0]
        signes_rayon_laser = self._animations_actuelles["rayon_laser"]
        couleurs = ["\033[91m", "\033[93m", "\033[94m", "\033[95m"] # Rouge, Jaune, Bleu, Magenta
        
        # Eléments de l'animation de fin de chargement
        chasseur_gagne = self._animations_actuelles["chasseur"][2]
        fantome_perd = self._animations_actuelles["fantome"][1]

        # Variables pour l'animation de chargement
        index_boucle = 0
        rayon_laser = ""

        # Début de l'animation (jusqu'à la demande d'arrêt)
        while not self._thread_chargement_demande_arret.is_set():
            # Récupération de la prochaine couleur
            couleur_courante = couleurs[(index_boucle % len(couleurs))]
            # Récupération du prochain signe du rayon
            signe_courant = signes_rayon_laser[(index_boucle % len(signes_rayon_laser))]
            # Ajout du dernier signe avec la nouvelle couleur au rayon
            rayon_laser += couleur_courante + signe_courant
            # Réactualisation de l'animation de chargement
            self.reecrire_ligne(f"{chasseur_chargement}{rayon_laser}\033[0m{fantome_chargement}")
            index_boucle += 1
            sleep(0.05)

        # Suppression de la ligne de chargement
        self.reecrire_ligne("\033[K")
        # Message d'animation terminée
        self.reecrire_ligne(f"{chasseur_gagne}{" " * index_boucle}\033[0m{fantome_perd}")

    def stop_animation_chargement(self):
        """
        Lance une demande d'arrêt au thread qui gère l'animation de chargement
        en cours. Si aucune animation n'est en cours, cette méthode ne fait rien.

        Returns:
            None
        """
        # Si le thread de chargement existe et est lancé
        if self._thread_chargement and self._thread_chargement.is_alive():
            # Lancement de la demade d'arrêt
            self._thread_chargement_demande_arret.set()
            # Attente de l'arrêt depuis le thread principal
            self._thread_chargement.join()
            self.affiche_message(f"\nAnalyse terminée! We came, we saw, we logged it.")
