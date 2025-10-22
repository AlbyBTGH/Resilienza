# Classi\ClasseProgettoQuestionarioDomanda\Repository_progetto_questionario_domanda.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda

class RepositoryProgettoQuestionarioDomanda:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def get_domande_by_progetto_questionario(self, id_progetto_questionario):
        session = self.Session()
        try:
            result = session.query(ProgettoQuestionarioDomanda).filter_by(
                id_progetto_questionario=id_progetto_questionario
            ).all()
            return result
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()