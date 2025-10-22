# Classi\ClasseProgettoQuestionarioDomanda\Controller_progetto_questionario_domanda.py
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from sqlalchemy.orm import sessionmaker
import logging

from Classi.ClasseDB.db_connection import engine

progetto_questionario_domanda_controller = Blueprint('progetto_questionario_domanda', __name__)

@progetto_questionario_domanda_controller.route(
    "/api/progetto_questionario_domande/<int:id_progetto>/<int:id_questionario>", methods=['GET']
)
def get_domande_associazione(id_progetto, id_questionario):
    """
    Restituisce tutte le domande associate a una specifica coppia (progetto + questionario).
    Import effettuati dentro la funzione per evitare problemi di import circolare.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Import locali — se falliscono verrà loggato chiaramente
        try:
            from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario
            from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda
            from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
            # GruppoRisposta è opzionale — commenta se non esiste
            try:
                from Classi.ClasseQuestionario.Domain_gruppo_risposta import GruppoRisposta
                has_gruppo = True
            except Exception:
                has_gruppo = False
        except Exception as imp_err:
            logging.exception("Import error in Controller_progetto_questionario_domanda")
            return jsonify({"error": "Import error: " + str(imp_err)}), 500

        # 1️⃣ Trova l'associazione nella tabella progetto_questionario
        pq = (
            session.query(ProgettoQuestionario)
            .filter_by(id_progetto=id_progetto, id_questionario=id_questionario)
            .first()
        )

        if not pq:
            return jsonify({"error": "Associazione progetto-questionario non trovata"}), 404

        # 2️⃣ Recupera tutte le domande associate
        if has_gruppo:
            query = (
                session.query(
                    ProgettoQuestionarioDomanda.id.label("id_associazione"),
                    TDomanda.ID.label("id_domanda"),
                    TDomanda.DESCR.label("descr_domanda"),
                    GruppoRisposta.DESCR.label("descr_gruppo_risposta")
                )
                .join(TDomanda, ProgettoQuestionarioDomanda.id_domanda == TDomanda.ID)
                .outerjoin(GruppoRisposta, ProgettoQuestionarioDomanda.id_gruppo_risposta == GruppoRisposta.ID_GRUPPO_RISPOSTA)
                .filter(ProgettoQuestionarioDomanda.id_progetto_questionario == pq.id)
            )
            domande = [
                {
                    "id_associazione": r.id_associazione,
                    "id_domanda": r.id_domanda,
                    "descr_domanda": r.descr_domanda,
                    "descr_gruppo_risposta": r.descr_gruppo_risposta
                }
                for r in query.all()
            ]
        else:
            # Se non hai GruppoRisposta, esegui query più semplice
            query = (
                session.query(
                    ProgettoQuestionarioDomanda.id.label("id_associazione"),
                    TDomanda.ID.label("id_domanda"),
                    TDomanda.DESCR.label("descr_domanda"),
                    ProgettoQuestionarioDomanda.id_gruppo_risposta.label("id_gruppo_risposta")
                )
                .join(TDomanda, ProgettoQuestionarioDomanda.id_domanda == TDomanda.ID)
                .filter(ProgettoQuestionarioDomanda.id_progetto_questionario == pq.id)
            )
            domande = [
                {
                    "id_associazione": r.id_associazione,
                    "id_domanda": r.id_domanda,
                    "descr_domanda": r.descr_domanda,
                    "id_gruppo_risposta": r.id_gruppo_risposta
                }
                for r in query.all()
            ]

        return jsonify(domande), 200

    except Exception as e:
        logging.exception("Errore in get_domande_associazione")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()