# Classi/Classe_dati_caricamento/Service_t_dati_caricamento.py
from .Domain_t_dati_caricamento import TDatiCaricamento
from .Repository_t_dati_caricamento import RepositoryTDatiCaricamento
from ..ClasseDB.db_connection import SessionLocal

class ServiceTDatiCaricamento:
    def __init__(self):
        self.repo = RepositoryTDatiCaricamento()
    
    def log_caricamento(self, descrizione, utente, numero_record, stato):
        try:
            dati_caricamento = TDatiCaricamento(
                descrizione=descrizione,
                utente=utente,
                numero_record=numero_record,
                stato=stato
            )
            return self.repo.add(dati_caricamento)
        except Exception as e:
            raise e
        
    def get_all_caricamenti(self):
        """
        Recupera tutti i record di caricamento dal repository.
        """
        try:
            return self.repo.get_all()
        except Exception as e:
            raise e