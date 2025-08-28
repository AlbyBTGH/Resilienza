# Classi/ClasseAnagrafica/ClasseCategoria/Controller_t_categoria.py

from flask import Blueprint, request, jsonify, session
from Classi.ClasseAnagrafica.ClasseCategoria.Service_t_categoria import Service_t_categoria
from Classi.ClasseAnagrafica.ClasseAmbito.Service_t_ambito import Service_t_ambito
import logging
from datetime import datetime

t_categoria_controller = Blueprint('categoria', __name__)
service_t_categoria = Service_t_categoria()
service_t_ambito = Service_t_ambito()

def format_date_for_json(date_value):
    if isinstance(date_value, datetime):
        return date_value.isoformat()
    elif isinstance(date_value, str):
        return date_value
    return None

@t_categoria_controller.route("/", methods=['GET'])
def get_all_categorie():
    logging.info("Richiesta GET per categorie.")
    try:
        id_ambito_filter = request.args.get('id_ambito', type=int)
        if id_ambito_filter:
            logging.info(f"Filtro ambito applicato: {id_ambito_filter}")
        else:
            logging.info("Nessun filtro ambito, recupero tutte le categorie.")
        
        categorie = service_t_categoria.get_all_categorie(id_ambito_filter)
        return jsonify(categorie), 200
    except Exception as e:
        logging.error(f"Errore nel servizio durante il recupero di tutte le categorie: {str(e)}")
        return jsonify({"error": "Errore nel recupero delle categorie."}), 500

@t_categoria_controller.route("/<int:categoria_id>", methods=['GET'])
def get_categoria_by_id(categoria_id: int):
    logging.info(f"Richiesta GET per categoria con ID: {categoria_id}")
    try:
        categoria = service_t_categoria.get_categoria_by_id(categoria_id)
        if categoria:
            return jsonify(categoria), 200
        else:
            return jsonify({"error": "Categoria non trovata."}), 404
    except Exception as e:
        logging.error(f"Errore nel recupero della categoria con ID {categoria_id}: {str(e)}")
        return jsonify({"error": "Errore nel recupero della categoria."}), 500

@t_categoria_controller.route("/", methods=['POST'])
def create_categoria():
    logging.info("Richiesta POST per creare una nuova categoria.")
    data = request.json
    id_ambito = data.get('id_ambito')
    descr = data.get('descr')
    tipo_categoria = data.get('tipo_categoria') # Aggiunto: tipo_categoria
    creato_da = session.get('username', 'system')

    if not id_ambito or not descr:
        logging.warning("ID ambito o descrizione mancante.")
        return jsonify({"error": "ID Ambito e Descrizione sono obbligatori."}), 400

    # Modifica qui: Aggiunto 'tipo_categoria', rimosso 'note' e 'acronimo'
    result_obj, status_code = service_t_categoria.create_categoria(id_ambito, descr, tipo_categoria, creato_da)
    
    if status_code == 201 and result_obj:
        return jsonify({
            'id': result_obj['id'],
            'id_ambito': result_obj['id_ambito'],
            'descr': result_obj['descr'],
            'tipo_categoria': result_obj['tipo_categoria'], # Aggiunto: tipo_categoria
            'data_ultima_modifica': format_date_for_json(result_obj['data_ultima_modifica']),
            'modificato_da': result_obj['modificato_da']
        }), status_code
    else:
        return jsonify(result_obj), status_code

@t_categoria_controller.route("/<int:categoria_id>", methods=['PUT'])
def update_categoria(categoria_id: int):
    logging.info(f"Richiesta PUT per aggiornare categoria con ID: {categoria_id}")
    data = request.json
    id_ambito = data.get('id_ambito')
    descr = data.get('descr')
    tipo_categoria = data.get('tipo_categoria') # Aggiunto: tipo_categoria
    modificato_da = session.get('username', 'system')

    if not id_ambito or not descr:
        logging.warning("ID ambito o descrizione mancante.")
        return jsonify({"error": "ID Ambito e Descrizione sono obbligatori."}), 400

    # Modifica qui: Aggiunto 'tipo_categoria', rimosso 'note' e 'acronimo'
    result_obj, status_code = service_t_categoria.update_categoria(categoria_id, id_ambito, descr, tipo_categoria, modificato_da)
    
    if status_code == 200 and result_obj:
        return jsonify({
            'id': result_obj['id'],
            'id_ambito': result_obj['id_ambito'],
            'descr': result_obj['descr'],
            'tipo_categoria': result_obj['tipo_categoria'], # Aggiunto: tipo_categoria
            'data_ultima_modifica': format_date_for_json(result_obj['data_ultima_modifica']),
            'modificato_da': result_obj['modificato_da']
        }), status_code
    else:
        return jsonify(result_obj), status_code

@t_categoria_controller.route("/<int:categoria_id>", methods=['DELETE'])
def delete_categoria(categoria_id: int):
    logging.info(f"Richiesta DELETE per categoria con ID: {categoria_id}")
    result, status_code = service_t_categoria.delete_categoria(categoria_id)
    return jsonify(result), status_code

@t_categoria_controller.route("/ambiti", methods=['GET'])
def get_ambiti_for_dropdown():
    logging.info("Richiesta GET per ambiti per dropdown categorie.")
    try:
        ambiti = service_t_ambito.get_all_ambiti()
        ambiti_data = [{'id': ambito['id'], 'descrizione': ambito['descrizione']} for ambito in ambiti]
        return jsonify(ambiti_data), 200
    except Exception as e:
        logging.error(f"Errore nel recupero degli ambiti per dropdown: {str(e)}")
        return jsonify({"error": "Errore nel recupero degli ambiti."}), 500
