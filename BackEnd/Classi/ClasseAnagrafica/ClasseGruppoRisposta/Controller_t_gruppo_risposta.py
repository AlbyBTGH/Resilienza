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
    API per recuperare tutti i gruppi di risposta.
    """
    logging.info("Richiesta GET per tutti i gruppi di risposta.")
    try:
        # 1. Recupera la lista di oggetti (Model o Dict)
        gruppi = service_t_gruppo_risposta.get_all_gruppi_risposta()
        
        # 2. **CORREZIONE CHIAVE:** Serializza in modo sicuro.
        #    - Se 'gruppo' ha l'attributo 'to_dict', lo chiama.
        #    - ALTRIMENTI (se è un dict), usa l'oggetto così com'è.
        gruppi_serializzati = [
            gruppo.to_dict() if hasattr(gruppo, 'to_dict') else gruppo
            for gruppo in gruppi
        ] 
        
        # 3. Restituisce la risposta JSON
        return jsonify({'gruppi_risposta': gruppi_serializzati}), 200
        
    except Exception as e:
        # Gestione degli errori migliorata
        logging.error(f"ERRORE CRITICO in get_all_gruppi_risposta: {e}", exc_info=True)
        return jsonify({"error": "Errore interno del server"}), 500

@t_gruppo_risposta_controller.route("/", methods=['POST'])
def create_gruppo_risposta():
    """
    API per creare un nuovo gruppo di risposta.
    """
    data = request.get_json()
    descr = data.get('descr')
    creato_da = session.get('username', 'Sistema')

    if not descr:
        logging.warning("Tentativo di creare gruppo di risposta con descrizione mancante.")
        return jsonify({"error": "Descrizione è obbligatoria."}), 400

    logging.info(f"Richiesta POST per creare nuovo gruppo di risposta: {descr}")
    result, status_code = service_t_gruppo_risposta.create_gruppo_risposta(descr, creato_da)
    
    # Se il servizio restituisce un oggetto (non solo un messaggio di errore)
    if status_code == 201 and result and 'id' in result:
        # Assicurati di formattare correttamente la data nel dizionario restituito
        result['data_ultima_modifica'] = format_date_for_json(result.get('data_ultima_modifica'))
        return jsonify(result), status_code
    else:
        return jsonify(result), status_code


@t_gruppo_risposta_controller.route("/<int:gruppo_id>", methods=['GET'])
def get_gruppo_risposta_by_id(gruppo_id):
    """
    API per recuperare un gruppo di risposta specifico per ID.
    """
    logging.info(f"Richiesta GET per gruppo di risposta con ID: {gruppo_id}")
    gruppo = service_t_gruppo_risposta.get_gruppo_risposta_by_id(gruppo_id)
    
    if gruppo:
        # Usa il to_dict() del modello per la serializzazione
        gruppo_serializzato = gruppo.to_dict()
        return jsonify(gruppo_serializzato), 200
    else:
        logging.warning(f"Gruppo di risposta con ID {gruppo_id} non trovato.")
        return jsonify({"error": "Gruppo di risposta non trovato."}), 404

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
    # Il service deve restituire un dizionario compatibile con JSON o un oggetto con .to_dict()
    result_obj, status_code = service_t_gruppo_risposta.update_gruppo_risposta(gruppo_id, descr, modificato_da)
    
    if status_code == 200 and result_obj:
        # Serializzazione dell'oggetto restituito (sia che sia un dict che un oggetto SQLAlchemy)
        if isinstance(result_obj, dict):
            # Se il service restituisce un dizionario, assicurati che la data sia formattata
            result_obj['data_ultima_modifica'] = format_date_for_json(result_obj.get('data_ultima_modifica'))
            return jsonify(result_obj), status_code
        else:
            # Se il service restituisce l'oggetto Domain, usa il suo to_dict()
            return jsonify(result_obj.to_dict()), status_code
    else:
        return jsonify(result_obj), status_code

@t_gruppo_risposta_controller.route("/<int:gruppo_id>", methods=['DELETE'])
def delete_gruppo_risposta(gruppo_id):
    """
    API per eliminare un gruppo di risposta.
    """
    logging.info(f"Richiesta DELETE per gruppo di risposta con ID: {gruppo_id}")
    return service_t_gruppo_risposta.delete_gruppo_risposta(gruppo_id)