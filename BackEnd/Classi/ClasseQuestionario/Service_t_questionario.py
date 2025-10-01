# Classi/ClasseQuestionario/Service_t_questionario.py
# -*- coding: utf-8 -*-
import logging
from Classi.ClasseQuestionario.Repository_t_questionario import Repository_t_questionario
from Classi.ClasseQuestionario.Domain_t_questionario import TQuestionario
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class Service_t_questionario:
    def __init__(self):
        self.repository = Repository_t_questionario()

    def _to_dict(self, questionario: TQuestionario):
        if questionario is None:
            return None
        return {
            'id': questionario.id,
            'descr': questionario.descr,
            'data_creazione': questionario.data_creazione.isoformat() if questionario.data_creazione else None,
            'creato_da': questionario.creato_da,
            'data_ultima_modifica': questionario.data_ultima_modifica.isoformat() if questionario.data_ultima_modifica else None,
            'modificato_da': questionario.modificato_da,
            'domande': [{'id': d.id, 'descr': d.descr} for d in questionario.domande]
        }

    def get_all_questionari(self):
        try:
            questionari = self.repository.get_all()
            return [self._to_dict(q) for q in questionari], 200
        except Exception as e:
            logging.error(f"Errore nel servizio durante la lettura dei questionari: {str(e)}")
            return {"error": "Errore interno del server"}, 500
    
    # Metodo per la creazione del questionario
    def create_questionario(self, descr: str, domande_ids: list, creato_da: str):
        try:
            questionario_creato = self.repository.create(descr, creato_da, domande_ids)
            
            if questionario_creato:
                return self._to_dict(questionario_creato), 201
            else:
                return {"error": "Creazione del questionario fallita."}, 500
        except IntegrityError:
            logging.error("Violazione di integrita: Assicurati che le domande esistano.")
            return {"error": "Violazione di integrita. Assicurati che le domande esistano."}, 409
        except SQLAlchemyError as e:
            logging.error(f"Errore di SQLAlchemy durante la creazione del questionario: {str(e)}")
            return {"error": "Errore interno del server durante la creazione del questionario."}, 500
        except Exception as e:
            logging.error(f"Errore nel servizio durante la creazione del questionario: {str(e)}")
            return {"error": f"Errore durante la creazione del questionario: {str(e)}"}, 500
            
    def update_questionario(self, questionario_id, descr, modificato_da, domande_ids):
        try:
            updated_questionario = self.repository.update(questionario_id, descr, modificato_da, domande_ids)
            if updated_questionario:
                return self._to_dict(updated_questionario), 200
            else:
                return {"error": "Questionario non trovato."}, 404
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'aggiornamento del questionario: {str(e)}")
            return {"error": f"Errore durante l'aggiornamento del questionario: {str(e)}"}, 500

    def delete_questionario(self, questionario_id: int):
        try:
            success = self.repository.delete(questionario_id)
            if success:
                return {"message": "Questionario eliminato con successo."}, 200
            else:
                return {"error": "Questionario non trovato."}, 404
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'eliminazione del questionario con ID {questionario_id}: {str(e)}")
            return {"error": f"Errore durante la cancellazione del questionario: {str(e)}"}, 500