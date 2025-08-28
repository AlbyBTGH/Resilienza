# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDomanda/Controller_t_domanda.py

from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseDomanda.Service_t_domanda import Service_t_domanda
from Classi.ClasseAnagrafica.ClasseDriver.Service_t_driver import Service_t_driver # Per recuperare i driver per il dropdown
import logging
from datetime import datetime

# Inizializzazione del Blueprint per il controller Domanda
t_domanda_controller = Blueprint('domanda', __name__)
service_t_domanda = Service_t_domanda()
service_t_driver = Service_t_driver() # Per caricare i driver nel frontend

# Funzione helper per formattare le date in modo sicuro
def format_date_for_json(date_value):
    """
    Formatta un oggetto datetime o una stringa in una stringa ISO 8601.
    Se è già una stringa, la restituisce così com'è.
    """
    if isinstance(date_value, datetime):
        return date_value.isoformat()
    elif isinstance(date_value, str):
        return date_value
    return None

@t_domanda_controller.route("/", methods=['GET'])
def get_all_domande():
    """
    API per recuperare tutte le domande con i dettagli del driver.
    Supporta il filtro opzionale per id_driver.
    """
    logging.info("Richiesta GET per domande.")
    try:
        # Modifica qui: Recupera il parametro 'id_driver' dalla query string
        id_driver_filter = request.args.get('id_driver', type=int)
        
        if id_driver_filter:
            logging.info(f"Filtro driver applicato: {id_driver_filter}")
        else:
            logging.info("Nessun filtro driver, recupero tutte le domande.")
        
        domande = service_t_domanda.get_all_domande(id_driver_filter)
        
        # Formatta i dati per la risposta JSON
        domande_data = []
        for domanda in domande:
            domande_data.append({
                'id': domanda['id'],
                'descr': domanda['descr'],
                'id_driver': domanda['id_driver'],
                'driver_descr': domanda.get('driver_descr', ''), # Assicurati che driver_descr sia presente
                'data_ultima_modifica': format_date_for_json(domanda['data_ultima_modifica']),
                'modificato_da': domanda['modificato_da']
            })
        return jsonify(domande_data), 200
    except Exception as e:
        logging.error(f"Errore nel controller durante il recupero di tutte le domande: {str(e)}")
        return jsonify({"error": "Errore nel recupero delle domande."}), 500

@t_domanda_controller.route("/<int:domanda_id>", methods=['GET'])
def get_domanda_by_id(domanda_id: int):
    """
    API per recuperare una domanda tramite ID.
    """
    logging.info(f"Richiesta GET per domanda con ID: {domanda_id}")
    try:
        domanda = service_t_domanda.get_domanda_by_id(domanda_id)
        if domanda:
            return jsonify({
                'id': domanda['id'],
                'descr': domanda['descr'],
                'id_driver': domanda['id_driver'],
                'data_ultima_modifica': format_date_for_json(domanda['data_ultima_modifica']),
                'modificato_da': domanda['modificato_da']
            }), 200
        else:
            return jsonify({"error": "Domanda non trovata."}), 404
    except Exception as e:
        logging.error(f"Errore nel recupero della domanda con ID {domanda_id}: {str(e)}")
        return jsonify({"error": "Errore nel recupero della domanda."}), 500

@t_domanda_controller.route("/", methods=['POST'])
def create_domanda():
    """
    API per creare una nuova domanda.
    """
    logging.info("Richiesta POST per creare una nuova domanda.")
    data = request.json
    descr = data.get('descr')
    id_driver = data.get('id_driver')
    creato_da = session.get('username', 'system') # Recupera l'utente dalla sessione

    if not descr or not id_driver:
        logging.warning("Descrizione o ID Driver mancante.")
        return jsonify({"error": "Descrizione e ID Driver sono obbligatori."}), 400

    result_obj, status_code = service_t_domanda.create_domanda(descr, id_driver, creato_da)
    
    if status_code == 201 and result_obj:
        return jsonify({
            'id': result_obj['id'],
            'descr': result_obj['descr'],
            'id_driver': result_obj['id_driver'],
            'data_ultima_modifica': format_date_for_json(result_obj['data_ultima_modifica']),
            'modificato_da': result_obj['modificato_da']
        }), status_code
    else:
        return jsonify(result_obj), status_code

@t_domanda_controller.route("/<int:domanda_id>", methods=['PUT'])
def update_domanda(domanda_id: int):
    """
    API per aggiornare una domanda esistente.
    """
    logging.info(f"Richiesta PUT per aggiornare domanda con ID: {domanda_id}")
    data = request.json
    descr = data.get('descr')
    id_driver = data.get('id_driver')
    modificato_da = session.get('username', 'system') # Recupera l'utente dalla sessione

    if not descr or not id_driver:
        logging.warning("Descrizione o ID Driver mancante.")
        return jsonify({"error": "Descrizione e ID Driver sono obbligatori."}), 400

    result_obj, status_code = service_t_domanda.update_domanda(domanda_id, descr, id_driver, modificato_da)
    
    if status_code == 200 and result_obj:
        return jsonify({
            'id': result_obj['id'],
            'descr': result_obj['descr'],
            'id_driver': result_obj['id_driver'],
            'data_ultima_modifica': format_date_for_json(result_obj['data_ultima_modifica']),
            'modificato_da': result_obj['modificato_da']
        }), status_code
    else:
        return jsonify(result_obj), status_code

@t_domanda_controller.route("/<int:domanda_id>", methods=['DELETE'])
def delete_domanda(domanda_id: int):
    """
    API per eliminare fisicamente una domanda.
    """
    logging.info(f"Richiesta DELETE per domanda con ID: {domanda_id}")
    result, status_code = service_t_domanda.delete_domanda(domanda_id)
    return jsonify(result), status_code

# Endpoint per recuperare tutti i driver (per il dropdown nel frontend)
@t_domanda_controller.route("/drivers", methods=['GET'])
def get_drivers_for_dropdown():
    """
    API per recuperare tutti i driver, utilizzata per popolare un dropdown.
    """
    logging.info("Richiesta GET per driver per dropdown domande.")
    try:
        drivers = service_t_driver.get_all_drivers()
        # Assicurati che service_t_driver.get_all_drivers() restituisca oggetti con 'id' e 'descr'
        drivers_data = [{'id': driver['id'], 'descr': driver['descr']} for driver in drivers]
        logging.info(f"Recuperati {len(drivers_data)} driver.") # Aggiunto log per i driver recuperati
        return jsonify(drivers_data), 200
    except Exception as e:
        logging.error(f"Errore nel recupero dei driver per dropdown: {str(e)}")
        return jsonify({"error": "Errore nel recupero dei driver."}), 500
