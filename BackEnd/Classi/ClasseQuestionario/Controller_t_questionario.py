# Classi/ClasseQuestionario/Controller_t_questionario.py
# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, session
from Classi.ClasseQuestionario.Service_t_questionario import Service_t_questionario
import logging

t_questionario_controller = Blueprint('questionario', __name__)
service_t_questionario = Service_t_questionario()

@t_questionario_controller.route("/", methods=['GET'])
def get_all_questionari():
    logging.info("Richiesta GET per tutti i questionari.")
    try:
        questionari, status_code = service_t_questionario.get_all_questionari()
        return jsonify(questionari), status_code
    except Exception as e:
        logging.error(f"Errore nella richiesta GET per i questionari: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500

@t_questionario_controller.route("/<int:questionario_id>", methods=['PUT'])
def update_questionario(questionario_id):
    data = request.json
    descr = data.get('descr')
    domande_ids = data.get('domande', [])
    modificato_da = data.get('modificato_da', 'Utente Sconosciuto')
    
    result, status_code = service_t_questionario.update_questionario(questionario_id, descr, modificato_da, domande_ids)
    return jsonify(result), status_code

@t_questionario_controller.route("/<int:questionario_id>", methods=['DELETE'])
def delete_questionario(questionario_id):
    result, status_code = service_t_questionario.delete_questionario(questionario_id)
    return jsonify(result), status_code

@t_questionario_controller.route("/", methods=['POST'])
def create_questionario():
    logging.info("Richiesta POST per la creazione di un questionario.")
    data = request.json
    
    # Debug: Stampa i dati ricevuti dalla richiesta
    logging.info(f"Dati ricevuti per la creazione del questionario: {data}")

    # Estrai i dati dal body della richiesta
    descr = data.get('descr') if data else None
    domande_ids = data.get('domande') if data else None
    creato_da = data.get('creato_da') if data else None

    # Esegui la validazione dei dati
    if not descr or not domande_ids:
        # Debug: Stampa un messaggio specifico in caso di errore
        logging.error(f"Validazione fallita: descr='{descr}', domande_ids='{domande_ids}'")
        return jsonify({"error": "Descrizione e domande sono campi obbligatori."}), 400

    try:
        # Chiama il service per creare il questionario
        result, status_code = service_t_questionario.create_questionario(descr, domande_ids, creato_da)
        return jsonify(result), status_code
    except Exception as e:
        logging.error(f"Errore nella creazione del questionario: {str(e)}")
        return jsonify({"error": "Errore interno del server durante la creazione del questionario."}), 500