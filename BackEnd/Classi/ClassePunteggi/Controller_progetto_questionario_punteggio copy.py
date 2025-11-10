#  File: Classi/ClassePunteggi/Controller_progetto_questionario_punteggio.py
# -*- coding: utf-8 -*-
import sys
import logging
from flask import Blueprint, jsonify, request
# Importa il Service dedicato
from Classi.ClassePunteggi.Service_progetto_questionario_punteggio import ServiceProgettoQuestionarioPunteggio


# Funzione Helper per ottenere l'istanza del Service
def get_punteggi_service():
    """Helper per accedere all'istanza del service inizializzata in server.py."""
    try:
        # Assumendo che il service sia inizializzato in server.py come 'service_punteggi'
        return sys.modules['server'].service_punteggi
    except (AttributeError, KeyError):
        logging.error("Istanza service_punteggi non trovata. Creazione temporanea.")
        return ServiceProgettoQuestionarioPunteggio() 


# Definisce il Blueprint per le API dei punteggi
punteggio_controller = Blueprint('punteggio', __name__)
logging.basicConfig(level=logging.INFO)


# ======================================================================
# ROTTA: Calcolo Punteggio Questionario (POST) - (Rimane invariata)
# ======================================================================
@punteggio_controller.route(
    "/api/punteggio/calcola/<int:id_progetto_questionario>", 
    methods=['POST']
)
def calcola_punteggio_route(id_progetto_questionario):
    
    if not id_progetto_questionario:
        return jsonify({'success': False, 'error': 'ID Progetto Questionario mancante o non valido.'}), 400
        
    try:
        service_instance = get_punteggi_service()
        
        # 1. Chiama il Service per calcolare e salvare
        risultati = service_instance.calcola_e_salva_punteggio(
            id_progetto_questionario=id_progetto_questionario
        )
        
        # 2. Risposta di Successo
        message = f"Calcolo e salvataggio punteggio completato per ID {id_progetto_questionario}. Righe inserite/aggiornate: {risultati.get('rows_affected', 0)}."
        logging.info(message)
        
        return jsonify({
            'success': True,
            'message': message,
            'risultati': risultati
        }), 200

    except Exception as e:
        logging.error(f"Errore interno del server durante il calcolo del punteggio per ID {id_progetto_questionario}: {e}")
        return jsonify({'success': False, 'error': f'Errore interno del server durante il calcolo del punteggio: {e}'}), 500


# ======================================================================
# ⭐ NUOVA ROTTA: Dati Grafico Radar Punteggio (GET)
# URL chiamato dal tuo frontend JavaScript: /api/punteggio/grafico_radar/<id>
# ======================================================================
@punteggio_controller.route(
    "/api/punteggio/grafico_radar/<int:id_progetto_questionario>", 
    methods=['GET']
)
def get_grafico_radar_data_route(id_progetto_questionario):
    """
    Recupera i dati aggregati (nome categoria e peso totale) per la visualizzazione 
    del grafico radar.
    """
    if not id_progetto_questionario:
        return jsonify({'success': False, 'error': 'ID Progetto Questionario mancante o non valido.'}), 400
        
    try:
        service_instance = get_punteggi_service()
        
        # Chiama il Service che a sua volta chiama il Repository
        dati_punteggio = service_instance.get_punteggio_per_categorie( 
            id_progetto_questionario=id_progetto_questionario
        )
        
        # Controlla se il Service ha restituito dati
        if not dati_punteggio or len(dati_punteggio) == 0:
            # Restituisce 404 se i dati non sono stati ancora calcolati o non sono presenti 
            # (questo attiverà il messaggio nel tuo frontend)
            return jsonify({'success': True, 'data': [], 'message': 'Nessun dato di punteggio trovato.'}), 404
            
        # Successo: restituisce i dati nel formato JSON atteso dal JavaScript
        return jsonify({'success': True, 'data': dati_punteggio}), 200
        
    except Exception as e:
        logging.error(f"Errore nel recupero dati grafico radar per ID {id_progetto_questionario}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500