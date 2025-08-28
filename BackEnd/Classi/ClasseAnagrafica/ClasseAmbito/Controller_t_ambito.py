# Classi/ClasseAnagrafica/ClasseAmbito/Controller_t_ambito.py
from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseAmbito.Service_t_ambito import Service_t_ambito
import logging
from datetime import datetime # Importa datetime per la serializzazione

# Inizializzazione del Blueprint per il controller Ambito
t_ambito_controller = Blueprint('ambito', __name__)
service_t_ambito = Service_t_ambito()

# Funzione helper per formattare le date in modo sicuro
def format_date_for_json(date_value):
    """
    Formatta un oggetto datetime o una stringa in una stringa ISO 8601.
    Se è già una stringa, la restituisce così com'è.
    """
    if isinstance(date_value, datetime):
        return date_value.isoformat()
    elif isinstance(date_value, str):
        return date_value # È già una stringa, la restituiamo così com'è
    return None # O un valore di default se preferisci, es. ''

@t_ambito_controller.route("/", methods=['GET'])
def get_all_ambiti():
    """
    API per recuperare tutti gli ambiti.
    """
    logging.info("Richiesta GET per tutti gli ambiti.")
    try:
        ambiti = service_t_ambito.get_all_ambiti()
        logging.info(f"Recuperati {len(ambiti)} ambiti dal servizio.")
        
        ambiti_data = []
        for ambito in ambiti:
            logging.debug(f"DEBUG Controller: Tipo di ambito nell'iterazione: {type(ambito)}")
            
            # Accesso ai dati come dizionario o attributo, e formattazione sicura della data
            ambiti_data.append({
                'id': ambito['id'] if isinstance(ambito, dict) else ambito.id,
                'codice': ambito['codice'] if isinstance(ambito, dict) else ambito.codice,
                'descrizione': ambito['descrizione'] if isinstance(ambito, dict) else ambito.descrizione,
                'note': ambito['note'] if isinstance(ambito, dict) else ambito.note,
                'data_ultima_modifica': format_date_for_json(
                    ambito['data_ultima_modifica'] if isinstance(ambito, dict) else ambito.data_ultima_modifica
                ),
                'modificato_da': ambito['modificato_da'] if isinstance(ambito, dict) else ambito.modificato_da
            })
        
        return jsonify(ambiti_data), 200
    except Exception as e:
        logging.error(f"Errore nel recupero degli ambiti (Controller): {e}")
        return jsonify({"error": f"Errore interno del server nel recupero degli ambiti: {str(e)}"}), 500

@t_ambito_controller.route("/<int:ambito_id>", methods=['GET'])
def get_ambito_by_id(ambito_id: int):
    """
    API per recuperare un ambito tramite ID.
    """
    logging.info(f"Richiesta GET per ambito con ID: {ambito_id}")
    ambito = service_t_ambito.get_ambito_by_id(ambito_id)
    if ambito:
        # Serializza l'oggetto TAmbito in un formato JSON
        ambito_data = {
            'id': ambito['id'] if isinstance(ambito, dict) else ambito.id,
            'codice': ambito['codice'] if isinstance(ambito, dict) else ambito.codice,
            'descrizione': ambito['descrizione'] if isinstance(ambito, dict) else ambito.descrizione,
            'note': ambito['note'] if isinstance(ambito, dict) else ambito.note,
            'data_ultima_modifica': format_date_for_json(
                ambito['data_ultima_modifica'] if isinstance(ambito, dict) else ambito.data_ultima_modifica
            ),
            'modificato_da': ambito['modificato_da'] if isinstance(ambito, dict) else ambito.modificato_da
        }
        return jsonify(ambito_data), 200
    else:
        return jsonify({"error": "Ambito non trovato."}), 404

@t_ambito_controller.route("/", methods=['POST'])
def create_ambito():
    """
    API per creare un nuovo ambito.
    Richiede 'codice', 'descrizione', 'note' (opzionale) nel corpo della richiesta JSON.
    Recupera 'modificato_da' dalla sessione dell'utente loggato.
    """
    data = request.get_json()
    codice = data.get('codice')
    descrizione = data.get('descrizione')
    note = data.get('note')
    
    modificato_da = session.get('username', 'Sistema')

    if not codice or not descrizione:
        logging.warning("Tentativo di creare ambito con dati mancanti (codice o descrizione).")
        return jsonify({"error": "Codice e descrizione sono obbligatori."}), 400

    logging.info(f"Richiesta POST per creare ambito con codice: {codice}")
    result_obj, status_code = service_t_ambito.create_ambito(codice, descrizione, note, modificato_da)
    
    if status_code == 201 and result_obj:
        return jsonify({
            'id': result_obj['id'] if isinstance(result_obj, dict) else result_obj.id,
            'codice': result_obj['codice'] if isinstance(result_obj, dict) else result_obj.codice,
            'descrizione': result_obj['descrizione'] if isinstance(result_obj, dict) else result_obj.descrizione,
            'note': result_obj['note'] if isinstance(result_obj, dict) else result_obj.note,
            'data_ultima_modifica': format_date_for_json(
                result_obj['data_ultima_modifica'] if isinstance(result_obj, dict) else result_obj.data_ultima_modifica
            ),
            'modificato_da': result_obj['modificato_da'] if isinstance(result_obj, dict) else result_obj.modificato_da
        }), status_code
    else:
        return jsonify(result_obj), status_code

@t_ambito_controller.route("/<int:ambito_id>", methods=['PUT'])
def update_ambito(ambito_id: int):
    """
    API per aggiornare la descrizione e le note di un ambito esistente.
    Richiede 'descrizione', 'note' (opzionale) nel corpo della richiesta JSON.
    Recupera 'modificato_da' dalla sessione dell'utente loggato.
    """
    data = request.get_json()
    descrizione = data.get('descrizione')
    note = data.get('note')

    modificato_da = session.get('username', 'Sistema')

    if not descrizione:
        logging.warning(f"Tentativo di aggiornare ambito {ambito_id} con descrizione mancante.")
        return jsonify({"error": "Descrizione è obbligatoria."}), 400

    logging.info(f"Richiesta PUT per aggiornare ambito con ID: {ambito_id}")
    result_obj, status_code = service_t_ambito.update_ambito(ambito_id, descrizione, note, modificato_da)
    
    if status_code == 200 and result_obj:
        return jsonify({
            'id': result_obj['id'] if isinstance(result_obj, dict) else result_obj.id,
            'codice': result_obj['codice'] if isinstance(result_obj, dict) else result_obj.codice,
            'descrizione': result_obj['descrizione'] if isinstance(result_obj, dict) else result_obj.descrizione,
            'note': result_obj['note'] if isinstance(result_obj, dict) else result_obj.note,
            'data_ultima_modifica': format_date_for_json(
                result_obj['data_ultima_modifica'] if isinstance(result_obj, dict) else result_obj.data_ultima_modifica
            ),
            'modificato_da': result_obj['modificato_da'] if isinstance(result_obj, dict) else result_obj.modificato_da
        }), status_code
    else:
        return jsonify(result_obj), status_code

@t_ambito_controller.route("/<int:ambito_id>", methods=['DELETE'])
def delete_ambito(ambito_id: int):
    """
    API per eliminare fisicamente un ambito.
    """
    logging.info(f"Richiesta DELETE per ambito con ID: {ambito_id}")
    result, status_code = service_t_ambito.delete_ambito(ambito_id)
    return jsonify(result), status_code
