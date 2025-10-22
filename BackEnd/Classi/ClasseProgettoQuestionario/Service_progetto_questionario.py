# Classi/ClasseProgettoQuestionario/Service_progetto_questionario.py
# -*- coding: utf-8 -*-
import logging
from Classi.ClasseProgetto.Repository_progetto_questionario import RepositoryProgettoQuestionario

class ServiceProgettoQuestionario:
    def __init__(self):
        self.repository = RepositoryProgettoQuestionario()

    def associate_questionario(self, id_progetto, id_questionario, domande_gruppo_list):
        """
        domande_gruppo_list = list of dict: [{'id_domanda':1,'id_gruppo_risposta':2}, ...]
        """
        try:
            pq = self.repository.associate_questionario(id_progetto, id_questionario, domande_gruppo_list)
            return {"id": pq.id, "id_progetto": pq.id_progetto, "id_questionario": pq.id_questionario}, 201
        except Exception as e:
            logging.error(f"Errore nel service nell'associare questionario: {str(e)}")
            return {"error": "Errore interno"}, 500