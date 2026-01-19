# File: Classi/ClasseRelazione/Controller_relazione_finale.py
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session, request, flash, redirect, url_for, make_response
from flask_wtf.csrf import generate_csrf
from Classi.ClasseRelazione.Service_relazione_finale import ServiceRelazioneFinale
# Importiamo il modello delle domande qui per evitare import circolari nei repository
from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda
from Classi.ClasseCorrettive.Domain_correttiva import Correttiva
from Classi.ClasseCorrettive.Service_correttiva import ServiceCorrettiva
from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario
from Classi.ClasseAnagrafica.ClasseProgetto.Domain_t_progetto import TProgetto
from io import BytesIO
from xhtml2pdf import pisa

relazione_controller = Blueprint('relazione', __name__)
service_relazione = ServiceRelazioneFinale()
service_correttiva = ServiceCorrettiva()

@relazione_controller.route("/redazione_relazione/<int:id_pq>")
def redazione_relazione_page(id_pq):
    current_username = session.get('username')
    csrf_token = generate_csrf() 

    # 1. RECUPERA LA RELAZIONE DAL DB
    relazione_salvata = service_relazione.ottieni_relazione(id_pq)

    # 2. RECUPERA DESCRIZIONE PROGETTO
    session_db = service_relazione.Session()
    descrizione_progetto = "Progetto non trovato"
    
    try:
        # Troviamo l'associazione progetto-questionario e carichiamo il progetto collegato
        pq_assoc = session_db.query(ProgettoQuestionario).filter_by(id=id_pq).first()
        if pq_assoc and pq_assoc.progetto:
            descrizione_progetto = pq_assoc.progetto.descr # 'descr' è il campo in TProgetto
    except Exception as e:
        print(f"Errore recupero descrizione: {e}")
    finally:
        # Chiudi sempre la sessione qui per evitare blocchi
        session_db.close()

    # 3. RECUPERA LE CORRETTIVE (Logica nel Controller per sbloccare VS Code)
    session_db = service_relazione.Session()
    lista_correttive = []
    try:
        lista_correttive = session_db.query(Correttiva).join(
            ProgettoQuestionarioDomanda, 
            Correttiva.id_progetto_questionario_domanda == ProgettoQuestionarioDomanda.id
        ).filter(
            ProgettoQuestionarioDomanda.id_progetto_questionario == id_pq
        ).all()
    except Exception as e:
        print(f"ERRORE RECUPERO CORRETTIVE: {e}")
    finally:
        session_db.close()

    return render_template(
        "redazione_relazione.html",
        id_pq=id_pq,
        nome_progetto=descrizione_progetto, 
        title="Finalizzazione Progetto",
        current_username=current_username,
        csrf_token=csrf_token,
        relazione=relazione_salvata,
        correttive=lista_correttive
    )

@relazione_controller.route("/salva_relazione_finale/<int:id_pq>", methods=['POST'])
def salva_relazione_finale(id_pq):
    try:
        dati_form = {
            'id_pq': id_pq, 
            'sintesi_introduttiva': request.form.get('sintesi_introduttiva'),
            'analisi_criticita': request.form.get('analisi_criticita'),
            'descrizione_interventi': request.form.get('descrizione_interventi'),
            'conclusioni_analista': request.form.get('conclusioni_analista'),
            'firma_analista': request.form.get('firma_analista'),
            'img_radar_baseline': request.form.get('img_radar_baseline'),
            'img_radar_actual': request.form.get('img_radar_actual'),
            'stato': 'COMPLETATA'
        }

        service_relazione.salva_relazione(dati_form)
        flash("Relazione salvata con successo!", "success")
        return redirect(url_for('appBT.associa_questionario_progetto_page'))

    except Exception as e:
        print(f"ERRORE SISTEMA: {e}")
        flash(f"Errore tecnico: {str(e)}", "danger")
        return redirect(url_for('relazione.redazione_relazione_page', id_pq=id_pq))

@relazione_controller.route("/download_pdf/<int:id_pq>")
def download_pdf(id_pq):
    """Genera e scarica il PDF della relazione usando xhtml2pdf."""
    try:
        # 1. Recupera i dati dal database
        relazione_salvata = service_relazione.ottieni_relazione(id_pq)
        
        if not relazione_salvata:
            flash("Salva la relazione prima di scaricare il PDF", "warning")
            return redirect(url_for('relazione.redazione_relazione_page', id_pq=id_pq))
        
        # 2. RECUPERA DESCRIZIONE PROGETTO PER IL PDF
        session_db = service_relazione.Session()
        nome_progetto_reale = f"Progetto ID: {id_pq}"
        try:
            pq_assoc = session_db.query(ProgettoQuestionario).filter(ProgettoQuestionario.id == id_pq).first()
            if pq_assoc and pq_assoc.progetto:
                nome_progetto_reale = pq_assoc.progetto.descr
        finally:
            session_db.close()

        # 3. Recupera le correttive anche per il PDF
        session_db = service_relazione.Session()
        lista_correttive = []
        try:
            lista_correttive = session_db.query(Correttiva).join(
                ProgettoQuestionarioDomanda, 
                Correttiva.id_progetto_questionario_domanda == ProgettoQuestionarioDomanda.id
            ).filter(
                ProgettoQuestionarioDomanda.id_progetto_questionario == id_pq
            ).all()
        finally:
            session_db.close()

        # 3. Renderizza il template HTML dedicato al PDF passando anche le correttive
        html_content = render_template(
            "relazione_pdf.html", 
            relazione=relazione_salvata, 
            correttive=lista_correttive,
            nome_progetto=nome_progetto_reale
        )

        # 4. Crea il PDF in memoria
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)

        if pisa_status.err:
            print(f"Errore xhtml2pdf: {pisa_status.err}")
            return f"Errore nella generazione del PDF", 500

        # 5. Prepara la risposta HTTP
        pdf_buffer.seek(0)
        response = make_response(pdf_buffer.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=Relazione_Finale_{id_pq}.pdf'
        
        return response

    except Exception as e:
        print(f"ERRORE GENERAZIONE PDF: {e}")
        flash("Si è verificato un errore durante la creazione del PDF.", "danger")
        return redirect(url_for('relazione.redazione_relazione_page', id_pq=id_pq))