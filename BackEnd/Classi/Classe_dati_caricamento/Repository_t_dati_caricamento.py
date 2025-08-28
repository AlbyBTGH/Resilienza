# Classi/Classe_dati_caricamento/Repository_t_dati_caricamento.py
from ..ClasseDB.db_connection import SessionLocal
from .Domain_t_dati_caricamento import TDatiCaricamento

class RepositoryTDatiCaricamento:
    def __init__(self, session=None):
        self.db = session if session else SessionLocal()

    def add(self, dati_caricamento):
        try:
            self.db.add(dati_caricamento)
            self.db.commit()
            return dati_caricamento
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_all(self):
        """
        Recupera tutti i record dalla tabella t_dati_caricamento.
        """
        try:
            return self.db.query(TDatiCaricamento).all()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()