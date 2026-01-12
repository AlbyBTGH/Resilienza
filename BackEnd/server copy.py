# -*- coding: utf-8 -*-
import calendar
import pprint
import logging
import pandas as pd
import io
import sys
from datetime import datetime, date
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from apscheduler.schedulers.background import BackgroundScheduler
from flask import (
    Flask,
    jsonify,
    Blueprint,
    request,
    session,
    render_template,
    redirect,
    url_for,
    flash,
    abort,
)
from flask_cors import CORS
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from sqlalchemy import text
from sqlalchemy.orm import joinedload

# -------------------
# DATABASE / ORM
# -------------------
from Classi.ClasseDB.db_connection import Base, engine, SessionLocal

# -------------------
# UTENTI / RUOLI / FUNZIONALITA
# -------------------
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti
from Classi.ClasseUtenti.Classe_t_ruolo.Domain_t_ruolo import TRuolo
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Domain_t_funzionalitaUtente import TFunzionalitaUtente

# -------------------
# MENU
# -------------------
from Classi.Classe_menu_principale.Domain_t_menu_principale import TMenuPrincipale

# -------------------
# AMBITO / CATEGORIA / DRIVER / DOMANDA
# -------------------
from Classi.ClasseAnagrafica.ClasseAmbito.Domain_t_ambito import TAmbito
from Classi.ClasseAnagrafica.ClasseCategoria.Domain_t_categoria import TCategoria
from Classi.ClasseAnagrafica.ClasseDriver.Domain_t_driver import TDriver
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda

# -------------------
# GRUPPO RISPOSTA
# -------------------
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Domain_t_gruppo_risposta import TGruppoRisposta

# -------------------
# CARICAMENTO DATI
# -------------------
from Classi.Classe_dati_caricamento.Domain_t_dati_caricamento import TDatiCaricamento

# -------------------
# PROGETTI / QUESTIONARI
# -------------------
from Classi.ClasseAnagrafica.ClasseProgetto.Domain_t_progetto import TProgetto
from Classi.ClasseAnagrafica.ClasseStatoProgetto.Domain_t_stato_progetto import TStatoProgetto
from Classi.ClasseAnagrafica.ClasseCliente.Domain_t_cliente import TCliente
from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario
from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda
from Classi.ClasseQuestionario.Domain_t_questionario import TQuestionario

# -------------------
# CONTROLLER
# -------------------
from Classi.ClasseAnagrafica.ClasseAmbito.Controller_t_ambito import t_ambito_controller
from Classi.ClasseAnagrafica.ClasseCategoria.Controller_t_categoria import t_categoria_controller
from Classi.ClasseAnagrafica.ClasseDriver.Controller_t_driver import t_driver_controller
from Classi.ClasseAnagrafica.ClasseDomanda.Controller_t_domanda import t_domanda_controller
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Controller_t_gruppo_risposta import t_gruppo_risposta_controller
from Classi.ClasseAnagrafica.ClasseProgetto.Controller_t_progetto import t_progetto_controller
from Classi.ClasseAnagrafica.ClasseStatoProgetto.Controller_stati_progetto import t_stato_progetto_controller
from Classi.ClasseQuestionario.Controller_t_questionario import t_questionario_controller
from Classi.ClasseAnagrafica.ClasseRisposta.Controller_t_risposta import t_risposta_controller
from Classi.ClasseAnagrafica.ClasseCliente.Controller_t_cliente import t_cliente_controller

# -------------------
# SERVICE / REPOSITORY
# -------------------
from Classi.Classe_menu_principale.Service_t_menu_principale import Service_t_menu_principale
from Classi.ClasseUtenti.Classe_t_funzionalita.Service_t_funzionalita import Service_t_funzionalita
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import Service_t_FunzionalitaUtente
from Classi.ClasseUtenti.Classe_t_utenti.Repository_t_utenti import Repository_t_utenti
from Classi.ClasseUtenti.Classe_t_ruolo.Repository_t_ruolo import Repository_t_ruolo
from Classi.ClasseAnagrafica.ClasseAmbito.Service_t_ambito import Service_t_ambito
from Classi.ClasseAnagrafica.ClasseCategoria.Service_t_categoria import Service_t_categoria
from Classi.ClasseAnagrafica.ClasseDriver.Service_t_driver import Service_t_driver
from Classi.ClasseAnagrafica.ClasseDomanda.Service_t_domanda import Service_t_domanda
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Service_t_gruppo_risposta import Service_t_gruppo_risposta
from Classi.Classe_dati_caricamento.Service_t_dati_caricamento import ServiceTDatiCaricamento
from Classi.ClasseAnagrafica.ClasseProgetto.Service_t_progetto import Service_t_progetto
from Classi.ClasseAnagrafica.ClasseRisposta.Service_t_risposta import Service_t_risposta 
from Classi.ClasseProgettoQuestionario.Service_progetto_questionario import ServiceProgettoQuestionario

from Classi.ClasseRisposteCliente.Service_risposta_cliente import ServiceRispostaCliente
from Classi.ClasseRisposteCliente.Controller_risposta_cliente import risposta_cliente_controller

from Classi.ClassePunteggi.Service_progetto_questionario_punteggio import ServiceProgettoQuestionarioPunteggio
from Classi.ClassePunteggi.Controller_progetto_questionario_punteggio import punteggio_controller

from Classi.ClasseCorrettive.Service_correttiva import ServiceCorrettiva 
from Classi.ClasseCorrettive.Controller_correttiva import correttiva_controller

from Classi.ClasseUtenti.Classe_t_utenti.Controller_t_utenti import t_utenti_controller

# Inizializzazione del logging
logging.basicConfig(level=logging.INFO)

# Inizializzazione di Blueprint e CSRFProtect
appBT = Blueprint('appBT', __name__, url_prefix='/')
csrf = CSRFProtect()
CORS(appBT) # Abilita CORS per il Blueprint

# Inizializzazione dei repository e servizi
repository_t_utenti = Repository_t_utenti()
service_t_menu_principale = Service_t_menu_principale()
service_t_funzionalita = Service_t_funzionalita()
service_t_funzionalita_utente = Service_t_FunzionalitaUtente()
repository_t_ruolo = Repository_t_ruolo()
service_t_ambito = Service_t_ambito()
service_t_categoria = Service_t_categoria()
service_t_driver = Service_t_driver() # Istanza del servizio Driver
service_t_domanda = Service_t_domanda() # Istanza del servizio Domanda
service_t_gruppo_risposta = Service_t_gruppo_risposta()

service_t_dati_caricamento = ServiceTDatiCaricamento() # AGGIUNTO

# Istanzia il servizio per la gestione dei progetti
service_t_progetto = Service_t_progetto()

service_progetto_questionario = ServiceProgettoQuestionario()

service_t_risposta = Service_t_risposta()
service_t_risposta.create_table_if_not_exists()

service_risposta_cliente = ServiceRispostaCliente()

service_punteggi = ServiceProgettoQuestionarioPunteggio()
sys.modules[__name__].service_punteggi = service_punteggi


# Definisci la classe del form di login
class LoginFormNoCSRF(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Accedi')


# Decoratore personalizzato per richiedere il login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Devi effettuare il login per accedere a questa pagina.', 'warning')
            return redirect(url_for('appBT.login'))
        return f(*args, **kwargs)
    return decorated_function


# Gestore errori 404
@appBT.errorhandler(404)
def error_404(e):
    logging.exception("Pagina non trovata:")
    return (
        render_template(
            "error.html",
            error_code=404,
            error_message="La pagina richiesta non è stata trovata.",
        ),
        404,
    )


# Gestore errori 500
@appBT.errorhandler(500)
def error_500(e):
    logging.exception("Errore interno del server:")
    return (
        render_template(
            "error.html",
            error_code=500,
            error_message="Si è verificato un errore interno del server. Riprova più tardi.",
        ),
        500,
    )


# Rotta della pagina di login
@appBT.route('/login', methods=['GET', 'POST'])
def login():
    print("DEBUG: Sono nella funzione login!")
    form = LoginFormNoCSRF()
    print(f"DEBUG: Metodo richiesta: {request.method}")

    if form.validate_on_submit():
        print("DEBUG: Form validato, tentativo di login...")
        email = form.email.data
        password = form.password.data
        print(f"DEBUG: Email inserita: {email}")

        user = repository_t_utenti.get_user_by_email(email) # Questo metodo dovrebbe restituire un oggetto TUtenti
        print(f"DEBUG: Utente recuperato da DB: {user.email if user else 'Nessun utente trovato'}")

        if user:
            print(f"DEBUG: Password hash dell'utente nel DB: {user.password}")
            print(f"DEBUG: Password inserita (non hashata): {password}")
            password_match = check_password_hash(user.password, password)
            print(f"DEBUG: Risultato confronto password: {password_match}")
        else:
            password_match = False

        if user and password_match:
            user_role_obj = repository_t_ruolo.get_by_id(user.fkIdRuolo)
            print(f"DEBUG: Ruolo utente recuperato: {user_role_obj.DESCR if user_role_obj else 'Non trovato'}")

            if user_role_obj:
                session['logged_in'] = True
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['username'] = user.username
                session['user_role_id'] = user_role_obj.ID
                session['user_role_descr'] = user_role_obj.DESCR

                repository_t_utenti.update_user_last_access(user)

                flash('Login avvenuto con successo!', 'success')
                print(f"DEBUG: Login riuscito per {user.email}, reindirizzo a index.")
                return redirect(url_for('appBT.index'))
            else:
                flash('Errore interno: Ruolo utente non configurato nel sistema.', 'danger')
                print("ERRORE: Login fallito: Ruolo utente non trovato nel database.")
        else:
            flash('Utente non abilitato o credenziali non valide.', 'danger')
            print("DEBUG: Login fallito: credenziali non valide o utente non abilitato.")

    print("DEBUG: Rendering login.html")
    return render_template("login.html", form=form)


# Rotta di logout
@appBT.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('username', None)
    session.pop('user_role_id', None)
    session.pop('user_role_descr', None)
    flash('Sei stato disconnesso.', 'info')
    return redirect(url_for('appBT.login'))


# Rotta della pagina di registrazione (da implementare se necessaria)
@appBT.route('/registrati')
def registrati():
    flash('La funzionalità di registrazione non è ancora disponibile.', 'info')
    return redirect(url_for('appBT.login'))


# Rotta principale con menu dinamico
@appBT.route("/")
@login_required
def index():
    """
    Renderizza la pagina principale con un menu dinamico basato sul ruolo dell'utente.
    """
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
        # Add a debug print here to inspect the menu data
        print("DEBUG: Dynamic Menu Data for index page:")
        pprint.pprint(dynamic_menu) # Use pprint for better readability
    else:
        dynamic_menu = []
        print("DEBUG: Ruolo utente non definito in sessione per index page. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf()

    return render_template(
        "index.html",
        title="Applicazione Resilienza",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token
    )

# Nuova rotta per la pagina di gestione Ambito
@appBT.route("/ambito")
@login_required
def ambito_page():
    """
    Renderizza la pagina di gestione dell'anagrafica Ambito.
    Passa i dati necessari per il menu dinamico e il token CSRF.
    """
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per ambito_page. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf() 
    
    return render_template(
        "ambito.html",
        title="Gestione Ambiti",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token
    )

# Nuova rotta per la pagina di gestione Categoria
@appBT.route("/categoria")
@login_required
def categoria_page():
    """
    Renderizza la pagina di gestione dell'anagrafica Categoria.
    Passa i dati necessari per il menu dinamico e il token CSRF.
    """
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per categoria_page. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf() 
    
    return render_template(
        "categoria.html",
        title="Gestione Categorie",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token
    )

# Nuova rotta per la pagina di gestione Driver
@appBT.route("/driver")
@login_required
def driver_page():
    """
    Renderizza la pagina di gestione dell'anagrafica Driver.
    Passa i dati necessari per il menu dinamico e il token CSRF.
    """
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per driver_page. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf() 
    
    return render_template(
        "driver.html",
        title="Gestione Driver",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_user_role_descr,
        csrf_token=csrf_token
    )

# Nuova rotta per la pagina di gestione Domanda
@appBT.route("/domanda")
@login_required
def domanda_page():
    """
    Renderizza la pagina di gestione dell'anagrafica Domanda.
    Passa i dati necessari per il menu dinamico e il token CSRF.
    """
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per domanda_page. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf() 
    
    return render_template(
        "domanda.html",
        title="Gestione Domande",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token
    )


# rotta per la pagina di SOLA FRUIZIONE Domande (layout piu efficiente)
@appBT.route("/fruizione_domande")
@login_required
def fruizione_domande_page():
    """
    Renderizza la pagina di visualizzazione moderna e raggruppata delle domande.
    """
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf() 
    
    return render_template(
        "fruizione_domande.html",
        title="Esplora Catalogo Domande",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token
    )


# ### INIZIO AGGIUNTA PER GRUPPO_RISPOSTA ###
@appBT.route("/gruppo_risposta")
@login_required
def gruppo_risposta_page():
    """
    Renderizza la pagina di gestione dell'anagrafica Gruppo Risposta.
    Passa i dati necessari per il menu dinamico e il token CSRF.
    """
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per gruppo_risposta_page. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf() 
    
    return render_template(
        "gruppo_risposta.html",
        title="Gestione Gruppi Risposta",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token
    )
# ### FINE AGGIUNTA PER GRUPPO_RISPOSTA ###


# --- ROTTE PER CARICAMENTO DOMANDE --- # AGGIUNTO
@appBT.route('/caricamento_domande')
@login_required
def caricamento_domande_page():
    """Renderizza la pagina per il caricamento massivo delle domande."""
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    
    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf()

    return render_template(
        'caricamento_domande.html',
        title="Caricamento Domande",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token
    )

@appBT.route('/caricamenti_log')
@login_required
def visualizza_caricamenti():
    """
    Pagina per visualizzare i log dei caricamenti massivi.
    """
    try:
        caricamenti = service_t_dati_caricamento.get_all_caricamenti()
        return render_template('visualizza_caricamenti.html', caricamenti=caricamenti)
    except Exception as e:
        print(f"ERRORE: Impossibile recuperare i dati dei caricamenti: {e}")
        flash("Errore nel recupero dei dati dei caricamenti.", "danger")
        return redirect(url_for('caricamento_domande'))
    
# ### route PROGETTI ###
@appBT.route("/progetti")
@login_required
def progetti_page():
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per progetti_page. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf()

    return render_template(
        "progetti.html",
        title="Gestione Progetti",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token
    )

# ### route CREA QUESTIONARIO ###
@appBT.route("/crea_questionario", methods=['GET'])
@login_required
def crea_questionario():
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per crea_questionario. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf()

    return render_template(
        "crea_questionario.html",
        title="Crea Questionario",
        menu_data=dynamic_menu,  # Questa è la riga fondamentale da modificare
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token
    )


# ### route GESTIONE QUESTIONARIO ###
@appBT.route('/gestione_questionario/<int:questionario_id>', methods=['GET'])
@login_required
def gestione_questionario(questionario_id):
    db_session = SessionLocal()
    questionario_descr = f"Questionario ID: {questionario_id}"

    try:
        # Recupera il questionario per ottenere la sua descrizione
        questionario = db_session.query(TQuestionario).filter(TQuestionario.id == questionario_id).one_or_none()

        if not questionario:
            flash("Questionario non trovato.", "danger")
            return redirect(url_for('appBT.dashboard_route'))
        else:
            questionario_descr = questionario.descr
        
    except Exception as e:
        print(f"ERRORE: Errore nel recupero del questionario per il titolo: {e}")
    finally:
        db_session.close()

    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per gestione_questionario. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf()

    return render_template(
        'gestione_questionario.html',
        title="Modifica Questionario",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token,
        questionario_id=questionario_id,
        questionario_descr=questionario_descr
    )


# Rotta per visualizzare la pagina di associazione Progetto <-> Questionario
@appBT.route("/associa_questionario_progetto")
@login_required
def associa_questionario_progetto_page():
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per associa_questionario_progetto_page. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf()

    return render_template(
        "associa_questionario_progetto.html",
        title="Associa Questionario a Progetto",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token
    )



# ### API GESTIONE QUESTIONARIO ###
@appBT.route('/api/questionario/<int:questionario_id>', methods=['GET'])
@login_required
def get_questionario_by_id(questionario_id):
    db_session = SessionLocal()
    try:
        # Caricamento gerarchico: Domanda -> Driver -> Categoria
        questionario = db_session.query(TQuestionario).options(
            joinedload(TQuestionario.domande)
                .joinedload(TDomanda.driver_rel)
                .joinedload(TDriver.categoria) # Usiamo 'categoria' come definito nel tuo relationship
        ).filter(TQuestionario.id == questionario_id).one_or_none()

        if not questionario:
            return jsonify({'error': 'Questionario non trovato'}), 404

        domande_selezionate = []
        for d in questionario.domande:
            # Recuperiamo le descrizioni risalendo la catena
            # d.driver_rel -> istanza di TDriver
            # d.driver_rel.categoria -> istanza di TCategoria
            cat_descr = d.driver_rel.categoria.descr if (d.driver_rel and d.driver_rel.categoria) else "N.D."
            driver_descr = d.driver_rel.descr if d.driver_rel else "N.D."

            domande_selezionate.append({
                'id': d.id,
                'descr': d.descr,
                'categoria_descr': cat_descr,
                'driver_descr': driver_descr
            })
        
        return jsonify({
            'id': questionario.id,
            'descr': questionario.descr,
            'domande': domande_selezionate
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

# ### API GESTIONE DOMANDE PER FRONTEND ###
@appBT.route('/api/domande/', methods=['GET'])
@login_required
def get_all_domande():
    """API per recuperare tutte le domande e il loro driver per il frontend."""
    session = SessionLocal()
    try:
        domande = session.query(TDomanda).options(joinedload(TDomanda.driver_rel)).all()
        
        domande_list = [
            {
                'id': domanda.id,
                'descr': domanda.descr,
                'id_driver': domanda.id_driver,
                'driver_descr': domanda.driver_rel.descr if domanda.driver_rel else 'N/A'
            }
            for domanda in domande
        ]
        return jsonify(domande_list), 200
    except Exception as e:
        print(f"ERRORE: Errore nel recupero delle domande: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ### API PER IL RECUPERO COMPLETO DELLE DOMANDE (per gestione_questionario) ###
@appBT.route('/api/domande_complete/', methods=['GET'])
@login_required
def get_domande_complete():
    session = SessionLocal()
    try:
        # Carichiamo anche la categoria associata al driver
        domande = session.query(TDomanda).options(
            joinedload(TDomanda.driver_rel).joinedload(TDriver.categoria)
        ).all()
        
        domande_list = []
        for d in domande:
            domande_list.append({
                'id': d.id,
                'descr': d.descr,
                'id_driver': d.id_driver,
                # Inseriamo qui i nomi testuali per il frontend
                'driver_descr': d.driver_rel.descr if d.driver_rel else "N.D.",
                'categoria_descr': d.driver_rel.categoria.descr if (d.driver_rel and d.driver_rel.categoria) else "N.D.",
                # Manteniamo l'oggetto originale se serve ad altre funzioni
                'driver_rel': {
                    'id': d.driver_rel.id, 
                    'descr': d.driver_rel.descr
                } if d.driver_rel else None
            })
        return jsonify(domande_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
        
# ### API UPDATE QUESTIONARIO ###
@appBT.route('/api/questionari/<int:questionario_id>', methods=['PUT'])
@login_required
def update_questionario(questionario_id):
    """API per aggiornare un questionario esistente."""
    session = SessionLocal()
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dati JSON mancanti'}), 400

        descr = data.get('descr')
        domande_ids = data.get('domande')

        if not descr or not domande_ids:
            return jsonify({'error': 'Descrizione o domande mancanti'}), 400
        
        questionario = session.query(TQuestionario).filter(TQuestionario.id == questionario_id).one_or_none()
        if not questionario:
            return jsonify({'error': 'Questionario non trovato'}), 404
        
        questionario.descr = descr
        
        # Aggiorna le domande associate
        domande_attuali = {d.id: d for d in questionario.domande}
        nuove_domande = session.query(TDomanda).filter(TDomanda.id.in_(domande_ids)).all()
        
        # Rimuovi le domande non più selezionate
        for domanda_id in list(domande_attuali.keys()):
            if domanda_id not in domande_ids:
                questionario.domande.remove(domande_attuali[domanda_id])
        
        # Aggiungi le nuove domande selezionate
        for domanda in nuove_domande:
            if domanda.id not in domande_attuali:
                questionario.domande.append(domanda)
        
        session.commit()
        return jsonify({'message': 'Questionario aggiornato con successo', 'id': questionario.id}), 200

    except Exception as e:
        session.rollback()
        print(f"ERRORE: Errore nell'aggiornamento del questionario: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ============================================
# API: Associa Questionario a Progetto (con domande collegate)
# ============================================
@appBT.route('/api/associa_questionario_progetto', methods=['POST'])
@login_required
def associa_questionario_progetto():
    """
    API per associare un questionario a un progetto e inserire automaticamente
    anche le domande associate nella tabella progetto_questionario_domanda.
    """
    db_session = SessionLocal()
    try:
        data = request.json
        if not data or 'id_progetto' not in data or 'id_questionario' not in data:
            return jsonify({'error': 'Parametri mancanti: id_progetto e id_questionario sono obbligatori'}), 400

        id_progetto = data['id_progetto']
        id_questionario = data['id_questionario']

        progetto = db_session.query(TProgetto).filter_by(id=id_progetto).one_or_none()
        questionario = db_session.query(TQuestionario).filter_by(id=id_questionario).one_or_none()

        if not progetto:
            return jsonify({'error': f'Progetto con ID {id_progetto} non trovato'}), 404
        if not questionario:
            return jsonify({'error': f'Questionario con ID {id_questionario} non trovato'}), 404

        # ⚙️ Controlla se l'associazione esiste già
        existing_assoc = (
            db_session.query(ProgettoQuestionario)
            .filter_by(id_progetto=id_progetto, id_questionario=id_questionario)
            .first()
        )
        if existing_assoc:
            return jsonify({'message': 'Il questionario è già associato a questo progetto'}), 200

        # ✅ Crea la nuova associazione principale
        nuova_associazione = ProgettoQuestionario(
            id_progetto=id_progetto,
            id_questionario=id_questionario
        )
        db_session.add(nuova_associazione)
        db_session.flush()  # serve per ottenere l’ID generato

        # 🧩 Recupera tutte le domande associate al questionario scelto
        query_domande = text("""
            SELECT dq.ID_DOMANDA, d.ID_GRUPPO_RISPOSTA
            FROM domande_questionario dq
            JOIN domande d ON dq.ID_DOMANDA = d.ID
            WHERE dq.ID_QUESTIONARIO = :idq
        """)
        domande = db_session.execute(query_domande, {'idq': id_questionario}).fetchall()        

        if not domande:
            db_session.rollback()
            return jsonify({'error': 'Nessuna domanda associata a questo questionario'}), 400

        # 🧱 Inserisce tutte le righe nella tabella progetto_questionario_domanda
        for id_domanda, id_gruppo_risposta in domande:
            if id_gruppo_risposta is not None:
                # Se il gruppo risposta è specificato, lo includiamo
                db_session.execute(
                    text("""
                        INSERT INTO progetto_questionario_domanda
                        (ID_PROGETTO_QUESTIONARIO, ID_DOMANDA, ID_GRUPPO_RISPOSTA)
                        VALUES (:id_pq, :id_domanda, :id_gr)
                    """),
                    {
                        'id_pq': nuova_associazione.id,
                        'id_domanda': id_domanda,
                        'id_gr': id_gruppo_risposta
                    }
                )
            else:
                # Se non c’è ancora un gruppo risposta, inseriamo solo progetto+domanda
                db_session.execute(
                    text("""
                        INSERT INTO progetto_questionario_domanda
                        (ID_PROGETTO_QUESTIONARIO, ID_DOMANDA)
                        VALUES (:id_pq, :id_domanda)
                    """),
                    {
                        'id_pq': nuova_associazione.id,
                        'id_domanda': id_domanda
                    }
                )

        db_session.commit()

        return jsonify({
            'message': 'Associazione creata con successo',
            'id_progetto': id_progetto,
            'id_questionario': id_questionario,
            'numero_domande_collegate': len(domande)
        }), 201

    except Exception as e:
        db_session.rollback()
        print(f"ERRORE: associa_questionario_progetto -> {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()


# ============================================
# API: Leggi tutte le associazioni progetto-questionario
# ============================================
@appBT.route('/api/associa_questionario_progetto', methods=['GET'])
@login_required
def get_associazioni_progetto_questionario():
    db_session = SessionLocal()
    try:
        associazioni = db_session.query(ProgettoQuestionario).all()
        result = []
        for a in associazioni:
            result.append({
                'ID': a.id,  # <-- usa 'id' invece di 'ID'
                'ID_PROGETTO': a.id_progetto,
                'descr_progetto': a.progetto.descr if a.progetto else '—',
                'ID_QUESTIONARIO': a.id_questionario,
                'descr_questionario': a.questionario.descr if a.questionario else '—'
            })
        return jsonify(result), 200
    except Exception as e:
        print(f"ERRORE: get_associazioni_progetto_questionario -> {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

# ============================================
# API: Rimuovi associazione progetto-questionario
# ============================================
@appBT.route('/api/associa_questionario_progetto', methods=['DELETE'])
@login_required
def delete_associazione_progetto_questionario():
    db_session = SessionLocal()
    try:
        data = request.json
        if not data or 'id_progetto' not in data or 'id_questionario' not in data:
            return jsonify({'error': 'Parametri mancanti: id_progetto e id_questionario sono obbligatori'}), 400

        id_progetto = data['id_progetto']
        id_questionario = data['id_questionario']

        associazione = db_session.query(ProgettoQuestionario).filter_by(
            id_progetto=id_progetto,
            id_questionario=id_questionario
        ).one_or_none()

        if not associazione:
            return jsonify({'error': 'Associazione non trovata'}), 404

        db_session.delete(associazione)
        db_session.commit()
        return jsonify({'message': 'Associazione rimossa con successo'}), 200

    except Exception as e:
        db_session.rollback()
        print(f"ERRORE: delete_associazione_progetto_questionario -> {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

# API per ottenere le domande associate a una specifica associazione progetto-questionario
@appBT.route('/api/progetto_questionario_domande/<int:id_progetto>/<int:id_questionario>', methods=['GET'])
@login_required
def get_domande_associazione(id_progetto, id_questionario):
    db_session = SessionLocal()
    try:
        # Recupera l'associazione progetto-questionario
        associazione = (
            db_session.query(ProgettoQuestionario)
            .filter_by(id_progetto=id_progetto, id_questionario=id_questionario)
            .one_or_none()
        )
        if not associazione:
            return jsonify({'error': 'Associazione non trovata'}), 404

        # Recupera tutte le domande associate
        domande = (
            db_session.query(TDomanda)
            .join(ProgettoQuestionarioDomanda, ProgettoQuestionarioDomanda.id_domanda == TDomanda.id)
            .filter(ProgettoQuestionarioDomanda.id_progetto_questionario == associazione.id)
            .all()
        )

        # 🔹 Recupera tutti i gruppi risposta (da mostrare nelle tendine)
        gruppi_risposta = db_session.query(TGruppoRisposta).all()
        gruppi_disponibili = [{'id': g.id, 'descr': g.descr} for g in gruppi_risposta]

        # 🔹 Crea l’elenco finale di domande + gruppo risposta attuale
        domande_list = []
        for d in domande:
            pq_domanda = (
                db_session.query(ProgettoQuestionarioDomanda)
                .filter_by(id_progetto_questionario=associazione.id, id_domanda=d.id)
                .one_or_none()
            )

            domande_list.append({
                'id_domanda': d.id,
                'descr_domanda': d.descr,
                'id_gruppo_risposta': pq_domanda.id_gruppo_risposta if pq_domanda else None,
                'gruppi_disponibili': gruppi_disponibili
            })

        return jsonify(domande_list), 200

    except Exception as e:
        db_session.rollback()
        print(f"ERRORE: get_domande_associazione -> {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        db_session.close()


# ============================================
# API: Associa / Aggiorna Gruppo Risposta per una domanda in un progetto-questionario
# ============================================
@appBT.route('/api/associa_gruppo_risposta_domanda', methods=['PUT'])
@login_required
def associa_gruppo_risposta_domanda():
    """
    Aggiorna l'id_gruppo_risposta per una specifica domanda
    associata a un progetto-questionario.
    Parametri JSON:
        - ID_PROGETTO_QUESTIONARIO: ID dell'associazione Progetto-Questionario
        - ID_DOMANDA: ID della domanda
        - ID_GRUPPO_RISPOSTA: ID del gruppo risposta da associare
    """
    db_session = SessionLocal()
    try:
        data = request.json
        print("DEBUG API - dati ricevuti:", data)  # 🔹 debug input

        if not data:
            return jsonify({'error': 'Dati JSON mancanti'}), 400

        # Recupero valori dal JSON
        id_pq = data.get('ID_PROGETTO_QUESTIONARIO')
        id_domanda = data.get('ID_DOMANDA')
        id_gruppo_risposta = data.get('ID_GRUPPO_RISPOSTA')

        print(f"DEBUG API - id_progetto_questionario: {id_pq}, id_domanda: {id_domanda}, id_gruppo_risposta: {id_gruppo_risposta}")

        if not id_pq or not id_domanda:
            return jsonify({'error': 'Parametri mancanti: ID_PROGETTO_QUESTIONARIO e ID_DOMANDA sono obbligatori'}), 400

        # 🔹 Converti in interi
        try:
            id_pq = int(id_pq)
            id_domanda = int(id_domanda)
            id_gruppo_risposta = int(id_gruppo_risposta) if id_gruppo_risposta else None
        except ValueError:
            return jsonify({'error': 'I parametri devono essere numerici'}), 400

        # 🔹 Usa gli attributi del modello, non i nomi colonne DB
        associazione = db_session.query(ProgettoQuestionarioDomanda).filter_by(
            id_progetto_questionario=id_pq,
            id_domanda=id_domanda
        ).one_or_none()

        if not associazione:
            return jsonify({'error': 'Associazione domanda-progetto-questionario non trovata'}), 404

        # Aggiorna il gruppo risposta
        associazione.id_gruppo_risposta = id_gruppo_risposta
        db_session.commit()

        print(f"DEBUG API - aggiornamento avvenuto: id_gruppo_risposta={associazione.id_gruppo_risposta}")

        return jsonify({
            'message': 'Gruppo risposta aggiornato con successo',
            'ID_PROGETTO_QUESTIONARIO': id_pq,
            'ID_DOMANDA': id_domanda,
            'ID_GRUPPO_RISPOSTA': id_gruppo_risposta
        }), 200

    except Exception as e:
        db_session.rollback()
        print(f"ERRORE: associa_gruppo_risposta_domanda -> {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        db_session.close()


@appBT.route('/api/drivers/', methods=['GET'])
@login_required
def get_drivers():
    db_session = SessionLocal()
    try:
        drivers = db_session.query(TDriver).all()
        drivers_list = [{'id': d.id, 'descr': d.descr} for d in drivers]
        return jsonify(drivers_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()


# ============================================
# API: Report Progetti Questionari
# ============================================
@appBT.route('/api/report_pq', methods=['GET'])
@login_required
def get_report_associazioni():
    db_session = SessionLocal()
    
    # Leggi il parametro id_cliente dalla query string
    id_cliente_filter = request.args.get('id_cliente', type=int)
    
    try:
        # Inizializza la query principale
        query = db_session.query(ProgettoQuestionario)
        
        # Carica tutte le relazioni necessarie con joinedload
        query = query.options(
            joinedload(ProgettoQuestionario.progetto).joinedload(TProgetto.cliente), 
            joinedload(ProgettoQuestionario.questionario)
        )
        
        # ✅ GESTIONE FILTRO
        if id_cliente_filter and id_cliente_filter != 0:
            # Se il filtro è attivo, è necessario un JOIN esplicito 
            # per applicare la condizione sulla tabella TProgetto
            query = query.join(ProgettoQuestionario.progetto).filter(TProgetto.id_cliente == id_cliente_filter)

        # Esegui la query
        report_results = query.all()
        
        report_data = []
        for a in report_results:
            progetto = a.progetto
            questionario = a.questionario
            
            # Protezione da dati orfani (caso in cui la relazione è NULL)
            if not progetto or not questionario:
                continue

            # Il cliente è caricato tramite joinedload da TProgetto
            cliente = progetto.cliente
            if not cliente:
                # Caso estremo di TProgetto senza TCliente associato
                cliente_descr = "N/D"
                cliente_id = None
            else:
                cliente_descr = cliente.ragione_sociale
                cliente_id = cliente.id

            report_data.append({
                'ID_Associazione': a.id,
                'ID_Progetto': progetto.id,
                'ID_Cliente': cliente_id,
                'ID_Questionario': questionario.id,
                
                'descr_Progetto': progetto.descr,
                'descr_Cliente': cliente_descr,
                'descr_Questionario': questionario.descr,
            })
            
        return jsonify(report_data), 200
    except Exception as e:
        print(f"ERRORE: get_report_associazioni -> {e}")
        return jsonify({'error': f"Errore nel caricamento del report: {str(e)}"}), 500
    finally:
        db_session.close()

# ============================================
# API: Elenco Clienti (per filtro report)
# ============================================
@appBT.route('/api/report_pq_filtro1', methods=['GET']) 
@login_required
def report_pq_filtro1():
    db_session = SessionLocal()
    try:
        # TCliente è la classe di Domain del cliente
        clienti = db_session.query(TCliente).order_by(TCliente.ragione_sociale).all()
        
        clienti_list = [{
            'id': c.id, 
            'ragione_sociale': c.ragione_sociale
        } for c in clienti]
            
        return jsonify(clienti_list), 200
    except Exception as e:
        print(f"ERRORE: report_pq_filtro1 -> {e}")
        return jsonify({'error': 'Errore nel recupero dell\'elenco clienti per il report.'}), 500
    finally:
        db_session.close()




# ============================================
# API: Dettaglio Report Progetto Questionario (Nuova)
# ============================================
@appBT.route('/api/dettaglio_report/<int:id_progetto_questionario>', methods=['GET'])
@login_required
def get_dettaglio_report(id_progetto_questionario):
    """
    API che recupera i dettagli strutturati (Domande con Risposte Possibili) 
    per un'associazione Progetto-Questionario.
    """
    try:
        # FIX 1: RECUPERA L'UTENTE DALLA SESSIONE
        # Assumendo che 'get_username_from_session' sia disponibile
        nome_utente_autore = get_username_from_session() 
        
        # Chiama il Service, che a sua volta chiama il Repository
        # FIX 2: PASSA IL NOME UTENTE AL SERVICE
        report_data = service_progetto_questionario.get_dettaglio_report(
            id_progetto_questionario=id_progetto_questionario,
            nome_utente_autore=nome_utente_autore # <--- ARGOMENTO AGGIUNTO
        )
        
        if not report_data:
            return jsonify({'message': 'Nessuna domanda/risposta trovata per questa associazione.'}), 200
            
        return jsonify(report_data), 200
        
    except Exception as e:
        # Questo print genera l'output ERRORE che vedi nel log
        print(f"ERRORE: get_dettaglio_report -> {e}") 
        return jsonify({'error': f"Errore nel caricamento del report di dettaglio: {str(e)}"}), 500

# ============================================
# Rotta Pagina: Dettaglio Report Progetto-Questionario (Nuova)
# ============================================
@appBT.route("/report/dettaglio_questionario/<int:id_progetto_questionario>", methods=['GET'])
@login_required
def dettaglio_questionario_page(id_progetto_questionario):
    """
    Renderizza la pagina per visualizzare il report di dettaglio.
    """
    # Logica standard per il menu dinamico e CSRF token
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)

    # from flask_wtf.csrf import generate_csrf
    # csrf_token = generate_csrf()
    
    # Passa l'ID al template affinché il frontend possa chiamare l'API sopra definita
    return render_template(
        "dettaglio_questionario_report.html", # Dovrai creare questo template
        title=f"Dettaglio Report Questionario ID: {id_progetto_questionario}",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
       # csrf_token=csrf_token,
        id_progetto_questionario=id_progetto_questionario
    )

# ============================================
# Rotta Pagina: Dettaglio Report Progetto-Questionario (VERSIONE V2)
# ============================================
@appBT.route("/report/dettaglio_questionario_v2/<int:id_progetto_questionario>", methods=['GET'])
@login_required
def dettaglio_questionario_v2_page(id_progetto_questionario):
    """
    Renderizza la versione V2 (organizzata per categorie) della pagina 
    per visualizzare il report di dettaglio.
    """
    # Logica standard per il menu dinamico e sessione
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)

    # Nota: Assicurati che il file si chiami esattamente dettaglio_questionario_report_v2.html
    return render_template(
        "dettaglio_questionario_report_v2.html", 
        title=f"Questionario Cliente V2 - ID: {id_progetto_questionario}",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        id_progetto_questionario=id_progetto_questionario
    )






@appBT.route("/gestione_risposte")
@login_required
def gestione_risposte():
    """
    Renderizza la pagina di gestione dell'anagrafica Risposta.
    Passa i dati necessari per il menu dinamico e il token CSRF.
    """
    # Replica la logica della rotta '/domanda' per visualizzare il menu
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per gestione_risposte. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf() # Qui generi il token

    return render_template(
        "risposta.html",
        title="Gestione Risposte",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token # E qui lo passi come variabile
    )



@appBT.route("/domanda_gruppo", methods=['GET'])
@login_required
def gestione_domande_gruppo():
    """
    Renderizza la pagina di gestione dell'associazione Domanda-Gruppo di Risposta (gestione_domande_gruppo.html).
    Passa i dati necessari per il menu dinamico e il token CSRF.
    """
    # Recupera i dati di sessione (come nelle altre rotte)
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    # Genera il menu dinamico solo se il ruolo è disponibile
    if current_user_role_id is not None:
        # **NOTA:** Assicurati che 'service_t_funzionalita_utente' sia importato nel tuo server.py
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        print("DEBUG: Ruolo utente non definito in sessione per gestione_domande_gruppo. Menu vuoto.")

    # Genera il token CSRF (come nelle altre rotte)
    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf() 

    return render_template(
        "gestione_domande_gruppo.html",  # Il template che ho creato
        title="Gestione Associazione Domanda-Gruppo Risposta",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token  # Passa il token al template
    )


# Rotta per visualizzare la pagina del report Progetto-Questionario
@appBT.route("/report_progetti_questionari")
@login_required
def report_progetti_questionari_page():
    # ----------------------------------------------------
    # QUESTA È LA PARTE CHE DEVE ESSERE INSERITA (L'INIZIALIZZAZIONE)
    # ----------------------------------------------------
    current_user_role_id = session.get('user_role_id')
    current_user_email = session.get('user_email')
    current_username = session.get('username')
    current_user_role_descr = session.get('user_role_descr')

    dynamic_menu = []
    # Assumo che 'service_t_funzionalita_utente' sia già importato e disponibile
    if current_user_role_id is not None:
        dynamic_menu = service_t_funzionalita_utente.build_menu_structure(role_id=current_user_role_id)
    else:
        # Questo messaggio è utile per il debug
        print("DEBUG: Ruolo utente non definito in sessione per report_progetti_questionari_page. Menu vuoto.")

    from flask_wtf.csrf import generate_csrf
    csrf_token = generate_csrf()
    # ----------------------------------------------------
    
    return render_template(
        "report_progetti_questionari.html", # Nuovo template
        title="Report Progetti/Questionari",
        menu_data=dynamic_menu,
        current_user_email=current_user_email,
        current_username=current_username,
        current_user_role_descr=current_user_role_descr,
        csrf_token=csrf_token # Importante per la sicurezza
    )





def upload_domande():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Nessun file selezionato"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "Nessun file selezionato"}), 400

        print(f"DEBUG: File ricevuto: {file.filename}, Tipo: {file.mimetype}")

        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(file.read()))
        else:
            return jsonify({"error": "Formato file non supportato. Usa .xlsx"}), 400

        df.columns = df.columns.str.strip().str.lower()
        
        print(f"DEBUG: Colonne rilevate nel file dopo la pulizia: {df.columns.tolist()}")

        if 'id_driver' not in df.columns or 'descrizione' not in df.columns:
            return jsonify({"error": "Il file Excel deve contenere le colonne 'id_driver' e 'descrizione'"}), 400

        session_db = SessionLocal()
        
        print(f"DEBUG: Trovate {len(df)} righe valide per l'inserimento.")

        try:
            for index, row in df.iterrows():
                nuova_domanda = TDomanda(
                    id_driver=int(row['id_driver']),  
                    descr=str(row['descrizione']),
                    modificato_da=session.get('username')
                )
                session_db.add(nuova_domanda)
            
            session_db.commit()
            print("DEBUG: Commit del database completato con successo.")

            # Chiamata al servizio di log del caricamento riuscito
            try:
                service_t_dati_caricamento.log_caricamento(
                    descrizione="Caricamento massivo domande",
                    utente=session.get('username'),
                    numero_record=len(df),
                    stato="successo"
                )
                print("DEBUG: Log di caricamento salvato in t_dati_caricamento.")
            except Exception as log_error:
                # Logga l'errore ma non bloccare la risposta HTTP di successo
                print(f"ERRORE DI LOG: Impossibile salvare il log di caricamento: {log_error}")

            return jsonify({"message": f"Caricamento completato. Inseriti {len(df)} record."}), 200

        except Exception as db_error:
            session_db.rollback()
            print(f"ERRORE DB: Errore durante l'inserimento dei dati nel database: {db_error}")
            return jsonify({"error": f"Errore durante l'inserimento dei dati nel database. Dettagli: {str(db_error)}"}), 500
        finally:
            session_db.close()

    except Exception as e:
        print(f"ERRORE GENERICO: Si è verificata un'eccezione non gestita: {e}")
        return jsonify({"error": "Errore di rete o del server. Controlla il terminale per maggiori dettagli."}), 500
    
            
# --- AVVIO DELL'APPLICAZIONE FLASK ---
if __name__ == '__main__':
    app = Flask(__name__, template_folder='template')
    
    app.config['SECRET_KEY'] = 'a_very_secret_and_complex_key_for_your_app_sessions_12345'
    csrf.init_app(app)
    app.register_blueprint(appBT)
    # Import del Controller per Ambito - Assicurati che sia importato dopo l'inizializzazione di app
    from Classi.ClasseAnagrafica.ClasseAmbito.Controller_t_ambito import t_ambito_controller
    print("DEBUG: Registrando t_ambito_controller con prefisso /api/ambito")
    app.register_blueprint(t_ambito_controller, url_prefix='/api/ambito')

    print("DEBUG: Registrando t_categoria_controller con prefisso /api/categoria")
    app.register_blueprint(t_categoria_controller, url_prefix='/api/categoria')

    print("DEBUG: Registrando t_driver_controller con prefisso /api/driver")
    app.register_blueprint(t_driver_controller, url_prefix='/api/driver')

    print("DEBUG: Registrando t_domanda_controller con prefisso /api/domanda")
    app.register_blueprint(t_domanda_controller, url_prefix='/api/domanda')

    # GRUPPO_RISPOSTA
    print("DEBUG: Registrando t_gruppo_risposta_controller con prefisso /api/gruppo_risposta")
    from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Controller_t_gruppo_risposta import t_gruppo_risposta_controller
    app.register_blueprint(t_gruppo_risposta_controller, url_prefix='/api/gruppo-risposta')

    from Classi.ClasseRisposteCliente.Controller_risposta_cliente import risposta_cliente_controller
    from Classi.ClasseRisposteCliente.Controller_risposta_cliente import get_username_from_session

    # Registra il blueprint per la gestione dei progetti
    app.register_blueprint(t_progetto_controller, url_prefix='/api/progetto')

    # Registra il blueprint per la gestione degli stati progetto
    app.register_blueprint(t_stato_progetto_controller, url_prefix='/api/stati_progetto')

    app.register_blueprint(t_questionario_controller, url_prefix='/api/questionario')

    app.register_blueprint(t_risposta_controller, url_prefix='/api/risposta')

    # app.register_blueprint(t_progetto_controller, url_prefix='/api/progetti')

    app.register_blueprint(t_cliente_controller, url_prefix='/api/clienti')

    print("DEBUG: Registrando t_utenti_controller con prefisso /api/utenti")
    app.register_blueprint(t_utenti_controller, url_prefix='/api/utenti')

    print("DEBUG: Registrando risposta_cliente_controller con prefisso /api/risposta_cliente")
    # Il prefisso /api/risposta_cliente è corretto, dato che la rotta nel Controller è /salva_risposte_massive
    app.register_blueprint(risposta_cliente_controller)

    app.register_blueprint(punteggio_controller)

    app.register_blueprint(correttiva_controller)
    
    print("DEBUG: Registrando la rotta di upload 'upload_domande' con prefisso /api/domande/upload")
    app.add_url_rule('/api/domande/upload', 'upload_domande', upload_domande, methods=['POST'])

    try:
        # Crea tutte le tabelle definite nei modelli (incluse Utenti, Ruoli, Funzionalita, etc.)
        # Le tabelle di anagrafica (Ambito, Categoria, etc.) avranno solo lo schema creato qui, 
        # ma l'assenza della logica di popolamento previene l'IntegrityError.
        Base.metadata.create_all(bind=engine)
        print("INFO: Tabelle del database create o già esistenti.")
        
        # AGGIUNTA: Assicurati che TProgetto sia importato e le tabelle create
        # Nonostante Base.metadata.create_all, è spesso lasciato per ridondanza.
        TProgetto.__table__.create(bind=engine, checkfirst=True)
        
        # Assicurati che la tabella 't_dati_caricamento' sia creata
        session_pop_caricamento = SessionLocal()
        try:
            TDatiCaricamento.__table__.create(bind=engine, checkfirst=True)
            print("INFO: Tabella 't_dati_caricamento' creata o già esistente.")
        except Exception as e:
            print(f"ERRORE: Impossibile creare la tabella 't_dati_caricamento': {e}")
        finally:
            session_pop_caricamento.close()
            
        # *** INIZIO SEZIONE POPOLAMENTO DATI RIMOSSA ***
        # L'intera logica di popolamento per Ambito, Categoria, Driver e Domanda è stata rimossa
        # per evitare conflitti con i dati preesistenti e risolvere l'IntegrityError.
        # Anche la chiamata a populate_db() è stata rimossa per risolvere il NameError.
        # *** FINE SEZIONE POPOLAMENTO DATI RIMOSSA ***

    except Exception as e:
        print(f"ERRORE: Errore durante l'avvio dell'applicazione: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)