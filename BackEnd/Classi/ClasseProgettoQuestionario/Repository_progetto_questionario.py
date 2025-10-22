# Classi/ClasseProgettoQuestionario/Repository_progetto_questionario.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
#from Classi.ClasseProgetto.Domain_progetto_questionario import ProgettoQuestionario, ProgettoQuestionarioDomanda
from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario
from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
from Classi.ClasseQuestionario.Domain_gruppo_risposta import GruppoRisposta
from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda
import logging

class RepositoryProgettoQuestionario:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def associate_questionario(self, id_progetto, id_questionario, domande_gruppo_list):
        """
        domande_gruppo_list = list of dict: [{'id_domanda':1,'id_gruppo_risposta':2}, ...]
        """
        session = self.Session()
        try:
            # Creo l'associazione progetto-questionario
            pq = ProgettoQuestionario(id_progetto=id_progetto, id_questionario=id_questionario)
            session.add(pq)
            session.flush()  # per avere pq.id

            # Creo tutte le righe progetto_questionario_domanda
            for dg in domande_gruppo_list:
                pqd = ProgettoQuestionarioDomanda(
                    id_progetto_questionario=pq.id,
                    id_domanda=dg['id_domanda'],
                    id_gruppo_risposta=dg['id_gruppo_risposta']
                )
                session.add(pqd)

            session.commit()
            logging.info(f"Questionario {id_questionario} associato al progetto {id_progetto} con {len(domande_gruppo_list)} domande.")
            return pq
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'associazione questionario-progetto: {str(e)}")
            raise
        finally:
            session.close()

