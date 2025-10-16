# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseCliente/Controller_t_cliente.py

from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseCliente.Service_t_cliente import Service_t_cliente
import logging
from datetime import datetime

# Inizializzazione del Blueprint per il controller Cliente
t_cliente_controller = Blueprint('cliente', __name__)
service_t_cliente = Service_t_cliente()

# Funzione helper per formattare le date in modo sicuro
def format_date_for_json(date_value):
    """
    Formatta un oggetto datetime o date in una stringa ISO 8601.
    """
    if isinstance(date_value, (datetime, date)):
        return date_value.isoformat()
    elif isinstance(date_value, str):
        return date_value
    return None

@t_cliente_controller.route("/", methods=['GET'])
def get_all_clienti():
    """
    API per recuperare tutti i clienti.
    """
    logging.info("Richiesta GET per tutti i clienti.")
    clienti, status_code = service_t_cliente.get_all_clienti()
    return jsonify(clienti), status_code

@t_cliente_controller.route("/<int:cliente_id>", methods=['GET'])
def get_cliente_by_id(cliente_id):
    """
    API per recuperare un cliente per ID.
    """
    logging.info(f"Richiesta GET per cliente con ID: {cliente_id}")
    cliente, status_code = service_t_cliente.get_cliente_by_id(cliente_id)
    return jsonify(cliente), status_code

@t_cliente_controller.route("/", methods=['POST'])
def create_cliente():
    """
    API per creare un nuovo cliente.
    """
    data = request.json
    ragione_sociale = data.get('ragione_sociale')
    partita_iva = data.get('partita_iva')
    indirizzo = data.get('indirizzo')
    citta = data.get('citta')
    provincia = data.get('provincia')
    cap = data.get('cap')
    email = data.get('email')
    telefono = data.get('telefono')
    
    # Prende l'utente dalla sessione di Flask o usa un valore di default
    creato_da = session.get('username', 'Sistema')
    
    logging.info(f"Richiesta POST per creare un nuovo cliente: {ragione_sociale}")
    result_obj, status_code = service_t_cliente.create_cliente(
        ragione_sociale, partita_iva, indirizzo, citta, provincia, cap, 
        email, telefono, creato_da
    )

    return jsonify(result_obj), status_code

@t_cliente_controller.route("/<int:cliente_id>", methods=['PUT'])
def update_cliente(cliente_id):
    """
    API per aggiornare un cliente esistente.
    """
    data = request.json
    ragione_sociale = data.get('ragione_sociale')
    partita_iva = data.get('partita_iva')
    indirizzo = data.get('indirizzo')
    citta = data.get('citta')
    provincia = data.get('provincia')
    cap = data.get('cap')
    email = data.get('email')
    telefono = data.get('telefono')
    
    # Prende l'utente dalla sessione di Flask o usa un valore di default
    modificato_da = session.get('username', 'Sistema')

    logging.info(f"Richiesta PUT per aggiornare cliente con ID: {cliente_id}")
    result_obj, status_code = service_t_cliente.update_cliente(
        cliente_id, ragione_sociale, partita_iva, indirizzo, citta, provincia, cap, 
        email, telefono, modificato_da
    )
    
    return jsonify(result_obj), status_code

@t_cliente_controller.route("/<int:cliente_id>", methods=['DELETE'])
def delete_cliente(cliente_id):
    """
    API per eliminare un cliente per ID.
    """
    logging.info(f"Richiesta DELETE per eliminare cliente con ID: {cliente_id}")
    result_obj, status_code = service_t_cliente.delete_cliente(cliente_id)
    return jsonify(result_obj), status_code