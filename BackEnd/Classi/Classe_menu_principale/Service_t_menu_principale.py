# Classi/Classe_menu_principale/Service_t_menu_principale.py
import logging
from Classi.Classe_menu_principale.Repository_t_menu_principale import Repository_t_menu_principale # Corrected import name

class Service_t_menu_principale:
    
    def __init__(self):
        self.repository = Repository_t_menu_principale()

    def get_menu_principale(self):
        """
        Recupera tutti gli elementi del menu principale dal repository.
        Il repository è ora responsabile della formattazione o della gestione degli errori.
        """
        return self.repository.get_menu_principale()
    
    def get_by_title(self, title):
        return self.repository.get_by_title(title) # This returns the Domain object
    
    def get_by_id(self, id):
        return self.repository.get_by_id(id)
