# Classi/ClasseAnagrafica/ClasseAmbito/Controller_t_ambito.py
from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseAmbito.Service_t_ambito import Service_t_ambito
import logging

# Inizializzazione del Blueprint per il controller Ambito
t_ambito_controller = Blueprint('ambito', __name__)
service_t_ambito = Service_t_ambito()

@t_ambito_controller.route("/", methods=['GET'])
def get_all_ambiti():
    """
    API per recuperare tutti gli ambiti.
    Restituisce la lista così com'è fornita dal repository (lista di dizionari).
    """
    logging.info("Richiesta GET per tutti gli ambiti.")
    try:
        ambiti = service_t_ambito.get_all_ambiti()
        logging.info(f"Recuperati {len(ambiti)} ambiti dal servizio.")
        # ambiti è già una lista di dizionari (con chiave 'descr' per la descrizione)
        return jsonify(ambiti), 200
    except Exception as e:
        logging.error(f"Errore nel recupero degli ambiti (Controller): {e}")
        return jsonify({"error": f"Errore interno del server nel recupero degli ambiti: {str(e)}"}), 500

@t_ambito_controller.route("/<int:ambito_id>", methods=['GET'])
def get_ambito_by_id(ambito_id: int):
    """
    API per recuperare un ambito tramite ID.
    """
    logging.info(f"Richiesta GET per ambito con ID: {ambito_id}")
    try:
        ambito = service_t_ambito.get_ambito_by_id(ambito_id)
        if ambito:
            return jsonify(ambito), 200
        else:
            return jsonify({"error": "Ambito non trovato."}), 404
    except Exception as e:
        logging.error(f"Errore nel recupero dell'ambito (Controller) ID {ambito_id}: {e}")
        return jsonify({"error": f"Errore interno del server: {str(e)}"}), 500

@t_ambito_controller.route("/", methods=['POST'])
def create_ambito():
    """
    API per creare un nuovo ambito.
    Richiede 'codice', 'descr' (descrizione), 'note' (opzionale) nel corpo della richiesta JSON.
    Recupera 'modificato_da' dalla sessione dell'utente loggato.
    """
    data = request.get_json()
    codice = data.get('codice')
    descr = data.get('descr')
    note = data.get('note')
    
    modificato_da = session.get('username', 'Sistema')

    if not codice or not descr:
        logging.warning("Tentativo di creare ambito con dati mancanti (codice o descr).")
        return jsonify({"error": "Codice e descr sono obbligatori."}), 400

    logging.info(f"Richiesta POST per creare ambito con codice: {codice}")
    result_obj, status_code = service_t_ambito.create_ambito(codice, descr, note, modificato_da)
    
    if status_code in (200, 201) and result_obj:
        return jsonify(result_obj), status_code
    else:
        return jsonify(result_obj), status_code

@t_ambito_controller.route("/<int:ambito_id>", methods=['PUT'])
def update_ambito(ambito_id: int):
    """
    API per aggiornare la descrizione e le note di un ambito esistente.
    Richiede 'descr' (descrizione), 'note' (opzionale) nel corpo della richiesta JSON.
    Recupera 'modificato_da' dalla sessione dell'utente loggato.
    """
    data = request.get_json()
    descr = data.get('descr')
    note = data.get('note')

    modificato_da = session.get('username', 'Sistema')

    if not descr:
        logging.warning(f"Tentativo di aggiornare ambito {ambito_id} con descr mancante.")
        return jsonify({"error": "Descr è obbligatoria."}), 400

    logging.info(f"Richiesta PUT per aggiornare ambito con ID: {ambito_id}")
    result_obj, status_code = service_t_ambito.update_ambito(ambito_id, descr, note, modificato_da)
    
    if status_code == 200 and result_obj:
        return jsonify(result_obj), status_code
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