# Classi/ClasseQuestionario/Repository_t_questionario.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseQuestionario.Domain_t_questionario import TQuestionario, t_questionario_domande
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
import logging

class Repository_t_questionario:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        session = self.Session()
        try:
            TQuestionario.__table__.create(bind=engine, checkfirst=True)
            t_questionario_domande.create(bind=engine, checkfirst=True)
            logging.info("Tabelle 'questionario' e 'questionario_domande' create o gia esistenti.")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione delle tabelle: {str(e)}")
            raise
        finally:
            session.close()

    def get_all(self):
        session = self.Session()
        try:
            questionari = session.query(TQuestionario).options(joinedload(TQuestionario.domande)).all()
            return questionari
        except SQLAlchemyError as e:
            logging.error(f"Errore nella lettura dei questionari: {str(e)}")
            return []
        finally:
            session.close()

    # Logica di creazione del questionario
    def create(self, descr, creato_da, domande_ids):
        session = self.Session()
        try:
            nuovo_questionario = TQuestionario(descr=descr, creato_da=creato_da)
            
            # Recupera le domande dal database
            domande_selezionate = session.query(TDomanda).filter(TDomanda.id.in_(domande_ids)).all()
            
            # Aggiungi le domande al questionario
            nuovo_questionario.domande.extend(domande_selezionate)

            session.add(nuovo_questionario)
            session.commit()
            session.refresh(nuovo_questionario)
            logging.info(f"Questionario '{nuovo_questionario.descr}' creato con successo.")
            return nuovo_questionario
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nel repository durante la creazione del questionario: {str(e)}")
            raise
        finally:
            session.close()

    def update(self, questionario_id, descr, modificato_da, domande_ids):
        session = self.Session()
        try:
            questionario = session.query(TQuestionario).filter_by(id=questionario_id).first()
            if questionario:
                questionario.descr = descr
                questionario.modificato_da = modificato_da

                questionario.domande.clear()
                domande_selezionate = session.query(TDomanda).filter(TDomanda.id.in_(domande_ids)).all()
                questionario.domande.extend(domande_selezionate)

                session.commit()
                session.refresh(questionario)
                logging.info(f"Questionario {questionario_id} aggiornato.")
                return questionario
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento del questionario {questionario_id}: {str(e)}")
            raise
        finally:
            session.close()

    def delete(self, questionario_id):
        session = self.Session()
        try:
            questionario = session.query(TQuestionario).filter_by(id=questionario_id).first()
            if questionario:
                session.delete(questionario)
                session.commit()
                logging.info(f"Questionario {questionario_id} eliminato.")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione del questionario {questionario_id}: {str(e)}")
            raise
        finally:
            session.close()