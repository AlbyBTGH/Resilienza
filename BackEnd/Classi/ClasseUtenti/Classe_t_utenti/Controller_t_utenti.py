# Classi/ClasseUtenti/Classe_t_utenti/Controller_t_utenti.py

from flask import Blueprint, request, jsonify
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import Service_t_FunzionalitaUtente 
import logging

t_utenti_controller = Blueprint('utenti', __name__)
service_t_utenti = Service_t_utenti()
service_t_funzionalita_utente = Service_t_FunzionalitaUtente() # <--- AGGIUNTA ISTANZA DEL SERVIZIO

# ========================================================================
# 🔹 NUOVO ENDPOINT: GET /analisti
# ========================================================================
@t_utenti_controller.route("/analisti", methods=['GET'])
def get_analisti():
    """
    API che restituisce la lista di tutti gli utenti con ruolo 'Analista'
    per popolare la checklist della Modal.
    Endpoint atteso dal frontend: /api/utenti/analisti
    """
    logging.info("Richiesta GET per la lista di tutti gli analisti.")
    try:
        # Chiama il Service per ottenere la lista serializzata degli analisti
        # ⭐ Questa funzione deve essere implementata in Service_t_utenti.py
        analisti = service_t_utenti.get_all_analisti() 
        return jsonify(analisti), 200
    except Exception as e:
        logging.error(f"Errore nel recupero degli analisti (Controller): {e}")
        # Restituisce un errore generico al client
        return jsonify({"error": "Errore interno del server nel recupero analisti."}), 500