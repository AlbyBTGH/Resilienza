# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDomanda/Controller_t_domanda.py

from flask import Blueprint, request, jsonify, session 
from Classi.ClasseAnagrafica.ClasseDomanda.Service_t_domanda import Service_t_domanda
from Classi.ClasseAnagrafica.ClasseDriver.Service_t_driver import Service_t_driver 
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Service_t_gruppo_risposta import Service_t_gruppo_risposta
import logging
from datetime import datetime

# Inizializzazione del Blueprint per il controller Domanda
t_domanda_controller = Blueprint('domanda', __name__)
service_t_domanda = Service_t_domanda()
service_t_driver = Service_t_driver() 
service_t_gruppo_risposta = Service_t_gruppo_risposta()


@t_domanda_controller.route("/", methods=['GET'])
def get_all_domande():
    """
    API per recuperare tutte le domande.
    Accetta un parametro di query opzionale 'id_driver_filter' per filtrare.
    """
    id_driver_filter_str = request.args.get('id_driver_filter')
    id_driver_filter = None
    if id_driver_filter_str:
        try:
            id_driver_filter = int(id_driver_filter_str)
        except ValueError:
            logging.warning("Parametro 'id_driver_filter' non valido.")
            # Si potrebbe decidere di continuare senza filtro o ritornare un errore 400
            # Ho scelto di continuare senza filtro per flessibilità.
            pass

    logging.info(f"Richiesta GET per tutte le domande (filtro Driver: {id_driver_filter}).")
    try:
        domande = service_t_domanda.get_all_domande(id_driver_filter)
        logging.info(f"Recuperate {len(domande)} domande dal servizio.")
        return jsonify(domande), 200
    except Exception as e:
        logging.error(f"Errore nel recupero delle domande (Controller): {e}")
        return jsonify({"error": f"Errore interno del server nel recupero delle domande: {str(e)}"}), 500


@t_domanda_controller.route("/<int:domanda_id>", methods=['GET'])
def get_domanda_by_id(domanda_id: int):
    """
    API per recuperare una domanda tramite ID.
    """
    logging.info(f"Richiesta GET per domanda con ID: {domanda_id}")
    result_obj = service_t_domanda.get_domanda_by_id(domanda_id)
    
    if result_obj:
        return jsonify(result_obj), 200
    else:
        return jsonify({"error": f"Domanda con ID {domanda_id} non trovata."}), 404


@t_domanda_controller.route("/", methods=['POST'])
def create_domanda():
    """
    API per creare una nuova domanda.
    Richiede 'descr' (descrizione), 'id_driver', 'id_gruppo_risposta' (opzionale).
    """
    data = request.get_json()
    descr = data.get('descr')
    id_driver = data.get('id_driver')
    id_gruppo_risposta = data.get('id_gruppo_risposta')
    # Rimosso: Gestione del campo is_attiva 
    
    # Conversione dei tipi
    try:
        if id_driver is not None:
            id_driver = int(id_driver)
        if id_gruppo_risposta is not None and id_gruppo_risposta != '':
            id_gruppo_risposta = int(id_gruppo_risposta)
        else:
            id_gruppo_risposta = None # Assicura che sia None se vuoto
        
        # Rimosso: Gestione della conversione booleana di is_attiva

    except ValueError:
        # Messaggio di errore aggiornato per riflettere solo i campi numerici gestiti
        return jsonify({"error": "I campi 'id_driver' e 'id_gruppo_risposta' devono essere numeri interi validi."}), 400

    if not descr or not id_driver:
        logging.warning("Tentativo di creare domanda con descr o id_driver mancanti.")
        return jsonify({"error": "Descr e id_driver sono obbligatori."}), 400
    
    inserito_da = session.get('username', 'Sistema') # Recupera l'utente dalla sessione

    logging.info(f"Richiesta POST per creare domanda per Driver ID: {id_driver}")
    # CHIAMATA CORRETTA: 5 ARGOMENTI TOTALI (self implicito + 4 espliciti)
    result_obj, status_code = service_t_domanda.create_domanda(
        descr, 
        id_driver, 
        id_gruppo_risposta, 
        inserito_da
    )
    
    if status_code in (200, 201) and result_obj:
        return jsonify(result_obj), status_code
    else:
        return jsonify(result_obj), status_code


@t_domanda_controller.route("/<int:domanda_id>", methods=['PUT'])
def update_domanda(domanda_id: int):
    """
    API per aggiornare una domanda esistente.
    Richiede 'descr', 'id_driver', 'id_gruppo_risposta' (opzionale).
    """
    data = request.get_json()
    descr = data.get('descr')
    id_driver = data.get('id_driver')
    id_gruppo_risposta = data.get('id_gruppo_risposta')
    # Rimosso: is_attiva = data.get('is_attiva') 
    
    # Conversione dei tipi
    try:
        if id_driver is not None:
            id_driver = int(id_driver)
        if id_gruppo_risposta is not None and id_gruppo_risposta != '':
            id_gruppo_risposta = int(id_gruppo_risposta)
        else:
            # Se la chiave è presente ma il valore è vuoto (es. il frontend invia null/empty string)
            # deve essere trattato come l'intenzione di impostare a NULL nel DB.
            if 'id_gruppo_risposta' in data and data.get('id_gruppo_risposta') in ('', None):
                 id_gruppo_risposta = None
            elif id_gruppo_risposta is not None:
                id_gruppo_risposta = int(id_gruppo_risposta)

        # Rimosso: Gestione della conversione booleana di is_attiva
            
    except ValueError:
        # Messaggio di errore aggiornato
        return jsonify({"error": "I campi 'id_driver' e 'id_gruppo_risposta' devono essere numeri interi validi."}), 400

    if not descr or not id_driver:
        logging.warning(f"Tentativo di aggiornare domanda {domanda_id} con descr o id_driver mancanti.")
        return jsonify({"error": "Descr e id_driver sono obbligatori per l'aggiornamento."}), 400

    modificato_da = session.get('username', 'Sistema') # Recupera l'utente dalla sessione

    logging.info(f"Richiesta PUT per aggiornare domanda con ID: {domanda_id}")
    # CHIAMATA CORRETTA: 6 ARGOMENTI TOTALI (self implicito + 5 espliciti)
    result_obj, status_code = service_t_domanda.update_domanda(
        domanda_id, 
        descr, 
        id_driver, 
        id_gruppo_risposta, 
        modificato_da
    )
    
    if status_code == 200 and result_obj:
        return jsonify(result_obj), status_code
    else:
        return jsonify(result_obj), status_code


@t_domanda_controller.route("/<int:domanda_id>", methods=['DELETE'])
def delete_domanda(domanda_id: int):
    """
    API per eliminare fisicamente una domanda.
    """
    logging.info(f"Richiesta DELETE per eliminare domanda con ID: {domanda_id}")
    
    result_obj, status_code = service_t_domanda.delete_domanda(domanda_id)
    
    if status_code == 200:
        return jsonify({"message": f"Domanda con ID {domanda_id} eliminata con successo."}), 200
    else:
        # Passa il messaggio di errore dal servizio (es. Ambito non trovato)
        return jsonify(result_obj), status_code


# --- ENDPOINT AUSILIARI PER DROPDOWN ---

@t_domanda_controller.route("/drivers", methods=['GET'])
def get_drivers_for_dropdown():
    """
    API per recuperare tutti i driver, utilizzata per popolare un dropdown.
    """
    logging.info("Richiesta GET per driver per dropdown domande.")
    try:
        # Assumiamo che service_t_driver.get_all_drivers() esista e ritorni una lista di dict
        drivers = service_t_driver.get_all_drivers() 
        # Assumo che i campi siano ID e DESCR (adattabile se il service restituisce 'id' e 'descr')
        drivers_data = [{'id': driver.get('ID') or driver.get('id'), 'descr': driver.get('DESCR') or driver.get('descr')} for driver in drivers]
        logging.info(f"Recuperati {len(drivers_data)} driver per dropdown.")
        return jsonify(drivers_data), 200
    except Exception as e:
        logging.error(f"Errore nel recupero dei driver: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500
    
   
@t_domanda_controller.route("/gruppi_risposta", methods=['GET'])
def get_gruppi_risposta_for_dropdown():
    """
    API per recuperare tutti i gruppi risposta, utilizzata per popolare un dropdown.
    """
    logging.info("Richiesta GET per gruppi risposta per dropdown domande.")
    try:
        # Assumiamo che service_t_gruppo_risposta.get_all_gruppi_risposta() esista e ritorni una lista di dict
        gruppi = service_t_gruppo_risposta.get_all_gruppi_risposta() 
        # Assumo che i campi siano ID_GRUPPO_RISPOSTA e DESCR_GRUPPO_RISPOSTA (adattabile se il service restituisce 'id' e 'descr')
        gruppi_data = [{'id': gruppo.get('ID_GRUPPO_RISPOSTA') or gruppo.get('id'), 'descr': gruppo.get('DESCR_GRUPPO_RISPOSTA') or gruppo.get('descr')} for gruppo in gruppi]
        logging.info(f"Recuperati {len(gruppi_data)} gruppi risposta per dropdown.")
        return jsonify(gruppi_data), 200
    except Exception as e:
        logging.error(f"Errore nel recupero dei gruppi risposta: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500