# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDomanda/Controller_t_domanda.py

# MODIFICA 1: Rimosso 'render_template' dall'import di flask
from flask import Blueprint, request, jsonify, session 
from Classi.ClasseAnagrafica.ClasseDomanda.Service_t_domanda import Service_t_domanda
from Classi.ClasseAnagrafica.ClasseDriver.Service_t_driver import Service_t_driver 
# Importa il servizio per il menu (non necessario se la rotta frontend non è qui)
# Questo import può essere rimosso, ma lo lascio per sicurezza se lo usi altrove
# from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import Service_t_funzionalitaUtente
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Service_t_gruppo_risposta import Service_t_gruppo_risposta
import logging
from datetime import datetime
# from functools import wraps # Rimosso l'import non necessario

# Inizializzazione del Blueprint per il controller Domanda
t_domanda_controller = Blueprint('domanda', __name__)
service_t_domanda = Service_t_domanda()
service_t_driver = Service_t_driver() 
# service_t_funzionalita_utente = Service_t_funzionalitaUtente() 
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

# Funzione helper per uniformare la risposta JSON, inclusi i campi del Gruppo Risposta
def _format_domanda_response(domanda_obj):
    """
    Formatta un dizionario/oggetto Domanda con tutte le relazioni per la risposta JSON.
    Assumiamo che il Repository restituisca un dizionario con i campi necessari,
    inclusi i campi flat del driver se il join è stato eseguito.
    """
    if not domanda_obj:
        return None
    
    # Se il driver è un oggetto/dizionario annidato, estraiamo i campi
    driver_descr = domanda_obj.get('descr_driver')
    driver_id = domanda_obj.get('id_driver')
    gruppo_risposta_id = domanda_obj.get('id_gruppo_risposta')
    gruppo_risposta_descr = domanda_obj.get('descr_gruppo_risposta') 
    
    # Costruisce la risposta JSON
    return {
        'id': domanda_obj.get('id'),
        'descr': domanda_obj.get('descr'),
        'id_driver': driver_id,
        'driver_descr': driver_descr,
        'abilitato': domanda_obj.get('abilitato'),
        'data_ultima_modifica': format_date_for_json(domanda_obj.get('data_ultima_modifica')),
        'modificato_da': domanda_obj.get('modificato_da'),
        'id_gruppo_risposta': gruppo_risposta_id,
        'gruppo_risposta_descr': gruppo_risposta_descr
    }

# **********************************************
# ROTTA HTML RIMOSSA (MODIFICA 2)
# **********************************************
# La rotta @t_domanda_controller.route("/gestione_gruppo", methods=['GET']) è stata rimossa, 
# in quanto la gestione del rendering HTML è stata spostata in server.py


# ----------------------------------------------------
# API ENDPOINTS (SOLO JSON)
# ----------------------------------------------------

@t_domanda_controller.route("/", methods=['GET'])
def get_all_domande():
    """
    API per recuperare tutte le domande con i dettagli del driver.
    Supporta il filtro opzionale per id_driver.
    """
    logging.info("Richiesta GET per tutte le domande.")
    # 🔴 PRIMA: id_driver_filter = request.args.get('id_driver')
    # 🟢 DOPO: accetta sia 'id_driver_filter' (dal frontend) che 'id_driver'
    id_driver_filter = request.args.get('id_driver_filter') or request.args.get('id_driver')
    
    try:
        if id_driver_filter:
            id_driver_filter = int(id_driver_filter)
        
        domande = service_t_domanda.get_all_domande(id_driver_filter=id_driver_filter)
        
        # Formattazione per includere i dati del driver
        domande_data = [_format_domanda_response(d) for d in domande]
        
        logging.info(f"Recuperate {len(domande_data)} domande.") 
        return jsonify(domande_data), 200
    except Exception as e:
        logging.error(f"Errore nel recupero delle domande: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500


# **********************************************
# NUOVO ENDPOINT: GET per ID
# **********************************************
@t_domanda_controller.route("/<int:domanda_id>", methods=['GET'])
def get_domanda_by_id(domanda_id: int):
    """
    API per recuperare una singola domanda tramite ID.
    Questo endpoint è necessario per il frontend (domanda.html) per
    leggere i dati prima di un aggiornamento (PUT).
    """
    logging.info(f"Richiesta GET per domanda con ID: {domanda_id}")
    try:
        # service_t_domanda.get_domanda_by_id chiama il repository che esegue 
        # il joinedload e restituisce il dict formattato.
        domanda = service_t_domanda.get_domanda_by_id(domanda_id)
        
        if domanda:
            logging.info(f"Recuperata domanda con ID: {domanda_id}")
            # Usa la funzione helper per formattare la risposta
            return jsonify(_format_domanda_response(domanda)), 200
        else:
            logging.warning(f"Domanda con ID {domanda_id} non trovata.")
            return jsonify({"error": f"Domanda con ID {domanda_id} non trovata."}), 404
    except Exception as e:
        logging.error(f"Errore nel recupero della domanda {domanda_id}: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500


@t_domanda_controller.route("/", methods=['POST'])
def create_domanda():
    """
    API per creare una nuova domanda.
    """
    data = request.get_json()
    descr = data.get('descr')
    id_driver = data.get('id_driver')
    id_gruppo_risposta = data.get('id_gruppo_risposta')
    abilitato = data.get('abilitato', True)
    modificato_da = session.get('username', 'Sistema')

    if not descr or id_driver is None:
        return jsonify({"error": "Descrizione e ID Driver sono obbligatori."}), 400

    logging.info(f"Richiesta POST per creare domanda: {descr}")
    result_obj, status_code = service_t_domanda.create_domanda(
        descr, 
        id_driver, 
        id_gruppo_risposta,
        abilitato,
        modificato_da
    )
    
    if status_code == 201 and result_obj:
        # Usa la funzione helper per formattare la risposta
        return jsonify(_format_domanda_response(result_obj)), status_code
    else:
        return jsonify(result_obj), status_code


@t_domanda_controller.route("/<int:domanda_id>", methods=['PUT'])
def update_domanda(domanda_id: int):
    """
    API per aggiornare una domanda esistente.
    CORREZIONE TypeError: Rimosso 'abilitato' dalla chiamata al service.
    """
    data = request.get_json()
    descr = data.get('descr')
    id_driver = data.get('id_driver')
    id_gruppo_risposta = data.get('id_gruppo_risposta') 
    # abilitato = data.get('abilitato') # Manteniamo abilitato nel Service solo se necessario
    modificato_da = session.get('username', 'Sistema')

    if not descr:
        logging.warning(f"Tentativo di aggiornare domanda {domanda_id} con descrizione mancante.")
        return jsonify({"error": "Descrizione è obbligatoria."}), 400
    
    if id_driver is None:
        logging.warning(f"Tentativo di aggiornare domanda {domanda_id} con ID Driver mancante.")
        return jsonify({"error": "ID Driver è obbligatorio."}), 400

    logging.info(f"Richiesta PUT per aggiornare domanda con ID: {domanda_id}")
    
    # Rimosso 'abilitato' per risolvere il TypeError, in quanto il Service non lo accetta
    result_obj, status_code = service_t_domanda.update_domanda(
        domanda_id,
        descr, 
        id_driver,
        id_gruppo_risposta,
        modificato_da
    )
    
    if status_code == 200 and result_obj:
        # Usa la funzione helper per formattare la risposta
        return jsonify(_format_domanda_response(result_obj)), status_code
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
        # La correzione qui assicura che si acceda ai dati come dizionari
        drivers_data = [{'id': driver['id'], 'descr': driver['descr']} for driver in drivers]
        logging.info(f"Recuperati {len(drivers_data)} driver.")
        return jsonify(drivers_data), 200
    except Exception as e:
        logging.error(f"Errore nel recupero dei driver: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500
    
# NUOVO ENDPOINT: per recuperare tutti i gruppi risposta (per il dropdown nella Modal)   
@t_domanda_controller.route("/gruppi_risposta", methods=['GET'])
def get_gruppi_risposta_for_dropdown():
    """
    API per recuperare tutti i gruppi risposta, utilizzata per popolare un dropdown.
    """
    logging.info("Richiesta GET per gruppi risposta per dropdown domande.")
    try: # <--- CORREZIONE: USO DEI DUE PUNTI (:)
        # Assumiamo che service_t_gruppo_risposta.get_all_gruppi_risposta() esista e ritorni una lista di dict
        gruppi = service_t_gruppo_risposta.get_all_gruppi_risposta() 
        # Assumo che i campi siano ID_GRUPPO_RISPOSTA e DESCR_GRUPPO_RISPOSTA (adattabile se il service restituisce 'id' e 'descr')
        gruppi_data = [{'id': gruppo.get('ID_GRUPPO_RISPOSTA') or gruppo.get('id'), 'descr': gruppo.get('DESCR_GRUPPO_RISPOSTA') or gruppo.get('descr')} for gruppo in gruppi]
        logging.info(f"Recuperati {len(gruppi_data)} gruppi risposta.")
        return jsonify([g for g in gruppi_data if g['id'] is not None]), 200
    except Exception as e: # <--- CORREZIONE: USO DEI DUE PUNTI (:) e sintassi 'except'
        logging.error(f"Errore nel recupero dei gruppi risposta: {str(e)}")
        return jsonify({"error": "Errore interno del server"}), 500