# Classi/ClasseUtenti/Classe_t_utenti/Controller_t_utenti.py

from flask import Blueprint, request, jsonify
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
# <--- MODIFICATO QUI: Il nome della classe è 'Service_t_FunzionalitaUtente'
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import Service_t_FunzionalitaUtente 

t_utenti_controller = Blueprint('utenti', __name__)
service_t_utenti = Service_t_utenti()
service_t_funzionalita_utente = Service_t_FunzionalitaUtente() # <--- AGGIUNTA ISTANZA DEL SERVIZIO
