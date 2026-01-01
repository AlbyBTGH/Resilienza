# File: Classi/ClasseCorrettive/Controller_correttiva.py
# -*- coding: utf-8 -*-
import sys
import logging
from flask import Blueprint, jsonify, request
from Classi.ClasseCorrettive.Service_correttiva import ServiceCorrettiva
# Assumendo che le funzioni di utility siano accessibili o replicate
from Classi.ClasseRisposteCliente.Controller_risposta_cliente import get_username_from_session 

def get_correttiva_service():
    """Helper per accedere all'istanza del service inizializzata in server.py."""
    try:
        # Assumi che service_correttiva sia stata inizializzata nel punto di ingresso
        return sys.modules['server'].service_correttiva 
    except (AttributeError, KeyError):
        logging.error("Istanza service_correttiva non trovata.")
        return ServiceCorrettiva() 

# Definisce il Blueprint
correttiva_controller = Blueprint('correttiva', __name__)
logging.basicConfig(level=logging.INFO)

# ======================================================================
# ROTTA: Creazione Nuova Correttiva (POST)
# ======================================================================
@correttiva_controller.route(
    "/api/correttiva/salva_nuova", methods=['POST']
)
def salva_nuova_correttiva_route():
    dati_correttiva = request.get_json() 
    
    if not isinstance(dati_correttiva, dict) or not dati_correttiva:
        return jsonify({'success': False, 'error': 'Dati JSON mancanti o non validi.'}), 400

    # 1. Recupera la stringa del nome utente
    nome_utente_autore = get_username_from_session()
    
    try:
        service_instance = get_correttiva_service()
        
        # 2. Chiama il Service
        nuovo_id = service_instance.salva_nuova_correttiva(
            dati_correttiva=dati_correttiva,
            nome_utente_autore=nome_utente_autore
        )
        
        # 3. Risposta di Successo
        return jsonify({
            'success': True,
            'message': f'Correttiva creata con successo. ID: {nuovo_id}.',
            'id': nuovo_id
        }), 200

    except ValueError as e:
        # Errore di validazione (es. dati mancanti o formato data errato)
        return jsonify({'success': False, 'error': f"Errore di validazione: {str(e)}"}), 400
    except Exception as e:
        logging.exception("Errore nel salvataggio della nuova correttiva")
        return jsonify({'success': False, 'error': f"Errore server: {str(e)}"}), 500
    
# ======================================================================
# ROTTA: Verifica Correttiva Attiva per Domanda (GET)
# ======================================================================
@correttiva_controller.route(
    "/api/correttiva/check_active/<int:id_pqd>", methods=['GET']
)
def check_active_correttiva_route(id_pqd):
    try:
        service_instance = get_correttiva_service()
        
        # 1. Chiama il Service
        is_active = service_instance.verifica_correttiva_attiva(id_pqd=id_pqd)
        
        # 2. Risposta JSON
        return jsonify({
            'success': True,
            'is_active': is_active
        }), 200

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logging.exception("Errore nella verifica della correttiva attiva")
        return jsonify({'success': False, 'error': f"Errore server: {str(e)}"}), 500
    
# ======================================================================
# ROTTA: Lista Correttive per Domanda (usata nella modal Correttiva)
# ======================================================================
@correttiva_controller.route(
    "/api/correttiva/lista_per_domanda/<int:id_pqd>", methods=['GET']
)
def lista_correttive_per_domanda_route(id_pqd):
    try:
        service_instance = get_correttiva_service()
        
        # 1. Chiama il Service
        lista_correttive = service_instance.get_lista_correttive(id_pqd=id_pqd)
        
        # 2. Risposta JSON
        return jsonify({
            'success': True,
            'correttive': lista_correttive
        }), 200

    except Exception as e:
        logging.exception("Errore nel recupero della lista correttive")
        return jsonify({'success': False, 'error': f"Errore server: {str(e)}"}), 500
    

# ======================================================================
# Dettaglio Correttiva per ID (usata per l'Edit)
# ======================================================================
@correttiva_controller.route(
    "/api/correttiva/dettaglio/<int:correttiva_id>", methods=['GET']
)
def get_correttiva_dettaglio_route(correttiva_id):
    try:
        service_instance = get_correttiva_service()
        
        # 1. Chiama il Service per recuperare il dettaglio
        dettaglio_correttiva = service_instance.get_dettaglio_correttiva(correttiva_id=correttiva_id)
        
        # 2. Gestisce il caso in cui il record non sia trovato
        if not dettaglio_correttiva:
            return jsonify({
                'success': False, 
                'error': f'Correttiva ID {correttiva_id} non trovata.'
            }), 404
        
        # 3. Risposta JSON
        return jsonify({
            'success': True,
            'dettaglio': dettaglio_correttiva
        }), 200

    except Exception as e:
        logging.exception(f"Errore nel recupero del dettaglio correttiva ID {correttiva_id}")
        return jsonify({'success': False, 'error': f"Errore server: {str(e)}"}), 500