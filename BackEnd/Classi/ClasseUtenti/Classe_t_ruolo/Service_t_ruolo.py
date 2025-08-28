
# Classi/ClasseUtenti/Classe_t_ruolo/Service_t_ruolo.py
from Classi.ClasseUtenti.Classe_t_ruolo.Repository_t_ruolo import Repository_t_ruolo

class Service_t_ruolo:
    def __init__(self) -> None:
        self.repository = Repository_t_ruolo()

    def create_table_if_not_exists(self):
        return self.repository.create_table_if_not_exists()
    
    def create_default_ruolo(self): # <--- CAMBIATO QUI il nome del metodo
        return self.repository.create_default_ruolo()
        
    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def get_by_descr(self, descr): # <--- AGGIUNTO QUI il metodo
        return self.repository.get_by_descr(descr)
    
    def get_all(self):
        return self.repository.get_all()
    
    def create(self, cod_ruolo, descr, dt_fine_val=None, modificato_da=None, ordinatore=0, visualizza_notifiche=False): # <--- AGGIORNATI i parametri
        return self.repository.create(cod_ruolo, descr, dt_fine_val, modificato_da, ordinatore, visualizza_notifiche)
    
    def update(self, id, cod_ruolo=None, descr=None, dt_fine_val=None, modificato_da=None, ordinatore=None, visualizza_notifiche=None): # <--- AGGIORNATI i parametri
        return self.repository.update(id, cod_ruolo, descr, dt_fine_val, modificato_da, ordinatore, visualizza_notifiche)
    
    def delete(self, id):
        return self.repository.delete(id)