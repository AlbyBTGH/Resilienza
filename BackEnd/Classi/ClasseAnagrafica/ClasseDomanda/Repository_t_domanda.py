# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDomanda/Repository_t_domanda.py

from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
from Classi.ClasseAnagrafica.ClasseDriver.Domain_t_driver import TDriver 
# NUOVO IMPORT NECESSARIO per la relazione
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Domain_t_gruppo_risposta import TGruppoRisposta
import logging
from datetime import datetime

class Repository_t_domanda:
    """
    Gestisce le operazioni di accesso ai dati per la tabella 'domande'.
    """
    def __init__(self):
        """
        Inizializza la sessione per le operazioni sul database.
        """
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        """
        Crea la tabella 'domande' se non esiste.
        """
        session = self.Session()
        try:
            TDomanda.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'domande' creata o già esistente (secondo il modello TDomanda).")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'domande': {str(e)}")
            raise
        finally:
            session.close()

    def _domanda_to_dict(self, domanda: TDomanda) -> dict:
        """
        Converte un oggetto TDomanda (con relazioni caricate) in un dizionario,
        includendo i dettagli del Gruppo Risposta.
        """
        # Garantisce che la conversione del driver sia gestita correttamente
        driver_descr = domanda.driver_rel.descr if domanda.driver_rel else None
        
        # Gestisce la relazione NUOVA (gruppo_risposta_rel)
        gruppo_risposta_descr = domanda.gruppo_risposta_rel.descr if domanda.gruppo_risposta_rel else None
        
        data = {
            'id': domanda.id,
            'descr': domanda.descr,
            'id_driver': domanda.id_driver,
            'data_ultima_modifica': domanda.data_ultima_modifica.isoformat() if domanda.data_ultima_modifica else None,
            'modificato_da': domanda.modificato_da,
            # Dettagli del Driver
            'descr_driver': driver_descr,
            # NUOVI CAMPI DEL GRUPPO DI RISPOSTA
            'id_gruppo_risposta': domanda.id_gruppo_risposta,
            'descr_gruppo_risposta': gruppo_risposta_descr,
        }
        return data

    def get_all(self, id_driver_filter: int = None):
        """
        Recupera tutte le domande, con opzione di filtro per ID del driver, 
        caricando EAGERLY le relazioni Driver e GruppoRisposta.
        """
        session = self.Session()
        try:
            query = session.query(TDomanda).options(
                joinedload(TDomanda.driver_rel),
                joinedload(TDomanda.gruppo_risposta_rel) # **AGGIUNTO joinedload**
            )

            if id_driver_filter is not None:
                query = query.filter(TDomanda.id_driver == id_driver_filter)
            
            domande_db = query.all()
            
            # Usa la funzione helper per la conversione
            domande_data = [self._domanda_to_dict(domanda) for domanda in domande_db]
            
            return domande_data

        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero di tutte le domande: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_id(self, domanda_id: int):
        """
        Recupera una domanda tramite ID, caricando EAGERLY le relazioni Driver e GruppoRisposta.
        """
        session = self.Session()
        try:
            domanda = session.query(TDomanda).options(
                joinedload(TDomanda.driver_rel),
                joinedload(TDomanda.gruppo_risposta_rel) # **AGGIUNTO joinedload**
            ).filter_by(id=domanda_id).first()
            
            if domanda:
                return self._domanda_to_dict(domanda)
            return None
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero della domanda {domanda_id}: {str(e)}")
            raise
        finally:
            session.close()

    def create(self, descr: str, id_driver: int, modificato_da: str, id_gruppo_risposta: int = None):
        """
        Crea una nuova domanda nel database.
        """
        session = self.Session()
        try:
            # La domanda viene creata con o senza l'associazione iniziale al gruppo di risposta
            new_domanda = TDomanda(
                descr=descr,
                id_driver=id_driver,
                id_gruppo_risposta=id_gruppo_risposta, # **NUOVO CAMPO**
                modificato_da=modificato_da
            )
            session.add(new_domanda)
            session.commit()
            session.refresh(new_domanda)
            logging.info(f"Nuova domanda creata con ID: {new_domanda.id}")
            
            # Ritorna il dizionario completo della nuova domanda
            return self._domanda_to_dict(new_domanda)
        except IntegrityError as e:
            session.rollback()
            logging.error(f"Errore di integrita nella creazione della domanda: {str(e)}")
            raise ValueError("Violazione dell'integrita dei dati (ad es. ID Driver/Gruppo Risposta non valido).")
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nella creazione della domanda: {str(e)}")
            raise
        finally:
            session.close()

    def update(self, domanda_id: int, descr: str, id_driver: int, id_gruppo_risposta: int, modificato_da: str):
        """
        Aggiorna una domanda esistente nel database, includendo il gruppo di risposta.
        """
        session = self.Session()
        try:
            domanda = session.query(TDomanda).filter_by(id=domanda_id).first()
            if domanda:
                domanda.descr = descr
                domanda.id_driver = id_driver
                
                # **NUOVA LOGICA:** Aggiorna il gruppo di risposta
                # Se id_gruppo_risposta è 0 o None, imposta il campo a None (chiave esterna nullable)
                domanda.id_gruppo_risposta = id_gruppo_risposta if id_gruppo_risposta else None
                
                domanda.modificato_da = modificato_da
                
                session.commit()
                # Ricarica l'oggetto per ottenere le relazioni aggiornate
                # Usiamo una subquery per ricaricare con le relazioni caricate
                updated_domanda = session.query(TDomanda).options(
                    joinedload(TDomanda.driver_rel),
                    joinedload(TDomanda.gruppo_risposta_rel)
                ).filter_by(id=domanda_id).first()

                logging.info(f"Domanda {domanda_id} aggiornata.")
                
                # Ritorna il dizionario completo usando la funzione helper
                return self._domanda_to_dict(updated_domanda)
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento della domanda {domanda_id}: {str(e)}")
            raise
        finally:
            session.close()

    def delete(self, domanda_id: int):
        """
        Elimina fisicamente una domanda dal database.
        """
        session = self.Session()
        try:
            domanda = session.query(TDomanda).filter_by(id=domanda_id).first()
            if domanda:
                session.delete(domanda)
                session.commit()
                logging.info(f"Domanda {domanda_id} eliminata fisicamente.")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione della domanda {domanda_id}: {str(e)}")
            raise
        finally:
            session.close()
