from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_funzionalita.Service_t_funzionalita import Service_t_funzionalita
from werkzeug.exceptions import NotFound

t_funzionalita_controller = Blueprint('funzionalita', __name__)
service_t_funzionalita = Service_t_funzionalita()

