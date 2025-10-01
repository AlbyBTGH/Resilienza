# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseGruppoRisposta/Repository_t_gruppo_risposta.py

from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Domain_t_gruppo_risposta import TGruppoRisposta
import logging
from datetime import datetime

class Repository_t_gruppo_risposta:
    """
    Gestisce le operazioni di accesso ai dati per la tabella 'gruppo_risposta'.
    """
    def __init__(self):
        """
        Inizializza la sessione per le operazioni sul database.
        """
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        """
        Crea la tabella 'gruppo_risposta' se non esiste.
        """
        session = self.Session()
        try:
            TGruppoRisposta.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'gruppo_risposta' creata o già esistente (secondo il modello TGruppoRisposta).")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'gruppo_risposta': {str(e)}")
            raise
        finally:
            session.close()

    
    def _gruppo_risposta_to_dict(self, gruppo: TGruppoRisposta) -> dict:
        """
        Converte un oggetto TGruppoRisposta in un dizionario.
        NOTA: Accesso all'ID reso più robusto per il nome della Primary Key.
        """
        if not gruppo:
            return None
            
        # PROBABILE CORREZIONE: 
        # Tenta di accedere prima all'attributo 'id' standard. 
        # Se non è presente, prova 'id_gruppo_risposta' (attributo comune per ID_GRUPPO_RISPOSTA).
        # In ultima istanza, usa 'ID_GRUPPO_RISPOSTA' se è il nome dell'attributo mappato.
        gruppo_id = getattr(gruppo, 'id', None)
        if gruppo_id is None:
            gruppo_id = getattr(gruppo, 'id_gruppo_risposta', getattr(gruppo, 'ID_GRUPPO_RISPOSTA', None))
            
        # Se anche con i tentativi l'ID è None, solleva un errore o usa un valore di fallback (qui None)
        if gruppo_id is None:
             logging.error("Impossibile recuperare l'ID dell'oggetto TGruppoRisposta.")
        
        return {
            'id': gruppo_id, # CHIAVE 'id' minuscola richiesta dal frontend
            'descr': gruppo.descr,
            'data_ultima_modifica': gruppo.data_ultima_modifica.isoformat() if gruppo.data_ultima_modifica else None,
            'modificato_da': gruppo.modificato_da
        }

    def get_all(self) -> list:
        """
        Recupera tutti i gruppi di risposta 
        """
        session = self.Session()
        try:
            # CORREZIONE/OTTIMIZZAZIONE: Aggiunto filtro e ordinamento
            gruppi = session.query(TGruppoRisposta).order_by(TGruppoRisposta.descr).all()
            return [self._gruppo_risposta_to_dict(g) for g in gruppi]
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero di tutti i gruppi di risposta: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_id(self, gruppo_id: int) -> dict | None:
        """
        Recupera un gruppo di risposta per ID
        """
        session = self.Session()
        try:
            gruppo = session.query(TGruppoRisposta).filter_by(id=gruppo_id).first()
            if gruppo:
                return self._gruppo_risposta_to_dict(gruppo)
            return None
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero del gruppo di risposta {gruppo_id}: {str(e)}")
            raise
        finally:
            session.close()
            
    def get_by_descr(self, descr: str) -> TGruppoRisposta | None:
        """
        Cerca un gruppo di risposta per descrizione.
        """
        session = self.Session()
        try:
            gruppo = session.query(TGruppoRisposta).filter(TGruppoRisposta.descr == descr).first()
            return gruppo
        except SQLAlchemyError as e:
            logging.error(f"Errore nella ricerca per descrizione del gruppo di risposta: {str(e)}")
            raise
        finally:
            session.close()

    def create(self, descr: str, creato_da: str) -> dict:
        """
        Crea un nuovo record nella tabella 'gruppo_risposta'.
        """
        session = self.Session()
        try:
            new_gruppo = TGruppoRisposta(
                descr=descr,
                data_ultima_modifica=datetime.now(),
                modificato_da=creato_da
            )
            session.add(new_gruppo)
            session.commit()
            logging.info(f"Gruppo di risposta {new_gruppo.id} creato.")
            return self._gruppo_risposta_to_dict(new_gruppo)
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nella creazione del gruppo di risposta: {str(e)}")
            raise
        except IntegrityError as e:
             session.rollback()
             logging.error(f"Errore di integrità nella creazione del gruppo di risposta: {str(e)}")
             raise
        finally:
            session.close()
            
    def update(self, gruppo_id: int, descr: str, modificato_da: str = 'system') -> dict | None:
        """
        Aggiorna un record esistente nella tabella 'gruppo_risposta'.
        """
        session = self.Session()
        try:
            gruppo = session.query(TGruppoRisposta).filter_by(id=gruppo_id).first()
            if gruppo:
                gruppo.descr = descr
                gruppo.data_ultima_modifica = datetime.now()
                gruppo.modificato_da = modificato_da
                session.commit()
                logging.info(f"Gruppo di risposta {gruppo_id} aggiornato.")
                return self._gruppo_risposta_to_dict(gruppo)
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento del gruppo di risposta {gruppo_id}: {str(e)}")
            raise
        finally:
            session.close()
            
    def delete(self, gruppo_id: int) -> bool:
        """
        Elimina fisicamente un gruppo di risposta dal database.
        """
        session = self.Session()
        try:
            gruppo = session.query(TGruppoRisposta).filter_by(id=gruppo_id).first()
            if gruppo:
                session.delete(gruppo)
                session.commit()
                logging.info(f"Gruppo di risposta {gruppo_id} eliminato fisicamente.")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione del gruppo di risposta {gruppo_id}: {str(e)}")
            raise
        finally:
            session.close()

    def check_gruppi_risposta_exist(self, gruppi_risposta_ids: list[int]) -> bool:
        """
        Controlla se tutti gli ID di gruppo di risposta forniti esistono nel database.
        """
        if not gruppi_risposta_ids:
            return True
        
        session = self.Session()
        try:
            # Controlla solo gli ID
            count = session.query(TGruppoRisposta).filter(
                TGruppoRisposta.id.in_(gruppi_risposta_ids)
            ).count()
            return count == len(gruppi_risposta_ids)
        except SQLAlchemyError as e:
            logging.error(f"Errore nella verifica dell'esistenza dei gruppi di risposta: {str(e)}")
            raise
        finally:
            session.close()


    def get_by_descr_excluding_self(self, descr: str, gruppo_id: int) -> TGruppoRisposta | None:
        """
        Cerca un gruppo di risposta per descrizione, escludendo un gruppo specifico.
        """
        session = self.Session()
        try:
            gruppo = session.query(TGruppoRisposta).filter(
                TGruppoRisposta.descr == descr,
                TGruppoRisposta.id != gruppo_id
            ).first()
            return gruppo
        except SQLAlchemyError as e:
            logging.error(f"Errore nella ricerca per descrizione (escludendo se stesso): {str(e)}")
            raise
        finally:
            session.close()