# Classi/ClasseAnagrafica/ClasseStatoProgetto/Controller_stati_progetto.py
# -*- coding: utf-8 -*-
import logging
from flask import Blueprint, jsonify
from .Service_t_stato_progetto import Service_t_stato_progetto

t_stato_progetto_controller = Blueprint('stati_progetto', __name__)
service_t_stato_progetto = Service_t_stato_progetto()

@t_stato_progetto_controller.route("/", methods=['GET'])
def get_all_stati():
    logging.info("Richiesta GET per tutti gli stati progetto.")
    try:
        stati = service_t_stato_progetto.get_all_stati()
        logging.info(f"Recuperati {len(stati)} stati.")
        return jsonify(stati), 200
    except Exception as e:
        logging.error(f"Errore nella richiesta GET per gli stati: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500