# Classi/ClasseAsset/Controller_t_asset.py
# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from Classi.ClasseAsset.Service_t_asset import Service_t_asset
import csv
from io import TextIOWrapper
import logging

t_asset_controller = Blueprint('asset', __name__)
service_asset = Service_t_asset()

@t_asset_controller.route("/cliente/<int:id_cliente>", methods=['GET'])
def get_assets_cliente(id_cliente):
    try:
        result, status_code = service_asset.get_assets_by_cliente(id_cliente)
        return jsonify(result), status_code
    except Exception as e:
        logging.error(f"Errore Controller Asset (get_assets_cliente): {str(e)}")
        return jsonify({"error": str(e)}), 500

@t_asset_controller.route("/upload/<int:id_cliente>", methods=['POST'])
def upload_asset_csv(id_cliente):
    if 'file' not in request.files:
        return jsonify({"error": "Nessun file inviato"}), 400
    
    file = request.files['file']
    modificato_da = request.form.get('utente', 'Sistema')

    try:
        # 'utf-8-sig' gestisce i file salvati da Excel con BOM
        csv_file = TextIOWrapper(file.stream, encoding='utf-8-sig')
        
        sample = csv_file.read(2048)
        csv_file.seek(0)
        
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=',;') if sample else 'excel'
        except csv.Error:
            dialect = 'excel'
        
        reader = csv.DictReader(csv_file, dialect=dialect)
        
        asset_list = []
        for row in reader:
            # Ricerca flessibile della colonna 'descrizione'
            valore = next((v for k, v in row.items() if k and k.strip().lower() == 'descrizione'), None)
            if valore and valore.strip():
                asset_list.append(valore.strip())
        
        if not asset_list:
            logging.warning(f"Colonne rilevate: {reader.fieldnames}")
            return jsonify({"error": "Nessun dato trovato. Assicurati che la colonna si chiami 'descrizione'"}), 400

        result, status_code = service_asset.import_from_list(id_cliente, asset_list, modificato_da)
        return jsonify(result), status_code

    except Exception as e:
        logging.error(f"Errore Controller Asset (upload): {str(e)}")
        return jsonify({"error": f"Errore durante l'upload: {str(e)}"}), 500