# File: Classi/ClasseRelazione/Controller_relazione_finale.py
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flask_wtf.csrf import generate_csrf
from Classi.ClasseRelazione.Service_relazione_finale import ServiceRelazioneFinale

relazione_controller = Blueprint('relazione', __name__)
service_relazione = ServiceRelazioneFinale()

@relazione_controller.route("/redazione_relazione/<int:id_pq>")
def redazione_relazione_page(id_pq):
    current_username = session.get('username')
    csrf_token = generate_csrf() 

    # 1. RECUPERA LA RELAZIONE DAL DB
    relazione_salvata = service_relazione.ottieni_relazione(id_pq)

    return render_template(
        "redazione_relazione.html",
        id_pq=id_pq,
        title="Finalizzazione Progetto",
        current_username=current_username,
        csrf_token=csrf_token,
        relazione=relazione_salvata  # 2. PASSA L'OGGETTO AL TEMPLATE
    )

@relazione_controller.route("/salva_relazione_finale/<int:id_pq>", methods=['POST'])
def salva_relazione_finale(id_pq):
    try:
        # Recuperiamo i dati dal form
        # NOTA: Usiamo 'id_pq' come chiave perché il tuo Repository.py alla riga 11 
        # fa: filter_by(id_progetto_questionario=dati['id_pq'])
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