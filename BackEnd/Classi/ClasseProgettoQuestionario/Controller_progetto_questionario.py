# File: Classi/ClasseProgettoQuestionario/Controller_progetto_questionario.py
# -*- coding: utf-8 -*-
import logging
import sys
from flask import Blueprint, jsonify, request, session, abort

# 1. Importa i Service e le funzioni di supporto (Assicurati che i percorsi siano corretti)
from Classi.ClasseProgettoQuestionario.Service_progetto_questionario import ServiceProgettoQuestionario
# Assumiamo che la funzione per recuperare l'username si trovi qui o in un file di utility comune
from Classi.ClasseRisposteCliente.Controller_risposta_cliente import get_username_from_session 
# dalla repository o service se necessario
from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario 

# ----------------------------------------------------------------------
# HELPER: Funzione per accedere all'istanza del Service
# (Devi assicurarti che sia inizializzata in server.py)
# ----------------------------------------------------------------------
def get_progetto_questionario_service():
    """Helper per accedere all'istanza del service inizializzata in server.py."""
    try:
        # Tenta di accedere al service iniettato nel modulo principale (server.py)
        return sys.modules['server'].service_progetto_questionario
    except (AttributeError, KeyError):
        logging.error("Istanza service_progetto_questionario non trovata in 'server'. Creazione di una nuova istanza.")
        return ServiceProgettoQuestionario()

# ----------------------------------------------------------------------
# DEFINIZIONE BLUEPRINT
# ----------------------------------------------------------------------
progetto_questionario_bp = Blueprint('progetto_questionario', __name__)
logging.basicConfig(level=logging.INFO)

# ======================================================================
# ROTTA API: Dettaglio Report Questionario (GET)
# ======================================================================
@progetto_questionario_bp.route("/api/dettaglio_report/<int:id_progetto_questionario>", methods=['GET'])
# Se usi una decoratore per la login, aggiungilo qui, es: @login_required 
def dettaglio_report_api(id_progetto_questionario):
    """
    Recupera il dettaglio del questionario (domande e risposte possibili)
    e la risposta salvata dall'utente loggato.
    """
    try:
        # 🟢 1. Recupera la stringa utente per il filtro (stringa MODIFICATO_DA)
        nome_utente_autore = get_username_from_session() 
        
        if nome_utente_autore == "ANONIMO":
             # Blocca l'accesso se l'utente non è autenticato/identificabile
             return jsonify({'success': False, 'error': 'Accesso negato: Utente non autenticato o non identificabile.'}), 401
             
        service_instance = get_progetto_questionario_service() 

        # 🟢 2. Chiama il Service, PASSANDO IL nome_utente_autore
        data = service_instance.get_dettaglio_report(
            id_progetto_questionario=id_progetto_questionario,
            nome_utente_autore=nome_utente_autore 
        )
        
        # 3. Restituisce la struttura dati JSON al frontend
        return jsonify(data), 200
        
    except Exception as e:
        # Logga l'errore completo per debugging lato server
        logging.exception(f"Errore API dettaglio report per ID {id_progetto_questionario} e utente {nome_utente_autore}")
        return jsonify({'success': False, 'error': f'Errore interno: la lista non è disponibile ({str(e)}).'}), 500

# ======================================================================
# ROTTA ESISTENTE (Esempio: Associazione Questionario)
# ======================================================================
@progetto_questionario_bp.route("/api/progetto_questionario/associa", methods=['POST'])
def associa_questionario_api():
    """
    Associa un questionario a un progetto.
    """
    data = request.get_json()
    if not data or 'id_progetto' not in data or 'id_questionario' not in data or 'domande_gruppo_list' not in data:
        return jsonify({'error': 'Dati mancanti o non validi (id_progetto, id_questionario, domande_gruppo_list).'}), 400

    service_instance = get_progetto_questionario_service()
    
    try:
        # Chiama il service per l'associazione
        result, status_code = service_instance.associate_questionario(
            id_progetto=data['id_progetto'],
            id_questionario=data['id_questionario'],
            domande_gruppo_list=data['domande_gruppo_list']
        )
        return jsonify(result), status_code
    except Exception as e:
        logging.error(f"Errore API nell'associazione questionario: {str(e)}")
        return jsonify({'error': 'Errore nell\'associazione del questionario al progetto.'}), 500