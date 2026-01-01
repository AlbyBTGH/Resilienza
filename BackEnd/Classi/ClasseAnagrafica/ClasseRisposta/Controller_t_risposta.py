# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseRisposta/Controller_t_risposta.py

from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseRisposta.Service_t_risposta import Service_t_risposta
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Service_t_gruppo_risposta import Service_t_gruppo_risposta
import logging
from datetime import datetime

# Inizializzazione del Blueprint per il controller Risposta
t_risposta_controller = Blueprint('risposta', __name__)
service_t_risposta = Service_t_risposta()
service_t_gruppo_risposta = Service_t_gruppo_risposta()

@t_risposta_controller.route("/", methods=['GET'])
def get_all_risposte():
    logging.info("Richiesta GET per tutte le risposte.")
    try:
        risposte_formattate = service_t_risposta.get_all_risposte()
        logging.info(f"Recuperate {len(risposte_formattate)} risposte.")
        return jsonify(risposte_formattate), 200
    except Exception as e:
        logging.error(f"Errore nella richiesta GET per le risposte: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500

@t_risposta_controller.route("/<int:risposta_id>", methods=['GET'])
def get_risposta_by_id(risposta_id):
    logging.info(f"Richiesta GET per la risposta con ID: {risposta_id}")
    risposta = service_t_risposta.get_risposta_by_id(risposta_id)
    if risposta:
        return jsonify(risposta), 200
    return jsonify({"error": "Risposta non trovata"}), 404

@t_risposta_controller.route("/", methods=['POST'])
def create_risposta():
    logging.info("Richiesta POST per creare una nuova risposta.")
    data = request.get_json()
    descr = data.get('descr')
    gruppi_risposta_ids = data.get('gruppi_risposta_ids', [])
    peso = data.get('peso')
    # modificato_da = data.get('modificato_da')
    modificato_da = session.get('username', 'Sistema')

    if not descr:
        return jsonify({"error": "Descrizione è obbligatoria."}), 400

    try:
        new_risposta_dict, status_code = service_t_risposta.create_risposta(descr, gruppi_risposta_ids, peso, modificato_da)
        return jsonify(new_risposta_dict), status_code
    except Exception as e:
        logging.error(f"Errore nel controller durante la creazione della risposta: {str(e)}")
        return jsonify({"error": "Errore interno del server."}), 500

@t_risposta_controller.route("/<int:risposta_id>", methods=['PUT'])
def update_risposta(risposta_id):
    logging.info(f"Richiesta PUT per aggiornare risposta con ID: {risposta_id}")
    data = request.get_json()
    descr = data.get('descr')
    gruppi_risposta_ids = data.get('gruppi_risposta_ids', [])
    peso = data.get('peso')
    modificato_da = session.get('username', 'Sistema')

    if not descr:
        return jsonify({"error": "Descrizione è obbligatoria."}), 400

    try:
        updated_risposta_dict, status_code = service_t_risposta.update_risposta(risposta_id, descr, gruppi_risposta_ids, peso, modificato_da)
        return jsonify(updated_risposta_dict), status_code
    except Exception as e:
        logging.error(f"Errore nel controller durante l'aggiornamento della risposta: {str(e)}")
        return jsonify({"error": "Errore interno del server."}), 500

@t_risposta_controller.route("/<int:risposta_id>", methods=['DELETE'])
def delete_risposta(risposta_id):
    logging.info(f"Richiesta DELETE per eliminare risposta con ID: {risposta_id}")
    result_obj, status_code = service_t_risposta.delete_risposta(risposta_id)
    return jsonify(result_obj), status_code

@t_risposta_controller.route("/gruppi", methods=['GET'])
def get_gruppi_for_select():
    logging.info("Richiesta GET per recuperare tutti i gruppi per la select.")
    try:
        gruppi = service_t_gruppo_risposta.get_all_gruppi_risposta()
        logging.info(f"Recuperati {len(gruppi)} gruppi di risposta.")
        
        gruppi_formattati = []
        for gruppo in gruppi:
            if isinstance(gruppo, dict):
                gruppi_formattati.append({
                    'id': gruppo.get('id'),
                    'descr': gruppo.get('descr')
                })
            else:
                gruppi_formattati.append({
                    'id': gruppo.id,
                    'descr': gruppo.descr
                })

        return jsonify(gruppi_formattati), 200
    except Exception as e:
        logging.error(f"Errore nel controller durante il recupero dei gruppi di risposta: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500
