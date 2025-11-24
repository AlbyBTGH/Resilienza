# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDomanda/Repository_t_domanda.py

from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
from Classi.ClasseAnagrafica.ClasseDriver.Domain_t_driver import TDriver 
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Domain_t_gruppo_risposta import TGruppoRisposta
import logging
from datetime import datetime

class Repository_t_domanda:
    
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        session = self.Session()
        try:
            TDomanda.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'domande' creata o già esistente.")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'domande': {str(e)}")
            raise
        finally:
            session.close()

    def _domanda_to_dict(self, domanda: TDomanda) -> dict:
        """
        Converte un oggetto TDomanda in un dizionario. 
        Implementa una diagnostica robusta per la descrizione del Driver.
        """
        driver_descr = "N/D (Relazione non Caricata)" # Default se tutto fallisce

        if domanda.driver_rel:
            try:
                # ✅ ACCESSO DEFINITIVO ALL'ATTRIBUTO CORRETTO 'descr'
                desc = domanda.driver_rel.descr
                if desc:
                    driver_descr = desc
                else:
                    driver_descr = f"Driver ID {domanda.id_driver} (NOME VUOTO NEL DB)"
                    
            except AttributeError as e:
                # Questo non dovrebbe succedere con i Domain forniti, ma gestiamo l'errore
                driver_descr = f"Driver ID {domanda.id_driver} (ERRORE DI ATTRIBUTO: {e})"
                logging.error(f"Impossibile accedere all'attributo descr: {e}")
        else:
            # Caso in cui driver_rel è None (il problema attuale)
            driver_descr = f"Driver ID {domanda.id_driver} (Relazione NON CARICATA/NULL)"
            logging.warning(f"Relazione driver_rel mancante per la domanda ID {domanda.id}. Controlla i modelli e il joinedload.")

        # --- LOGICA GRUPPO RISPOSTA ---
        gruppo_risposta_descr = domanda.gruppo_risposta_rel.descr if domanda.gruppo_risposta_rel else None
        
        data = {
            'id': domanda.id,
            'descr': domanda.descr,
            'id_driver': domanda.id_driver,
            'data_ultima_modifica': domanda.data_ultima_modifica.isoformat() if domanda.data_ultima_modifica else None,
            'modificato_da': domanda.modificato_da,
            # Dettagli del Driver (usiamo la descrizione recuperata)
            'descr_driver': driver_descr,
            # NUOVI CAMPI DEL GRUPPO DI RISPOSTA
            'id_gruppo_risposta': domanda.id_gruppo_risposta,
            'descr_gruppo_risposta': gruppo_risposta_descr,
        }
        return data

    def get_all(self, id_driver_filter: int = None):
        session = self.Session()
        try:
            # 💡 ASSICURATI che il joinedload sia attivo e funzioni
            query = session.query(TDomanda).options(
                joinedload(TDomanda.driver_rel),
                joinedload(TDomanda.gruppo_risposta_rel) 
            )

            if id_driver_filter is not None:
                query = query.filter(TDomanda.id_driver == id_driver_filter)
            
            domande_db = query.all()
            domande_data = [self._domanda_to_dict(domanda) for domanda in domande_db]
            return domande_data

        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero di tutte le domande: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_id(self, domanda_id: int):
        session = self.Session()
        try:
            domanda = session.query(TDomanda).options(
                joinedload(TDomanda.driver_rel),
                joinedload(TDomanda.gruppo_risposta_rel) 
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
        session = self.Session()
        try:
            new_domanda = TDomanda(
                descr=descr,
                id_driver=id_driver,
                id_gruppo_risposta=id_gruppo_risposta, 
                modificato_da=modificato_da
            )
            session.add(new_domanda)
            session.commit()
            session.refresh(new_domanda)
            
            # Ricarica con joinedload subito dopo l'inserimento
            new_domanda_with_rel = session.query(TDomanda).options(
                joinedload(TDomanda.driver_rel),
                joinedload(TDomanda.gruppo_risposta_rel)
            ).filter_by(id=new_domanda.id).first()
            
            return self._domanda_to_dict(new_domanda_with_rel), 201
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
        session = self.Session()
        try:
            domanda = session.query(TDomanda).filter_by(id=domanda_id).first()
            if domanda:
                domanda.descr = descr
                domanda.id_driver = id_driver
                domanda.id_gruppo_risposta = id_gruppo_risposta if id_gruppo_risposta else None
                domanda.modificato_da = modificato_da
                
                session.commit()
                
                updated_domanda = session.query(TDomanda).options(
                    joinedload(TDomanda.driver_rel),
                    joinedload(TDomanda.gruppo_risposta_rel)
                ).filter_by(id=domanda_id).first()

                return self._domanda_to_dict(updated_domanda)
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento della domanda {domanda_id}: {str(e)}")
            raise
        finally:
            session.close()

    def delete(self, domanda_id: int):
        session = self.Session()
        try:
            domanda = session.query(TDomanda).filter_by(id=domanda_id).first()
            if domanda:
                session.delete(domanda)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione della domanda {domanda_id}: {str(e)}")
            raise
        finally:
            session.close()