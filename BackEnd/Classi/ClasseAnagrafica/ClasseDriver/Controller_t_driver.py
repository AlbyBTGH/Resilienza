# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDriver/Controller_t_driver.py

from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseDriver.Service_t_driver import Service_t_driver
from Classi.ClasseAnagrafica.ClasseCategoria.Service_t_categoria import Service_t_categoria # Per recuperare le categorie per il dropdown
import logging
from datetime import datetime

# Inizializzazione del Blueprint per il controller Driver
t_driver_controller = Blueprint('driver', __name__)
service_t_driver = Service_t_driver()
service_t_categoria = Service_t_categoria() # Per caricare le categorie nel frontend

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

@t_driver_controller.route("/", methods=['GET'])
def get_all_drivers():
    """
    API per recuperare tutti i driver con i dettagli della categoria.
    Supporta il filtro opzionale per id_categoria.
    """
    logging.info("Richiesta GET per driver.")
    try:
        id_categoria_filter = request.args.get('id_categoria', type=int)
        if id_categoria_filter:
            logging.info(f"Filtro categoria applicato: {id_categoria_filter}")
        else:
            logging.info("Nessun filtro categoria, recupero tutti i driver.")
        
        drivers = service_t_driver.get_all_drivers(id_categoria_filter)
        return jsonify(drivers), 200
    except Exception as e:
        logging.error(f"Errore nel servizio durante il recupero di tutti i driver: {str(e)}")
        return jsonify({"error": "Errore nel recupero dei driver."}), 500

@t_driver_controller.route("/<int:driver_id>", methods=['GET'])
def get_driver_by_id(driver_id: int):
    """
    API per recuperare un driver tramite ID con i dettagli della categoria.
    """
    logging.info(f"Richiesta GET per driver con ID: {driver_id}")
    try:
        driver = service_t_driver.get_driver_by_id(driver_id)
        if driver:
            return jsonify(driver), 200
        else:
            return jsonify({"error": "Driver non trovato."}), 404
    except Exception as e:
        logging.error(f"Errore nel recupero del driver con ID {driver_id}: {str(e)}")
        return jsonify({"error": "Errore nel recupero del driver."}), 500

@t_driver_controller.route("/", methods=['POST'])
def create_driver():
    """
    API per creare un nuovo driver.
    """
    logging.info("Richiesta POST per creare un nuovo driver.")
    data = request.json
    descr = data.get('descr')
    id_categoria = data.get('id_categoria')
    creato_da = session.get('username', 'system') # Recupera l'utente dalla sessione

    if not descr or not id_categoria:
        logging.warning("Descrizione o ID categoria mancante.")
        return jsonify({"error": "Descrizione e ID Categoria sono obbligatori."}), 400

    result_obj, status_code = service_t_driver.create_driver(descr, id_categoria, creato_da)
    
    if status_code == 201 and result_obj:
        return jsonify({
            'id': result_obj['id'],
            'descr': result_obj['descr'],
            'id_categoria': result_obj['id_categoria'],
            'data_ultima_modifica': format_date_for_json(result_obj['data_ultima_modifica']),
            'modificato_da': result_obj['modificato_da']
        }), status_code
    else:
        return jsonify(result_obj), status_code

@t_driver_controller.route("/<int:driver_id>", methods=['PUT'])
def update_driver(driver_id: int):
    """
    API per aggiornare un driver esistente.
    """
    logging.info(f"Richiesta PUT per aggiornare driver con ID: {driver_id}")
    data = request.json
    descr = data.get('descr')
    id_categoria = data.get('id_categoria')
    modificato_da = session.get('username', 'system') # Recupera l'utente dalla sessione

    if not descr or not id_categoria:
        logging.warning("Descrizione o ID categoria mancante.")
        return jsonify({"error": "Descrizione e ID Categoria sono obbligatori."}), 400

    result_obj, status_code = service_t_driver.update_driver(driver_id, descr, id_categoria, modificato_da)
    
    if status_code == 200 and result_obj:
        return jsonify({
            'id': result_obj['id'],
            'descr': result_obj['descr'],
            'id_categoria': result_obj['id_categoria'],
            'data_ultima_modifica': format_date_for_json(result_obj['data_ultima_modifica']),
            'modificato_da': result_obj['modificato_da']
        }), status_code
    else:
        return jsonify(result_obj), status_code

@t_driver_controller.route("/<int:driver_id>", methods=['DELETE'])
def delete_driver(driver_id: int):
    """
    API per eliminare fisicamente un driver.
    """
    logging.info(f"Richiesta DELETE per driver con ID: {driver_id}")
    result, status_code = service_t_driver.delete_driver(driver_id)
    return jsonify(result), status_code

# Endpoint per recuperare tutte le categorie (per il dropdown nel frontend)
@t_driver_controller.route("/categorie", methods=['GET'])
def get_categorie_for_dropdown():
    """
    API per recuperare tutte le categorie, utilizzata per popolare un dropdown.
    """
    logging.info("Richiesta GET per categorie per dropdown driver.")
    try:
        categorie = service_t_categoria.get_all_categorie()
        # Assicurati che service_t_categoria.get_all_categorie() restituisca oggetti con 'id' e 'descr'
        # o converte tu qui se necessario (es: categorie = self.repository.get_all() che ritorna TCategoria oggetti)
        categorie_data = [{'id': categoria['id'], 'descr': categoria['descr']} for categoria in categorie]
        return jsonify(categorie_data), 200
    except Exception as e:
        logging.error(f"Errore nel recupero delle categorie per dropdown: {str(e)}")
        return jsonify({"error": "Errore nel recupero delle categorie."}), 500
