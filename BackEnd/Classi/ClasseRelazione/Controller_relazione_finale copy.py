# File: Classi/ClasseRelazione/Controller_relazione_finale.py
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session, request, flash, redirect, url_for, make_response
from flask_wtf.csrf import generate_csrf
from Classi.ClasseRelazione.Service_relazione_finale import ServiceRelazioneFinale
from Classi.ClassePunteggi.Service_progetto_questionario_punteggio import ServiceProgettoQuestionarioPunteggio

# Import per la logica ORM delle correttive
from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda
from Classi.ClasseCorrettive.Domain_correttiva import Correttiva
from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario

# Import engine e SQL
from Classi.ClasseDB.db_connection import engine
from sqlalchemy import text
from io import BytesIO
from xhtml2pdf import pisa
import logging

relazione_controller = Blueprint('relazione', __name__)
service_relazione = ServiceRelazioneFinale()
service_punteggi = ServiceProgettoQuestionarioPunteggio()

@relazione_controller.route("/redazione_relazione/<int:id_pq>")
def redazione_relazione_page(id_pq):
    current_username = session.get('username')
    csrf_token = generate_csrf() 

    # 1. RECUPERA LA RELAZIONE SALVATA
    relazione_salvata = service_relazione.ottieni_relazione(id_pq)
    
    nome_progetto_reale = "Progetto non trovato"
    risposte_dettaglio = []
    lista_correttive = []
    punteggi_categorie = [] # Nuova lista per il riepilogo aggregato

    # Utilizziamo la sessione ORM per anagrafica e azioni correttive
    session_db = service_relazione.Session()
    try:
        # 2. RECUPERA NOME PROGETTO (via ORM)
        pq_assoc = session_db.query(ProgettoQuestionario).filter_by(id=id_pq).first()
        if pq_assoc and pq_assoc.progetto:
            nome_progetto_reale = pq_assoc.progetto.descr

        # 3. RECUPERA LE AZIONI CORRETTIVE (via ORM)
        lista_correttive = session_db.query(Correttiva).join(
            ProgettoQuestionarioDomanda, 
            Correttiva.id_progetto_questionario_domanda == ProgettoQuestionarioDomanda.id
        ).filter(
            ProgettoQuestionarioDomanda.id_progetto_questionario == id_pq
        ).all()

    except Exception as e:
        logging.error(f"Errore recupero dati ORM: {e}")
    finally:
        session_db.close()

    # 4. QUERY SQL DIRETTA PER LE DOMANDE, RISPOSTE E PUNTEGGI
    try:
        with engine.connect() as conn:
            # Query per il dettaglio (Risposta + Peso)
            query_d = text("""
                SELECT 
                    c.DESCR AS nome_categoria, 
                    dr.DESCR AS nome_driver, 
                    d.DESCR AS testo_domanda,
                    r.DESCR_RISPOSTA AS risposta_testo,
                    r.PESO AS punteggio
                FROM progetto_questionario_domanda pqd
                JOIN domande d ON pqd.ID_DOMANDA = d.ID
                JOIN driver dr ON d.ID_DRIVER = dr.ID
                JOIN categoria c ON dr.ID_CATEGORIA = c.ID
                LEFT JOIN risposta_cliente rc ON pqd.ID = rc.ID_PROGETTO_QUESTIONARIO_DOMANDA
                LEFT JOIN risposta r ON rc.ID_RISPOSTA = r.ID_RISPOSTA
                WHERE pqd.ID_PROGETTO_QUESTIONARIO = :id_pq
                ORDER BY c.ID, dr.ID
            """)
            result_set = conn.execute(query_d, {"id_pq": id_pq})
            risposte_dettaglio = [dict(row._mapping) for row in result_set]
            
            # --- NUOVA QUERY PER RIEPILOGO PUNTEGGI PER CATEGORIA ---
            query_p = text("""
                SELECT 
                    c.DESCR AS nome_categoria,
                    MAX(CASE WHEN pqp.VERSIONE = 'Baseline' THEN pqp.PESO_TOTALE ELSE 0 END) AS peso_baseline,
                    MAX(CASE WHEN pqp.VERSIONE = 'Actual' THEN pqp.PESO_TOTALE ELSE 0 END) AS peso_actual
                FROM categoria c
                JOIN progetto_questionario_punteggio pqp ON c.ID = pqp.ID_CATEGORIA
                WHERE pqp.ID_PROGETTO_QUESTIONARIO = :id_pq
                GROUP BY c.ID, c.DESCR
                ORDER BY c.DESCR
            """)
            res_punteggi = conn.execute(query_p, {"id_pq": id_pq})
            punteggi_categorie = [dict(row._mapping) for row in res_punteggi]

    except Exception as e:
        logging.error(f"Errore Database Query: {e}")

    return render_template(
        "redazione_relazione.html",
        id_pq=id_pq,
        nome_progetto=nome_progetto_reale,
        relazione=relazione_salvata,
        correttive=lista_correttive,
        risposte_dettaglio=risposte_dettaglio,
        punteggi_categorie=punteggi_categorie, # Passaggio dei dati aggregati al template
        csrf_token=csrf_token,
        title="Redazione Relazione",
        current_username=current_username
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
        logging.error(f"ERRORE SALVATAGGIO RELAZIONE: {e}")
        flash(f"Errore tecnico: {str(e)}", "danger")
        return redirect(url_for('relazione.redazione_relazione_page', id_pq=id_pq))

@relazione_controller.route("/download_pdf/<int:id_pq>")
def download_pdf(id_pq):
    """Genera e scarica il PDF della relazione finale."""
    try:
        relazione_salvata = service_relazione.ottieni_relazione(id_pq)
        if not relazione_salvata:
            flash("Salva la relazione prima di scaricare il PDF", "warning")
            return redirect(url_for('relazione.redazione_relazione_page', id_pq=id_pq))
        
        session_db = service_relazione.Session()
        nome_progetto_reale = f"Progetto_{id_pq}"
        lista_correttive = []
        
        try:
            pq_assoc = session_db.query(ProgettoQuestionario).filter_by(id=id_pq).first()
            if pq_assoc and pq_assoc.progetto:
                nome_progetto_reale = pq_assoc.progetto.descr
            
            lista_correttive = session_db.query(Correttiva).join(
                ProgettoQuestionarioDomanda, 
                Correttiva.id_progetto_questionario_domanda == ProgettoQuestionarioDomanda.id
            ).filter(
                ProgettoQuestionarioDomanda.id_progetto_questionario == id_pq
            ).all()
        finally:
            session_db.close()

        html_content = render_template(
            "relazione_pdf.html", 
            relazione=relazione_salvata, 
            correttive=lista_correttive,
            nome_progetto=nome_progetto_reale
        )

        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)

        if pisa_status.err:
            logging.error(f"Errore xhtml2pdf: {pisa_status.err}")
            return "Errore nella generazione del PDF", 500

        pdf_buffer.seek(0)
        nome_file = f"RF_{nome_progetto_reale.replace(' ', '_')}.pdf"
        
        response = make_response(pdf_buffer.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={nome_file}'
        return response

    except Exception as e:
        logging.error(f"ERRORE GENERAZIONE PDF: {e}")
        flash("Si è verificato un errore durante la creazione del PDF.", "danger")
        return redirect(url_for('relazione.redazione_relazione_page', id_pq=id_pq))