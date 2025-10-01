# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseRisposta/Service_t_risposta.py

import logging
from Classi.ClasseAnagrafica.ClasseRisposta.Repository_t_risposta import Repository_t_risposta
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Repository_t_gruppo_risposta import Repository_t_gruppo_risposta
from datetime import datetime

class Service_t_risposta:
    def __init__(self):
        self.repository = Repository_t_risposta()
        self.gruppo_repository = Repository_t_gruppo_risposta()

    def create_table_if_not_exists(self):
        self.repository.create_table_if_not_exists()

    def _to_dict(self, risposta):
        """
        Converte un oggetto TRisposta in un dizionario serializzabile.
        """
        if not risposta:
            return None
        
        gruppi_ids = [g.id for g in risposta.gruppi_risposta] if risposta.gruppi_risposta else []
        gruppi_desc = [g.descr for g in risposta.gruppi_risposta] if risposta.gruppi_risposta else []

        return {
            'id': risposta.id,
            'descr': risposta.descr,
            'gruppi_risposta_ids': gruppi_ids,
            'gruppi_risposta_descr': gruppi_desc,
            'peso': float(risposta.peso),
            'modificato_da': risposta.modificato_da,
            'data_ultima_modifica': risposta.data_ultima_modifica.isoformat() if isinstance(risposta.data_ultima_modifica, datetime) else str(risposta.data_ultima_modifica)
        }

    def get_all_risposte(self):
        """
        Recupera tutte le risposte dal database e le formatta per l'API.
        """
        try:
            risposte = self.repository.get_all()
            risposte_formattate = [self._to_dict(r) for r in risposte]
            logging.info(f"Recuperate {len(risposte_formattate)} risposte.")
            return risposte_formattate
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero di tutte le risposte: {str(e)}")
            return []

    def get_risposta_by_id(self, risposta_id: int):
        try:
            risposta = self.repository.get_by_id(risposta_id)
            if risposta:
                return self._to_dict(risposta)
            return None
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero della risposta con ID {risposta_id}: {str(e)}")
            return None

    def create_risposta(self, descr: str, gruppi_risposta_ids: list[int], peso: float):
        """
        Crea una nuova risposta dopo aver validato i dati.
        """
        try:
            if not self.gruppo_repository.check_gruppi_risposta_exist(gruppi_risposta_ids):
                return {"error": "Uno o più gruppi di risposta forniti non esistono."}, 400

            new_risposta = self.repository.create(descr, gruppi_risposta_ids, peso)
            
            if new_risposta:
                logging.info(f"Risposta con ID {new_risposta.id} creata con successo.")
                return self._to_dict(new_risposta), 201
            else:
                return {"error": "Errore durante la creazione della risposta."}, 500
        except Exception as e:
            logging.error(f"Errore nel servizio durante la creazione della risposta: {str(e)}")
            return {"error": f"Errore durante la creazione della risposta: {str(e)}"}, 500

    def update_risposta(self, risposta_id: int, descr: str, gruppi_risposta_ids: list[int], peso: float, modificato_da: str):
        """
        Aggiorna una risposta esistente.
        """
        try:
            if not self.gruppo_repository.check_gruppi_risposta_exist(gruppi_risposta_ids):
                return {"error": "Uno o più gruppi di risposta forniti non esistono."}, 400

            updated_risposta = self.repository.update(risposta_id, descr, gruppi_risposta_ids, peso, modificato_da)
            if updated_risposta:
                logging.info(f"Risposta con ID {risposta_id} aggiornata con successo.")
                return self._to_dict(updated_risposta), 200
            else:
                logging.warning(f"Tentativo di aggiornare risposta con ID {risposta_id} non trovata.")
                return {"error": "Risposta non trovata."}, 404
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'aggiornamento della risposta con ID {risposta_id}: {str(e)}")
            return {"error": f"Errore durante l'aggiornamento della risposta: {str(e)}"}, 500

    def delete_risposta(self, risposta_id: int):
        try:
            success = self.repository.delete(risposta_id)
            if success:
                logging.info(f"Risposta con ID {risposta_id} eliminata con successo.")
                return {"message": "Risposta eliminata con successo."}, 200
            else:
                logging.warning(f"Tentativo di eliminare risposta con ID {risposta_id} non trovata.")
                return {"error": "Risposta non trovata."}, 404
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'eliminazione della risposta con ID {risposta_id}: {str(e)}")
            return {"error": f"Errore durante l'eliminazione della risposta: {str(e)}"}, 500