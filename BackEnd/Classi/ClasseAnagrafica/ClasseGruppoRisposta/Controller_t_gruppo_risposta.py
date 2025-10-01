# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseGruppoRisposta/Controller_t_gruppo_risposta.py

from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Service_t_gruppo_risposta import Service_t_gruppo_risposta
import logging
from datetime import datetime

# Inizializzazione del Blueprint per il controller GruppoRisposta
t_gruppo_risposta_controller = Blueprint('gruppo-risposta', __name__)
service_t_gruppo_risposta = Service_t_gruppo_risposta()

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

@t_gruppo_risposta_controller.route("/", methods=['GET'])
def get_all_gruppi_risposta():
    """
    API per recuperare tutti i gruppi di risposta, includendo le risposte associate.
    """
    logging.info("Richiesta GET per tutti i gruppi di risposta.")
    try:
        gruppi = service_t_gruppo_risposta.get_all_gruppi_risposta()
        gruppi_con_risposte = []
        for g in gruppi:
            risposte_associate = [
                {'id': r.id, 'descr': r.descr} for r in g.risposte
            ]
            gruppi_con_risposte.append({
                'id': g.id,
                'descr': g.descr,
                'modificato_da': g.modificato_da,
                'data_ultima_modifica': format_date_for_json(g.data_ultima_modifica),
                'risposte_associate': risposte_associate
            })
        
        return jsonify(gruppi_con_risposte), 200
    except Exception as e:
        logging.error(f"Errore nel controller durante il recupero dei gruppi di risposta: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500

@t_gruppo_risposta_controller.route("/<int:gruppo_id>", methods=['GET'])
def get_gruppo_risposta_by_id(gruppo_id):
    """
    API per recuperare un singolo gruppo di risposta per ID.
    """
    logging.info(f"Richiesta GET per gruppo di risposta con ID: {gruppo_id}")
    gruppo = service_t_gruppo_risposta.get_gruppo_risposta_by_id(gruppo_id)
    if gruppo:
        return jsonify({
            'id': gruppo.id,
            'descr': gruppo.descr,
            'modificato_da': gruppo.modificato_da,
            'data_ultima_modifica': format_date_for_json(gruppo.data_ultima_modifica)
        }), 200
    else:
        return jsonify({"error": "Gruppo di risposta non trovato."}), 404

@t_gruppo_risposta_controller.route("/", methods=['POST'])
def create_gruppo_risposta():
    """
    API per creare un nuovo gruppo di risposta.
    """
    data = request.get_json()
    descr = data.get('descr')
    modificato_da = session.get('username', 'Sistema')
    
    if not descr:
        logging.warning("Tentativo di creare un gruppo di risposta senza descrizione.")
        return jsonify({"error": "La descrizione è obbligatoria."}), 400

    logging.info("Richiesta POST per creare un nuovo gruppo di risposta.")
    result_obj, status_code = service_t_gruppo_risposta.create_gruppo_risposta(descr, modificato_da)
    
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
def update_gruppo_risposta(gruppo_id):
    """
    API per aggiornare un gruppo di risposta esistente.
    """
    data = request.get_json()
    descr = data.get('descr')
    modificato_da = session.get('username', 'Sistema')

    if not descr:
        logging.warning(f"Tentativo di aggiornare gruppo di risposta {gruppo_id} con descrizione mancante.")
        return jsonify({"error": "Descrizione è obbligatoria."}), 400

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
def delete_gruppo_risposta(gruppo_id):
    """
    API per eliminare un gruppo di risposta per ID.
    """
    logging.info(f"Richiesta DELETE per gruppo di risposta con ID: {gruppo_id}")
    result, status_code = service_t_gruppo_risposta.delete_gruppo_risposta(gruppo_id)
    return jsonify(result), status_code