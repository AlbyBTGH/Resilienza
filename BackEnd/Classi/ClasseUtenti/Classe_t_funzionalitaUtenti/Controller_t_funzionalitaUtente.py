# Classi/ClasseUtenti/Classe_t_funzionalitaUtenti/Controller_t_funzionalitaUtente.py

from flask import Blueprint, request
# <--- MODIFICATO QUI: Il nome della classe è 'Service_t_FunzionalitaUtente'
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import Service_t_FunzionalitaUtente 


t_funzionalitaUtenti_controller = Blueprint('funzionalita_utenti', __name__)
service_t_funz_utenti = Service_t_FunzionalitaUtente()

@t_funzionalitaUtenti_controller.route("/<int:funzionalita_utente_id>", methods=['GET'])
def get_funzionalita_utente(funzionalita_utente_id):  
    funzionalita_utente = service_t_funz_utenti.get_funzionalita_utente_by_id(funzionalita_utente_id)
    if funzionalita_utente:
        # Assicurati che i nomi delle chiavi nel dizionario siano coerenti con il tuo modello
        return {'id': funzionalita_utente['id'], 
                'fkRuolo': funzionalita_utente['fkRuolo'], # Modificato da fkTipoUtente a fkRuolo
                'fkFunzionalita': funzionalita_utente['fkFunzionalita'], 
                'permessi': funzionalita_utente['permessi']}
    else:
        return {'error': 'FunzionalitaUtente not found'}, 404

@t_funzionalitaUtenti_controller.route("/tipo_utente/<int:tipo_utente_id>", methods=['GET'])
def get_funzionalita_utenti_by_user_type(tipo_utente_id):
    funzionalita_utenti = service_t_funz_utenti.get_funz_utenti_by_user_type(tipo_utente_id) # Modificato nome metodo
    # Assicurati che i nomi delle chiavi nel dizionario siano coerenti con il tuo modello
    return [{'id': fu['id'], 'fkRuolo': fu['fkRuolo'], 'fkFunzionalita': fu['fkFunzionalita'], 'permessi': fu['permessi']} for fu in funzionalita_utenti] # Modificato da fkTipoUtente a fkRuolo

@t_funzionalitaUtenti_controller.route("/funzionalita/<int:funzionalita_id>", methods=['GET'])
def get_funzionalita_utenti_by_funzionalita(funzionalita_id):
    funzionalita_utenti = service_t_funz_utenti.get_funzionalita_utenti_by_funzionalita(funzionalita_id)
    return [{'id': fu.id, 'fkTipoUtente': fu.fkTipoUtente, 'fkFunzionalita': fu.fkFunzionalita, 'permessi': fu.permessi} for fu in funzionalita_utenti]