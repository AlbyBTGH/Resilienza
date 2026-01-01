#  File: Classi/ClassePunteggi/Controller_progetto_questionario_punteggio.py
# -*- coding: utf-8 -*-
import sys
import logging
from flask import Blueprint, jsonify, request, render_template 
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
# ROTTA: Calcolo Punteggio Questionario (POST) - LOGICA VERSIONE
# ======================================================================
@punteggio_controller.route(
    "/api/punteggio/calcola/<int:id_progetto_questionario>", 
    methods=['POST']
)
def calcola_punteggio_route(id_progetto_questionario):
    
    service_instance = get_punteggi_service()
    
    try:
        # 1. RECUPERA I DATI ESISTENTI PER DETERMINARE LA VERSIONE (Baseline o Actual)
        baseline_punti = service_instance.get_punteggio_per_categorie(
            id_progetto_questionario=id_progetto_questionario,
            version='Baseline' # Cerchiamo solo se esiste già una Baseline
        )
        
        # 2. DETERMINAZIONE VERSIONE
        if baseline_punti and len(baseline_punti) > 0:
            version = 'Actual'
            log_message = f"Punteggi ricalcolati per Actual (ID: {id_progetto_questionario})."
        else:
            version = 'Baseline'
            log_message = f"Punteggi calcolati e salvati come Baseline (ID: {id_progetto_questionario})."
        
        # Log di debug per verificare la scelta
        logging.info(f"DEBUG_CALCOLO: Versione determinata: {version}. Trovate {len(baseline_punti)} righe Baseline.")

        # 3. Esegue il calcolo e salvataggio
        risultati = service_instance.calcola_e_salva_punteggio(
            id_progetto_questionario=id_progetto_questionario,
            version=version # Usa la versione appena determinata
        )
        
        logging.info(f"Controller: Calcolo completato. Righe affette: {risultati.get('rows_affected', 0)}")
        return jsonify({'success': True, 'message': f"Punteggio ({version}) calcolato e salvato.", 'data': risultati}), 200

    except Exception as e:
        # Gestione critica degli errori: Assicura un ritorno JSON (Fix Bad Request)
        logging.error(f"ERRORE CRITICO Controller in calcola_punteggio_route per ID {id_progetto_questionario}: {e}", exc_info=True)
        return jsonify({'success': False, 'error': f'Errore durante il calcolo del punteggio. Controllare i log del server.'}), 500

# ======================================================================
# ROTTA: Dati Grafico Radar Punteggio (GET) - LOGICA FILTRO VERSIONE
# ======================================================================
@punteggio_controller.route(
    "/api/punteggio/grafico_radar/<int:id_progetto_questionario>", 
    methods=['GET']
)
def get_grafico_radar_data_route(id_progetto_questionario):
    """
    Recupera e formatta i dati di punteggio per categorie per il grafico radar,
    aggruppando sia Baseline che Actual in un formato a doppia serie.
    """        
    try:
        service_instance = get_punteggi_service()
        
        # 1. Chiama il Service/Repository per recuperare TUTTI i dati (Baseline e Actual)
        # Il Repository deve restituire una lista di dict con chiavi: 'nome_categoria', 'peso_totale', 'versione'
        dati_grezzi = service_instance.get_punteggio_per_categorie( 
            id_progetto_questionario=id_progetto_questionario,
            version=None 
        )
        
        # Se non ci sono dati grezzi, restituisci la struttura vuota attesa dal Frontend
        if not dati_grezzi:
            return jsonify({'success': True, 'data': {'labels': [], 'series': []}}), 200
            
        # 2. Trasformazione e separazione dei dati
        labels = []
        baseline_map = {} 
        actual_map = {}   
        
        for item in dati_grezzi:
            categoria = item.get('nome_categoria')
            punteggio = item.get('peso_totale')
            versione = item.get('versione') # <-- CERCA QUESTA CHIAVE (DEVE ARRIVARE DAL REPOSITORY)
            
            # Controllo di robustezza per dati incompleti e per la versione (usa .lower() per sicurezza)
            if not categoria or not versione:
                continue

            if categoria not in labels:
                labels.append(categoria)
            
            if versione.lower() == 'baseline':
                baseline_map[categoria] = punteggio
            elif versione.lower() == 'actual':
                actual_map[categoria] = punteggio

        # 3. Costruisce l'array finale delle serie per Chart.js
        series = []
        
        # Serie Baseline (viene aggiunta solo se esistono dati Baseline)
        if baseline_map:
            series.append({
                'name': 'Baseline',
                'data': [baseline_map.get(label, 0) for label in labels] 
            })

        # Serie Actual (viene aggiunta solo se esistono dati Actual)
        if actual_map:
            series.append({
                'name': 'Actual',
                'data': [actual_map.get(label, 0) for label in labels] 
            })
            
        # 4. Restituisce il JSON strutturato
        dati_per_grafico = {
            'labels': labels,
            'series': series
        }
        
        return jsonify({'success': True, 'data': dati_per_grafico}), 200
        
    except Exception as e:
        # Gestione dell'errore server
        import logging
        logging.error(f"Errore critico nel recupero dati grafico radar: {e}", exc_info=True)
        return jsonify({'success': False, 'error': "Errore interno server nel recupero dati grafico."}), 500

# ======================================================================
# ROTTA: Pagina Dettaglio Report (GET) - LOGICA DETERMINAZIONE VERSIONE
# ======================================================================
@punteggio_controller.route("/dettaglio_report/<int:id_progetto_questionario>", methods=['GET'])
def dettaglio_questionario_report_page(id_progetto_questionario):
    """
    Renderizza la pagina di dettaglio del questionario e report, determinando la 
    prossima versione da calcolare ('Baseline' o 'Actual').
    """
    service_instance = get_punteggi_service()
    
    # 1. Recupera i punteggi esistenti per vedere se la Baseline è stata salvata
    # Usiamo il filtro 'Baseline' per vedere se esiste già
    baseline_punti = service_instance.get_punteggio_per_categorie(
        id_progetto_questionario=id_progetto_questionario,
        version='Baseline'
    )
    
    # 2. Definisce la versione corrente: se esiste una Baseline, la prossima è Actual
    if baseline_punti and len(baseline_punti) > 0:
        versione_corrente = 'Actual'
    else:
        versione_corrente = 'Baseline'
        
    # Restituisce la variabile 'versione_corrente' al template Jinja2
    return render_template(
        "dettaglio_questionario_report.html", 
        id_progetto_questionario=id_progetto_questionario,
        versione_corrente=versione_corrente # ⭐ VARIABILE AGGIUNTA PER IL FRONTEND
    )

# ======================================================================
# ROTTA: Dashboard Questionario (GET) - FIX BuildError
# ======================================================================
@punteggio_controller.route("/dashboard_questionario/<int:id_progetto_questionario>", methods=['GET'])
def dashboard_questionario_page(id_progetto_questionario):
    """
    Rotta reintegrata per risolvere il BuildError nel template. 
    Renderizza la pagina della dashboard (grafici).
    """
    # Assumendo che esista un template 'dashboard_questionario.html'
    return render_template(
        "dashboard_questionario.html", 
        id_progetto_questionario=id_progetto_questionario
    )

# ======================================================================
# ROTTA API: Recupera i dati del Punteggio Radar per una specifica VERSIONE
# ======================================================================
@punteggio_controller.route(
    "/api/punteggio/grafico_radar/<int:id_progetto_questionario>/<string:version>", 
    methods=['GET']
)
def get_punteggio_radar_by_version(id_progetto_questionario, version):
    """
    Restituisce i dati del punteggio (etichette e valori) per una singola versione.
    Utilizzata per disegnare due grafici separati (Baseline e Actual).
    """
    service_instance = get_punteggi_service()
    
    if version not in ['Baseline', 'Actual']:
        return jsonify({"success": False, "error": "Versione non valida."}), 400

    try:
        # Chiama il Service con il filtro versione
        dati_grezzi = service_instance.get_punteggio_per_categorie(
            id_progetto_questionario=id_progetto_questionario,
            version=version # Passa la versione specifica
        )
        
        # Prepara la struttura dati per Chart.js (singola serie)
        labels = [d['nome_categoria'] for d in dati_grezzi]
        punteggi = [d['peso_totale'] for d in dati_grezzi]
        
        # Ritorna i dati in un formato semplice
        return jsonify({
            "success": True, 
            "data": {
                "labels": labels, 
                "punteggi": punteggi,
                "version": version
            }
        })

    except Exception as e:
        logging.error(f"Errore Controller recupero punteggio radar ({version}): {e}")
        return jsonify({"success": False, "error": "Errore nel recupero dati."}), 500