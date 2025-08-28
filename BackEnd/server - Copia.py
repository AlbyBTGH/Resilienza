# -*- coding: utf-8 -*-
import calendar
import pprint
import logging
import pandas as pd
import io
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

# Importare i modelli (Domain) e i servizi
# Assicurati che questi percorsi siano corretti rispetto alla tua struttura di progetto
from Classi.ClasseDB.db_connection import Base, engine, SessionLocal
from Classi.Classe_menu_principale.Domain_t_menu_principale import TMenuPrincipale
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Domain_t_funzionalitaUtente import TFunzionalitaUtente
from Classi.ClasseUtenti.Classe_t_ruolo.Domain_t_ruolo import TRuolo
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti # Modificato da TUtente a TUtenti

# Import del Domain per Ambito
from Classi.ClasseAnagrafica.ClasseAmbito.Domain_t_ambito import TAmbito

# Import del Domain per Categoria
from Classi.ClasseAnagrafica.ClasseCategoria.Domain_t_categoria import TCategoria

# Import del Domain per Driver
from Classi.ClasseAnagrafica.ClasseDriver.Domain_t_driver import TDriver

# Import del Domain per Domanda
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda

# ### INIZIO AGGIUNTA PER GRUPPO_RISPOSTA ###
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Domain_t_gruppo_risposta import TGruppoRisposta
# ### FINE AGGIUNTA PER GRUPPO_RISPOSTA ###

# Import del Domain per Caricamento Dati # AGGIUNTO
from Classi.Classe_dati_caricamento.Domain_t_dati_caricamento import TDatiCaricamento

# Servizi e Repository
from Classi.Classe_menu_principale.Service_t_menu_principale import Service_t_menu_principale
from Classi.ClasseUtenti.Classe_t_funzionalita.Service_t_funzionalita import Service_t_funzionalita
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import Service_t_FunzionalitaUtente
from Classi.ClasseUtenti.Classe_t_utenti.Repository_t_utenti import Repository_t_utenti
from Classi.ClasseUtenti.Classe_t_ruolo.Repository_t_ruolo import Repository_t_ruolo
# Import del Service e del Controller per Ambito
from Classi.ClasseAnagrafica.ClasseAmbito.Service_t_ambito import Service_t_ambito
from Classi.ClasseAnagrafica.ClasseAmbito.Controller_t_ambito import t_ambito_controller

# Import del Service e del Controller per Categoria
from Classi.ClasseAnagrafica.ClasseCategoria.Service_t_categoria import Service_t_categoria
from Classi.ClasseAnagrafica.ClasseCategoria.Controller_t_categoria import t_categoria_controller

# Import del Service e del Controller per Driver
from Classi.ClasseAnagrafica.ClasseDriver.Service_t_driver import Service_t_driver
from Classi.ClasseAnagrafica.ClasseDriver.Controller_t_driver import t_driver_controller

# Import del Service e del Controller per Domanda
from Classi.ClasseAnagrafica.ClasseDomanda.Service_t_domanda import Service_t_domanda
from Classi.ClasseAnagrafica.ClasseDomanda.Controller_t_domanda import t_domanda_controller

# ### INIZIO AGGIUNTA PER GRUPPO_RISPOSTA ###
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Service_t_gruppo_risposta import Service_t_gruppo_risposta
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Controller_t_gruppo_risposta import t_gruppo_risposta_controller
# ### FINE AGGIUNTA PER GRUPPO_RISPOSTA ###

# Import del Service per Caricamento Dati # AGGIUNTO
from Classi.Classe_dati_caricamento.Service_t_dati_caricamento import ServiceTDatiCaricamento


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
# ### INIZIO AGGIUNTA PER GRUPPO_RISPOSTA ###
service_t_gruppo_risposta = Service_t_gruppo_risposta()
# ### FINE AGGIUNTA PER GRUPPO_RISPOSTA ###

service_t_dati_caricamento = ServiceTDatiCaricamento() # AGGIUNTO


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
""""
# Funzione per il caricamento dei dati
def upload_domande():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Nessun file selezionato"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "Nessun file selezionato"}), 400

        # Debug: Stampa il nome del file e il tipo MIME
        print(f"DEBUG: File ricevuto: {file.filename}, Tipo: {file.mimetype}")

        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(file.read()))
        else:
            return jsonify({"error": "Formato file non supportato. Usa .xlsx"}), 400

        # Rimuovi spazi extra dai nomi delle colonne e convertili in minuscolo
        df.columns = df.columns.str.strip().str.lower()
        
        # Debug: Stampa le colonne lette e i loro tipi di dato
        print(f"DEBUG: Colonne lette dal file: {df.columns.tolist()}")
        print(f"DEBUG: Tipi di dato delle colonne:\n{df.dtypes}")

        if 'id_driver' not in df.columns or 'descrizione' not in df.columns:
            return jsonify({"error": "Il file Excel deve contenere le colonne 'id_driver' e 'descrizione'"}), 400

        session_db = SessionLocal()
        
        # Debug: Stampa il numero di righe da inserire
        print(f"DEBUG: Trovate {len(df)} righe valide per l'inserimento.")

        try:
            for index, row in df.iterrows():
                # Assicurati che il tipo di dato sia corretto
                id_driver = int(row['id_driver'])
                descrizione = str(row['descrizione'])

                nuova_domanda = TDatiCaricamento(
                    ID_DRIVER=id_driver,
                    DESCR=descrizione,
                    MODIFICATO_DA=session.get('username')
                )
                session_db.add(nuova_domanda)
            
            session_db.commit()
            print("DEBUG: Commit del database completato con successo.")

            return jsonify({"message": f"Caricamento completato. Inseriti {len(df)} record."}), 200

        except Exception as db_error:
            session_db.rollback()
            # Debug: Stampa l'errore specifico del database
            print(f"ERRORE DB: Errore durante l'inserimento dei dati nel database: {db_error}")
            return jsonify({"error": f"Errore durante l'inserimento dei dati nel database. Dettagli: {str(db_error)}"}), 500
        finally:
            session_db.close()

    except Exception as e:
        # Debug: Stampa l'errore generico
        print(f"ERRORE GENERICO: Si è verificata un'eccezione non gestita: {e}")
        return jsonify({"error": "Errore di rete o del server. Controlla il terminale per maggiori dettagli."}), 500
"""

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
                # LA CORREZIONE È QUI: Usare i nomi dei parametri in minuscolo
                nuova_domanda = TDomanda(
                    id_driver=int(row['id_driver']),  
                    descr=str(row['descrizione']),
                    modificato_da=session.get('username')
                )
                session_db.add(nuova_domanda)
            
            session_db.commit()
            print("DEBUG: Commit del database completato con successo.")

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

    # ### INIZIO AGGIUNTA PER GRUPPO_RISPOSTA ###
    print("DEBUG: Registrando t_gruppo_risposta_controller con prefisso /api/gruppo_risposta")
    from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Controller_t_gruppo_risposta import t_gruppo_risposta_controller
    app.register_blueprint(t_gruppo_risposta_controller, url_prefix='/api/gruppo_risposta')
    # ### FINE AGGIUNTA PER GRUPPO_RISPOSTA ###

    print("DEBUG: Registrando la rotta di upload 'upload_domande' con prefisso /api/domande/upload")
    app.add_url_rule('/api/domande/upload', 'upload_domande', upload_domande, methods=['POST'])

    try:
        Base.metadata.create_all(bind=engine)
        print("INFO: Tabelle del database create o già esistenti.")
        # Assicurati che la tabella 'ambito' sia creata
        service_t_ambito.create_table_if_not_exists()
        print("INFO: Tabella 'ambito' creata o già esistente.")
        # Assicurati che la tabella 'categoria' sia creata
        service_t_categoria.create_table_if_not_exists()
        print("INFO: Tabella 'categoria' creata o già esistente.")
        # Assicurati che la tabella 'driver' sia creata
        service_t_driver.create_table_if_not_exists()
        print("INFO: Tabella 'driver' creata o già esistente.")
        # Assicurati che la tabella 'domande' sia creata
        service_t_domanda.create_table_if_not_exists()
        print("INFO: Tabella 'domande' creata o già esistente.")
        # ### INIZIO AGGIUNTA PER GRUPPO_RISPOSTA ###
        service_t_gruppo_risposta.create_table_if_not_exists()
        print("INFO: Tabella 'gruppo_risposta' creata o già esistente.")
        # ### FINE AGGIUNTA PER GRUPPO_RISPOSTA ###
        # Assicurati che la tabella 't_dati_caricamento' sia creata
        # AGGIUNTO
        session_pop_caricamento = SessionLocal()
        try:
            TDatiCaricamento.__table__.create(bind=engine, checkfirst=True)
            print("INFO: Tabella 't_dati_caricamento' creata o già esistente.")
        except Exception as e:
            print(f"ERRORE: Impossibile creare la tabella 't_dati_caricamento': {e}")
        finally:
            session_pop_caricamento.close()
        # Popolamento dati di test per t_ambito
        session_pop_ambito = SessionLocal()
        try:
            if not session_pop_ambito.query(TAmbito).first():
                print("INFO: Popolamento dati di test per ambito...")
                default_ambiti = [
                    TAmbito(codice="AMB001", descrizione="Ambito di Test 1", note="Nota per AMB001"),
                    TAmbito(codice="AMB002", descrizione="Ambito di Test 2", note="Nota per AMB002"),
                    TAmbito(codice="AMB003", descrizione="Ambito di Test 3", note="Nota per AMB003")
                ]
                session_pop_ambito.add_all(default_ambiti)
                session_pop_ambito.commit()
                print("INFO: Dati di test per ambito popolati con successo.")
            else:
                print("INFO: Tabella 'ambito' già popolata, salto il popolamento dei dati di test.")
        except Exception as e:
            session_pop_ambito.rollback()
            print(f"ERRORE: Errore durante il popolamento di ambito: {e}")
        finally:
            session_pop_ambito.close()
        # Popolamento dati di test per t_categoria
        session_pop_categoria = SessionLocal()
        try:
            existing_ambito_for_cat = session_pop_categoria.query(TAmbito).filter_by(codice="AMB001").first()
            if not existing_ambito_for_cat:
                # Se "Categoria di Test 1" non esiste, prova a recuperare o creare una "Categoria Default per Driver"
                existing_ambito_for_cat = TAmbito(codice="DEFAULT_AMB", descrizione="Ambito Default per Categorie", note="Creato per test")
                session_pop_categoria.add(existing_ambito_for_cat)
                session_pop_categoria.commit()
                session_pop_categoria.refresh(existing_ambito_for_cat)
            if not session_pop_categoria.query(TCategoria).filter(TCategoria.descr.like("Categoria di Test %")).first(): # Modificato per evitare duplicati se ci sono altre categorie
                print("INFO: Popolamento dati di test per categoria...")
                default_categorie = [
                    TCategoria(descr="Categoria di Test 1", tipo_categoria="Tipo A", id_ambito=existing_ambito_for_cat.id),
                    TCategoria(descr="Categoria di Test 2", tipo_categoria="Tipo B", id_ambito=existing_ambito_for_cat.id),
                    TCategoria(descr="Categoria di Test 3", tipo_categoria="Tipo A", id_ambito=existing_ambito_for_cat.id) # CORREZIONE QUI
                ]
                session_pop_categoria.add_all(default_categorie)
                session_pop_categoria.commit()
                print("INFO: Dati di test per categoria popolati con successo.")
            else:
                print("INFO: Tabella 'categoria' già popolata con categorie di test, salto il popolamento.")
        except Exception as e:
            session_pop_categoria.rollback()
            print(f"ERRORE: Errore durante il popolamento di categoria: {e}")
        finally:
            session_pop_categoria.close()
        # Popolamento dati di test per t_driver
        session_pop_driver = SessionLocal()
        try:
            existing_categoria_for_driver = session_pop_driver.query(TCategoria).filter_by(descr="Categoria di Test 1").first()
            if not existing_categoria_for_driver:
                # Se "Categoria di Test 1" non esiste, prova a recuperare o creare una "Categoria Default per Driver"
                existing_categoria_for_driver = session_pop_driver.query(TCategoria).filter_by(descr="Categoria Default per Driver").first()
                if not existing_categoria_for_driver:
                    # Assicurati che esista un ambito per questa categoria di default
                    existing_ambito_for_cat_driver = session_pop_driver.query(TAmbito).filter_by(codice="DEFAULT_AMB").first()
                    if not existing_ambito_for_cat_driver:
                        existing_ambito_for_cat_driver = TAmbito(codice="DEFAULT_AMB", descrizione="Ambito Default per Categorie", note="Creato per test")
                        session_pop_driver.add(existing_ambito_for_cat_driver)
                        session_pop_driver.commit()
                        session_pop_driver.refresh(existing_ambito_for_cat_driver)
                    existing_categoria_for_driver = TCategoria(descr="Categoria Default per Driver", tipo_categoria="Default", id_ambito=existing_ambito_for_cat_driver.id)
                    session_pop_driver.add(existing_categoria_for_driver)
                    session_pop_driver.commit()
                    session_pop_driver.refresh(existing_categoria_for_driver)
            if not session_pop_driver.query(TDriver).filter(TDriver.descrizione.like("Driver di Test %")).first(): # Modificato per evitare duplicati
                print("INFO: Popolamento dati di test per driver...")
                default_drivers = [
                    TDriver(ID_CATEGORIA=existing_categoria_for_driver.ID if existing_categoria_for_driver else 1, descrizione="Driver di Test 1", note="Note Driver 1"),
                    TDriver(ID_CATEGORIA=existing_categoria_for_driver.ID if existing_categoria_for_driver else 1, descrizione="Driver di Test 2", note="Note Driver 2"),
                    TDriver(ID_CATEGORIA=existing_categoria_for_driver.ID if existing_categoria_for_driver else 1, descrizione="Driver di Test 3", note="Note Driver 3")
                ]
                session_pop_driver.add_all(default_drivers)
                session_pop_driver.commit()
                print("INFO: Dati di test per driver popolati con successo.")
            else:
                print("INFO: Tabella 'driver' già popolata con driver di test, salto il popolamento.")
        except Exception as e:
            session_pop_driver.rollback()
            print(f"ERRORE: Errore durante il popolamento di driver: {e}")
        finally:
            session_pop_driver.close()

        # Popolamento dati di test per t_domanda
        session_pop_domanda = SessionLocal()
        try:
            if not session_pop_domanda.query(TDomanda).first():
                print("INFO: Popolamento dati di test per domanda...")
                # Recupero di un driver esistente
                existing_driver = session_pop_domanda.query(TDriver).first()
                if not existing_driver:
                    # Se non ci sono driver, ne crea uno di default per evitare errori
                    print("ATTENZIONE: Nessun driver trovato. Creazione di un driver di default per le domande.")
                    default_cat = session_pop_domanda.query(TCategoria).first()
                    if not default_cat:
                        default_cat = TCategoria(descr="Categoria Default", tipo_categoria="Default", id_ambito=session_pop_domanda.query(TAmbito).first().id)
                        session_pop_domanda.add(default_cat)
                        session_pop_domanda.commit()
                        session_pop_domanda.refresh(default_cat)
                    existing_driver = TDriver(ID_CATEGORIA=default_cat.ID, descrizione="Driver Default per Domande", note="Creato per test")
                    session_pop_domanda.add(existing_driver)
                    session_pop_domanda.commit()
                    session_pop_domanda.refresh(existing_driver)

                # Dati di test per le domande
                default_domande = [
                    TDomanda(descr="Domanda di test 1?", id_driver=existing_driver.ID, abilitato=True),
                    TDomanda(descr="Domanda di test 2?", id_driver=existing_driver.ID, abilitato=True),
                    TDomanda(descr="Domanda di test 3?", id_driver=existing_driver.ID, abilitato=False)
                ]
                session_pop_domanda.add_all(default_domande)
                session_pop_domanda.commit()
                print("INFO: Dati di test per domanda popolati con successo.")
            else:
                print("INFO: Tabella 'domanda' già popolata, salto il popolamento dei dati di test.")
        except Exception as e:
            session_pop_domanda.rollback()
            print(f"ERRORE: Errore durante il popolamento di domanda: {e}")
        finally:
            session_pop_domanda.close()
            
        # Popolamento di ruoli e funzionalità
        populate_db()

    except Exception as e:
        print(f"ERRORE: Errore durante l'avvio dell'applicazione: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)