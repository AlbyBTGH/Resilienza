# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseGruppoRisposta/Controller_t_gruppo_risposta.py

from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Service_t_gruppo_risposta import Service_t_gruppo_risposta
import logging
from datetime import datetime

# Inizializzazione del Blueprint per il controller GruppoRisposta
t_gruppo_risposta_controller = Blueprint('gruppo_risposta', __name__)
service_t_gruppo_risposta = Service_t_gruppo_risposta()

# Funzione helper per formattare le date in modo sicuro
def format_date_for_json(date_value):
    """
    Formatta un oggetto datetime o una stringa in una stringa ISO 8601.
    Se � gi� una stringa, la restituisce cos� com'�.
    """
    if isinstance(date_value, datetime):
        return date_value.isoformat()
    elif isinstance(date_value, str):
        return date_value
    return None

@t_gruppo_risposta_controller.route("/", methods=['GET'])
def get_all_gruppi_risposta():
    """
    API per recuperare tutti i gruppi di risposta.
    """
    logging.info("Richiesta GET per tutti i gruppi di risposta.")
    try:
        gruppi = service_t_gruppo_risposta.get_all_gruppi_risposta()
        logging.info(f"Recuperati {len(gruppi)} gruppi di risposta dal servizio.")
        
        gruppi_data = []
        for gruppo in gruppi:
            gruppi_data.append({
                'id': gruppo['id'] if isinstance(gruppo, dict) else gruppo.id,
                'descr': gruppo['descr'] if isinstance(gruppo, dict) else gruppo.descr,
                'data_ultima_modifica': format_date_for_json(
                    gruppo['data_ultima_modifica'] if isinstance(gruppo, dict) else gruppo.data_ultima_modifica
                ),
                'modificato_da': gruppo['modificato_da'] if isinstance(gruppo, dict) else gruppo.modificato_da
            })
        
        return jsonify(gruppi_data), 200
    except Exception as e:
        logging.error(f"Errore nel recupero dei gruppi di risposta (Controller): {e}")
        return jsonify({"error": f"Errore interno del server nel recupero dei gruppi di risposta: {str(e)}"}), 500

@t_gruppo_risposta_controller.route("/<int:gruppo_id>", methods=['GET'])
def get_gruppo_risposta_by_id(gruppo_id: int):
    """
    API per recuperare un gruppo di risposta tramite ID.
    """
    logging.info(f"Richiesta GET per gruppo di risposta con ID: {gruppo_id}")
    gruppo = service_t_gruppo_risposta.get_gruppo_risposta_by_id(gruppo_id)
    if gruppo:
        gruppo_data = {
            'id': gruppo['id'] if isinstance(gruppo, dict) else gruppo.id,
            'descr': gruppo['descr'] if isinstance(gruppo, dict) else gruppo.descr,
            'data_ultima_modifica': format_date_for_json(
                gruppo['data_ultima_modifica'] if isinstance(gruppo, dict) else gruppo.data_ultima_modifica
            ),
            'modificato_da': gruppo['modificato_da'] if isinstance(gruppo, dict) else gruppo.modificato_da
        }
        return jsonify(gruppo_data), 200
    else:
        return jsonify({"error": "Gruppo di risposta non trovato."}), 404

@t_gruppo_risposta_controller.route("/", methods=['POST'])
def create_gruppo_risposta():
    """
    API per creare un nuovo gruppo di risposta.
    Richiede 'descr' nel corpo della richiesta JSON.
    Recupera 'creato_da' dalla sessione dell'utente loggato.
    """
    data = request.get_json()
    descr = data.get('descr')
    
    creato_da = session.get('username', 'Sistema')

    if not descr:
        logging.warning("Tentativo di creare gruppo di risposta con descrizione mancante.")
        return jsonify({"error": "Descrizione � obbligatoria."}), 400

    logging.info(f"Richiesta POST per creare gruppo di risposta con descrizione: {descr}")
    result_obj, status_code = service_t_gruppo_risposta.create_gruppo_risposta(descr, creato_da)
    
    if status_code == 201 and result_obj:
        return jsonify({
            'id': result_obj['id'] if isinstance(result_obj, dict) else result_obj.id,
            'descr': result_obj['descr'] if isinstance(result_obj, dict) else result_obj.descr,
            'data_ultima_modifica': format_date_for_json(
                result_obj['data_ultima_modifica'] if isinstance(result_obj, dict) else result_obj.data_ultima_modifica
            ),
            'modificato_da': result_obj['modificato_da'] if isinstance(result_obj, dict) else result_obj.modificato_da
        }), status_code
    else:
        return jsonify(result_obj), status_code

@t_gruppo_risposta_controller.route("/<int:gruppo_id>", methods=['PUT'])
def update_gruppo_risposta(gruppo_id: int):
    """
    API per aggiornare la descrizione di un gruppo di risposta esistente.
    Richiede 'descr' nel corpo della richiesta JSON.
    Recupera 'modificato_da' dalla sessione dell'utente loggato.
    """
    data = request.get_json()
    descr = data.get('descr')

    modificato_da = session.get('username', 'Sistema')

    if not descr:
        logging.warning(f"Tentativo di aggiornare gruppo di risposta {gruppo_id} con descrizione mancante.")
        return jsonify({"error": "Descrizione � obbligatoria."}), 400

    logging.info(f"Richiesta PUT per aggiornare gruppo di risposta con ID: {gruppo_id}")
    result_obj, status_code = service_t_gruppo_risposta.update_gruppo_risposta(gruppo_id, descr, modificato_da)
    
    if status_code == 200 and result_obj:
        return jsonify({
            'id': result_obj['id'] if isinstance(result_obj, dict) else result_obj.id,
            'descr': result_obj['descr'] if isinstance(result_obj, dict) else result_obj.descr,
            'data_ultima_modifica': format_date_for_json(
                result_obj['data_ultima_modifica'] if isinstance(result_obj, dict) else result_obj.data_ultima_modifica
            ),
            'modificato_da': result_obj['modificato_da'] if isinstance(result_obj, dict) else result_obj.modificato_da
        }), status_code
    else:
        return jsonify(result_obj), status_code

@t_gruppo_risposta_controller.route("/<int:gruppo_id>", methods=['DELETE'])
def delete_gruppo_risposta(gruppo_id: int):
    """
    API per eliminare fisicamente un gruppo di risposta.
    """
    logging.info(f"Richiesta DELETE per gruppo di risposta con ID: {gruppo_id}")
    result, status_code = service_t_gruppo_risposta.delete_gruppo_risposta(gruppo_id)
    return jsonify(result), status_code

