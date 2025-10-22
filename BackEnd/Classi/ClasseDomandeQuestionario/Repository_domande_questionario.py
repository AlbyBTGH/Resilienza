# Classi/ClasseDomandeQuestionario/Repository_domande_questionario.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
from sqlalchemy import select, and_

class RepositoryDomandeQuestionario:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def get_domande_by_questionario(self, id_questionario):
        """
        Ritorna lista di tuple (id_domanda, id_gruppo_risposta)
        """
        session = self.Session()
        try:
            query = """
                SELECT dq.ID_DOMANDA, d.ID_GRUPPO_RISPOSTA
                FROM domande_questionario dq
                JOIN domande d ON dq.ID_DOMANDA = d.ID
                WHERE dq.ID_QUESTIONARIO = :idq
            """
            result = session.execute(query, {'idq': id_questionario}).fetchall()
            return [{"id_domanda": r[0], "id_gruppo_risposta": r[1]} for r in result]
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()