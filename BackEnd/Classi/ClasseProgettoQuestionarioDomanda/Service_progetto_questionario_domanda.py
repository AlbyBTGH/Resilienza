# Classi\ClasseProgettoQuestionarioDomanda\Service_progetto_questionario_domanda.py
# -*- coding: utf-8 -*-
import logging
from Classi.ClasseProgettoQuestionarioDomanda.Repository_progetto_questionario_domanda import RepositoryProgettoQuestionarioDomanda

class ServiceProgettoQuestionarioDomanda:
    def __init__(self):
        self.repository = RepositoryProgettoQuestionarioDomanda()

    def get_domande_associazione(self, id_progetto_questionario):
        """
        Restituisce lista di domande associate a un progetto-questionario
        """
        try:
            domande = self.repository.get_domande_by_progetto_questionario(id_progetto_questionario)
            return [
                {
                    "id": d.id,
                    "id_domanda": d.id_domanda,
                    "id_gruppo_risposta": d.id_gruppo_risposta
                }
                for d in domande
            ]
        except Exception as e:
            logging.error(f"Errore nel service get_domande_associazione: {str(e)}")
            return []