# Classi/ClasseAnagrafica/ClasseProgetto/Controller_t_progetto.py
# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseProgetto.Service_t_progetto import Service_t_progetto
from Classi.ClasseAnagrafica.ClasseAmbito.Service_t_ambito import Service_t_ambito
import logging
from datetime import datetime

t_progetto_controller = Blueprint('progetto', __name__)
service_t_progetto = Service_t_progetto()
service_t_ambito = Service_t_ambito()

def format_date_for_json(date_value):
    if isinstance(date_value, datetime):
        return date_value.isoformat()
    elif isinstance(date_value, str):
        return date_value
    return None

@t_progetto_controller.route("/", methods=['GET'])
def get_all_progetti():
    logging.info("Richiesta GET per tutti i progetti.")
    try:
        progetti = service_t_progetto.get_all_progetti()
        logging.info(f"Recuperati {len(progetti)} progetti.")
        return jsonify(progetti), 200
    except Exception as e:
        logging.error(f"Errore nella richiesta GET per i progetti: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500

@t_progetto_controller.route("/<int:progetto_id>", methods=['GET'])
def get_progetto_by_id(progetto_id):
    logging.info(f"Richiesta GET per progetto con ID: {progetto_id}")
    progetto = service_t_progetto.get_progetto_by_id(progetto_id)
    if progetto:
        return jsonify(progetto), 200
    else:
        return jsonify({"error": "Progetto non trovato."}), 404

@t_progetto_controller.route("/", methods=['POST'])
def create_progetto():
    data = request.json
    descr = data.get('descr')
    dt_inizio = data.get('dt_inizio')
    dt_fine = data.get('dt_fine')
    id_stato = data.get('id_stato')
    id_ambito = data.get('id_ambito')
    ref_cliente = data.get('ref_cliente')
    modificato_da = data.get('modificato_da', 'Utente Sconosciuto')

    # Aggiunta la gestione dei valori nulli per i campi data e id_stato
    if not dt_inizio:
        dt_inizio = None
    if not dt_fine:
        dt_fine = None
    if not id_stato:
        id_stato = None

    result_obj, status_code = service_t_progetto.create_progetto(descr, dt_inizio, dt_fine, id_stato, id_ambito, ref_cliente, modificato_da)
    return jsonify(result_obj), status_code

@t_progetto_controller.route("/<int:progetto_id>", methods=['PUT'])
def update_progetto(progetto_id):
    data = request.json
    descr = data.get('descr')
    dt_inizio = data.get('dt_inizio')
    dt_fine = data.get('dt_fine')
    id_stato = data.get('id_stato')
    id_ambito = data.get('id_ambito')
    ref_cliente = data.get('ref_cliente')
    modificato_da = data.get('modificato_da', 'Utente Sconosciuto')

    if not dt_inizio:
        dt_inizio = None
    if not dt_fine:
        dt_fine = None
    if not id_stato:
        id_stato = None

    result_obj, status_code = service_t_progetto.update_progetto(progetto_id, descr, dt_inizio, dt_fine, id_stato, id_ambito, ref_cliente, modificato_da)
    return jsonify(result_obj), status_code

@t_progetto_controller.route("/<int:progetto_id>", methods=['DELETE'])
def delete_progetto(progetto_id):
    result_obj, status_code = service_t_progetto.delete_progetto(progetto_id)
    return jsonify(result_obj), status_code

@t_progetto_controller.route("/ambiti", methods=['GET'])
def get_ambiti_list():
    try:
        ambiti = service_t_ambito.get_all_ambiti()
        return jsonify(ambiti), 200
    except Exception as e:
        logging.error(f"Errore nel recupero della lista di ambiti: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500