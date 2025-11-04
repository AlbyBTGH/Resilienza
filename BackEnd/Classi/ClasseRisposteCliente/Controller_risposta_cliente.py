# File: Classi/ClasseRisposteCliente/Controller_risposta_cliente.py
# -*- coding: utf-8 -*-
import sys
import logging
from flask import Blueprint, jsonify, request, session
from Classi.ClasseDB.db_connection import SessionLocal 
from Classi.ClasseRisposteCliente.Service_risposta_cliente import ServiceRispostaCliente
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti # Assumendo questo path

def get_risposta_cliente_service():
    """Helper per accedere all'istanza del service inizializzata in server.py."""
    try:
        return sys.modules['server'].service_risposta_cliente
    except (AttributeError, KeyError):
        logging.error("Istanza service_risposta_cliente non trovata.")
        return ServiceRispostaCliente() 
    
def get_username_from_session():
    """Recupera il nome utente (Stringa) da usare per MODIFICATO_DA."""
    user_id = session.get('user_id') 
    
    if user_id is None:
        # Placeholder se l'utente non è loggato
        return "ANONIMO"
    
    db_session = SessionLocal()
    try:
        utente = db_session.query(TUtenti).filter(TUtenti.id == user_id).first()
        # Restituisce l'email o un identificatore testuale
        return utente.email if utente and hasattr(utente, 'email') else f"Utente ID:{user_id}"
    except Exception:
        logging.exception(f"Errore nel recupero username per ID {user_id}")
        return f"Utente ID:{user_id}_ERRORE"
    finally:
        db_session.close()

# Definisce il Blueprint
risposta_cliente_controller = Blueprint('risposta_cliente', __name__)
logging.basicConfig(level=logging.INFO)

# ======================================================================
# ROTTA: Salvataggio Massivo di Risposte (POST)
# ======================================================================
@risposta_cliente_controller.route(
    "/api/risposta_cliente/salva_risposte_massive", methods=['POST']
)
def salva_risposte_massive_route():
    risposte_list = request.get_json() 
    
    if not isinstance(risposte_list, list) or not risposte_list:
        return jsonify({'success': False, 'error': 'Dati JSON mancanti o non validi.'}), 400

    # 1. Recupera la stringa del nome utente
    nome_utente_autore = get_username_from_session()
    
    try:
        service_instance = get_risposta_cliente_service()
        
        # 2. Chiama il Service
        service_instance.salva_risposte_massive(
            risposte_list=risposte_list,
            nome_utente_autore=nome_utente_autore
        )
        
        # 3. Risposta di Successo
        return jsonify({
            'success': True,
            'message': f'{len(risposte_list)} risposte salvate/aggiornate con successo da {nome_utente_autore}.'
        }), 200

    except Exception as e:
        logging.exception("Errore nel salvataggio risposte massive")
        return jsonify({'success': False, 'error': f"Errore server: {str(e)}"}), 500