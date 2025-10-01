# Classi/ClasseAnagrafica/ClasseStatoProgetto/Service_t_stato_progetto.py
# -*- coding: utf-8 -*-
import logging
from .Repository_t_stato_progetto import Repository_t_stato_progetto
from .Domain_t_stato_progetto import TStatoProgetto
from datetime import datetime

class Service_t_stato_progetto:
    def __init__(self):
        self.repository = Repository_t_stato_progetto()

    def create_table_if_not_exists(self):
        self.repository.create_table_if_not_exists()
        
    def _to_dict(self, stato: TStatoProgetto):
        if stato is None:
            return None
        return {
            'id': stato.id,
            'descr': stato.descr,
            'nota': stato.nota,
            'data_ultima_modifica': stato.data_ultima_modifica.isoformat() if isinstance(stato.data_ultima_modifica, datetime) else stato.data_ultima_modifica,
            'modificato_da': stato.modificato_da,
        }

    def get_all_stati(self):
        try:
            stati = self.repository.get_all()
            logging.info(f"Recuperati {len(stati)} stati progetto.")
            return [self._to_dict(s) for s in stati]
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero di tutti gli stati: {str(e)}")
            return []