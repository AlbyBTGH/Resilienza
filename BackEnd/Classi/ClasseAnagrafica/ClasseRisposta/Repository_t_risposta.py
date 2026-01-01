# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseRisposta/Repository_t_risposta.py

from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseRisposta.Domain_t_risposta import TRisposta
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Domain_t_gruppo_risposta import TGruppoRisposta
import logging
from datetime import datetime

class Repository_t_risposta:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        try:
            TRisposta.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'risposta' creata o già esistente.")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'risposta': {str(e)}")
            raise

    def get_all(self):
        session = self.Session()
        try:
            # Carica in modo anticipato la relazione con la tabella dei gruppi
            risposte = session.query(TRisposta).options(joinedload(TRisposta.gruppi_risposta)).all()
            return risposte
        except SQLAlchemyError as e:
            logging.error(f"Errore durante il recupero di tutte le risposte: {str(e)}")
            return []
        finally:
            session.close()

    def get_by_id(self, risposta_id: int):
        session = self.Session()
        try:
            # Carica in modo anticipato la relazione con la tabella dei gruppi
            risposta = session.query(TRisposta).options(joinedload(TRisposta.gruppi_risposta)).filter_by(id=risposta_id).first()
            return risposta
        except SQLAlchemyError as e:
            logging.error(f"Errore durante il recupero della risposta con ID {risposta_id}: {str(e)}")
            return None
        finally:
            session.close()

    def create(self, descr: str, gruppi_risposta_ids: list, peso: float, modificato_da: str):
        session = self.Session()
        try:
            # 1. Crea l'oggetto Risposta (senza le relazioni inizialmente)
            risposta = TRisposta(
                descr=descr,
                peso=peso,
                modificato_da=modificato_da,
                data_ultima_modifica=datetime.now()
            )
            session.add(risposta)
            # NOTA: Non chiamiamo commit qui.

            # 2. Associa i Gruppi (CRUCIALE per Many-to-Many)
            if gruppi_risposta_ids:
                # Carica gli oggetti TGruppoRisposta esistenti che corrispondono agli ID
                # forniti dal frontend.
                gruppi = session.query(TGruppoRisposta).filter(
                    TGruppoRisposta.id.in_(gruppi_risposta_ids)
                ).all()

                # Associa gli oggetti TGruppoRisposta alla collezione della risposta.
                # SQLAlchemy gestirà l'inserimento nella tabella di associazione.
                risposta.gruppi_risposta.extend(gruppi)
                
            # 3. Commit finale: salva sia la Risposta che le sue associazioni.
            session.commit()
            
            # 4. Ricarica per garantire il corretto caricamento delle relazioni (Lazy Loading)
            session.refresh(risposta) 
            loaded_risposta = session.query(TRisposta).options(joinedload(TRisposta.gruppi_risposta)).filter_by(id=risposta.id).first()
            
            logging.info(f"Risposta {loaded_risposta.id} creata e associata ai gruppi.")
            return loaded_risposta
            
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nella creazione della risposta e associazione: {str(e)}")
            raise
        finally:
            session.close()

    def update(self, risposta_id: int, descr: str, gruppi_risposta_ids: list[int], peso: float, modificato_da: str):
        session = self.Session()
        try:
            risposta = session.query(TRisposta).filter_by(id=risposta_id).first()
            if not risposta:
                return None

            risposta.descr = descr
            risposta.peso = peso
            risposta.modificato_da = modificato_da
            risposta.data_ultima_modifica = datetime.now()

            # Svuota i gruppi esistenti e aggiungi i nuovi
            risposta.gruppi_risposta = []
            if gruppi_risposta_ids:
                gruppi = session.query(TGruppoRisposta).filter(TGruppoRisposta.id.in_(gruppi_risposta_ids)).all()
                risposta.gruppi_risposta.extend(gruppi)

            session.commit()
            
            # Carica la relazione con la sessione ancora aperta
            session.refresh(risposta)
            
            # Utilizza joinedload per caricare la relazione prima della chiusura
            # Questo è l'unico modo per risolvere l'errore di lazy loading
            updated_risposta = session.query(TRisposta).options(joinedload(TRisposta.gruppi_risposta)).filter_by(id=risposta_id).first()

            logging.info(f"Risposta {risposta_id} aggiornata.")
            return updated_risposta
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento della risposta {risposta_id}: {str(e)}")
            raise
        finally:
            session.close()

    def delete(self, risposta_id: int):
        session = self.Session()
        try:
            risposta = session.query(TRisposta).filter_by(id=risposta_id).first()
            if risposta:
                session.delete(risposta)
                session.commit()
                logging.info(f"Risposta {risposta_id} eliminata fisicamente.")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione della risposta {risposta_id}: {str(e)}")
            raise
        finally:
            session.close()