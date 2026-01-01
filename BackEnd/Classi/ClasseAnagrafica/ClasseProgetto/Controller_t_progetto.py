# Classi/ClasseAnagrafica/ClasseProgetto/Controller_t_progetto.py
# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseProgetto.Service_t_progetto import Service_t_progetto
import logging
from datetime import datetime, date

t_progetto_controller = Blueprint('progetto', __name__)
service_t_progetto = Service_t_progetto()


def format_date_for_json(date_value):
    if isinstance(date_value, (datetime, date)):
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
    progetto, status_code = service_t_progetto.get_progetto_by_id(progetto_id)
    return jsonify(progetto), status_code


@t_progetto_controller.route("/", methods=['POST'])
def create_progetto():
    """
    API per creare un nuovo progetto.
    """
    data = request.json
    descr = data.get('descr')
    dt_inizio = data.get('dt_inizio')
    dt_fine = data.get('dt_fine')
    id_stato = data.get('id_stato')
    id_ambito = data.get('id_ambito')
    id_cliente = data.get('id_cliente')
    ref_cliente = data.get('ref_cliente')  # <-- campo aggiunto
    creato_da = session.get('username', 'Sistema')

    try:
        id_stato = int(id_stato) if id_stato else None
        id_ambito = int(id_ambito) if id_ambito else None
        id_cliente = int(id_cliente) if id_cliente else None
    except (ValueError, TypeError):
        return jsonify({"error": "ID Stato, ID Ambito o ID Cliente non validi."}), 400

    logging.info(f"Richiesta POST per creare progetto: {descr} da {creato_da}")

    # Passiamo ref_cliente al Service
    result_obj, status_code = service_t_progetto.create_progetto(
        descr, dt_inizio, dt_fine, id_stato, id_ambito, id_cliente, ref_cliente, creato_da
    )
    return jsonify(result_obj), status_code


@t_progetto_controller.route("/<int:progetto_id>/progetto_analisti", methods=['PUT'])
def sync_progetto_analisti(progetto_id):
    """
    Gestisce la sincronizzazione della lista di analisti associati a un progetto.
    Utilizza il nuovo endpoint /<id>/progetto_analisti.
    """
    try:
        # 1. Recupera i dati dalla richiesta
        data = request.get_json()
        
        # 2. Estrazione e Validazione input
        analisti_ids = data.get('analisti_ids', [])
        # Recupera l'utente che effettua la modifica dalla sessione/token
        modificato_da = session.get('username', 'Sistema') 

        if not modificato_da:
             return jsonify({"error": "Impossibile identificare l'utente modificante. Sessione scaduta?"}), 401

        # Assicurati che analisti_ids sia una lista di interi
        if not isinstance(analisti_ids, list):
            return jsonify({"error": "Il campo 'analisti_ids' deve essere una lista di ID interi."}), 400
            
        # 3. Chiama il Service per eseguire la sincronizzazione
        response, status_code = service_t_progetto.sync_analisti_progetto(
            progetto_id=progetto_id,
            analisti_ids=analisti_ids,
            modificato_da=modificato_da
        )

        return jsonify(response), status_code

    except Exception as e:
        import logging
        logging.error(f"Errore nel Controller sync_progetto_analisti per ID {progetto_id}: {str(e)}")
        # Restituisce un errore 500 generico per evitare di esporre dettagli di implementazione
        return jsonify({"error": f"Errore interno del server durante la sincronizzazione degli analisti."}), 500


@t_progetto_controller.route("/<int:progetto_id>", methods=['PUT'])
def update_progetto(progetto_id):
    data = request.json
    descr = data.get('descr')
    dt_inizio = data.get('dt_inizio')
    dt_fine = data.get('dt_fine')
    id_stato = data.get('id_stato')
    id_ambito = data.get('id_ambito')
    id_cliente = data.get('id_cliente')
    ref_cliente = data.get('ref_cliente')  # <-- campo aggiunto
    modificato_da = session.get('username', 'Sistema')

    try:
        id_stato = int(id_stato) if id_stato else None
        id_ambito = int(id_ambito) if id_ambito else None
        id_cliente = int(id_cliente) if id_cliente else None
    except (ValueError, TypeError):
        return jsonify({"error": "ID Stato, ID Ambito o ID Cliente non validi."}), 400

    logging.info(f"Richiesta PUT per aggiornare progetto con ID: {progetto_id} da {modificato_da}")

    # Passiamo ref_cliente al Service
    result_obj, status_code = service_t_progetto.update_progetto(
        progetto_id, descr, dt_inizio, dt_fine, id_stato, id_ambito, id_cliente, ref_cliente, modificato_da
    )
    return jsonify(result_obj), status_code


@t_progetto_controller.route("/<int:progetto_id>", methods=['DELETE'])
def delete_progetto(progetto_id):
    result_obj, status_code = service_t_progetto.delete_progetto(progetto_id)
    return jsonify(result_obj), status_code