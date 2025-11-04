# File: Classi/ClasseProgettoQuestionarioDomanda/Controller_progetto_questionario_domanda.py
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from sqlalchemy.orm import sessionmaker
import logging

from Classi.ClasseDB.db_connection import engine

progetto_questionario_domanda_controller = Blueprint('progetto_questionario_domanda', __name__)

# ======================================================================
# 1. ROTTA ORIGINALE: Ricerca per Progetto ID + Questionario ID
#    (CORRETTA: Usa TDomanda.id e TDomanda.descr)
# ======================================================================

@progetto_questionario_domanda_controller.route(
    "/api/progetto_questionario_domande/<int:id_progetto>/<int:id_questionario>", methods=['GET']
)
def get_domande_associazione(id_progetto, id_questionario):
    """
    Restituisce tutte le domande associate a una specifica coppia (progetto + questionario).
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Import locali
        try:
            from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario
            from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda
            from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
            # GruppoRisposta è opzionale
            try:
                from Classi.ClasseQuestionario.Domain_gruppo_risposta import GruppoRisposta
                has_gruppo = True
            except Exception:
                has_gruppo = False
        except Exception as imp_err:
            logging.exception("Import error in get_domande_associazione")
            return jsonify({"error": "Import error: " + str(imp_err)}), 500

        # 1️⃣ Trova l'associazione nella tabella progetto_questionario
        pq = (
            session.query(ProgettoQuestionario)
            .filter_by(id_progetto=id_progetto, id_questionario=id_questionario)
            .first()
        )

        if not pq:
            return jsonify({"error": "Associazione progetto-questionario non trovata"}), 404

        pq_id_to_use = pq.id
        
        # 2️⃣ Recupera tutte le domande associate
        if has_gruppo:
            query = (
                session.query(
                    ProgettoQuestionarioDomanda.id.label("id_associazione"),
                    TDomanda.id.label("id_domanda"),          # CORRETTO: .id
                    TDomanda.descr.label("descr_domanda"),    # CORRETTO: .descr
                    GruppoRisposta.DESCR.label("descr_gruppo_risposta")
                )
                .join(TDomanda, ProgettoQuestionarioDomanda.id_domanda == TDomanda.id) # CORRETTO: TDomanda.id
                .outerjoin(GruppoRisposta, ProgettoQuestionarioDomanda.id_gruppo_risposta == GruppoRisposta.ID_GRUPPO_RISPOSTA)
                .filter(ProgettoQuestionarioDomanda.id_progetto_questionario == pq_id_to_use)
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
                    TDomanda.id.label("id_domanda"),          # CORRETTO: .id
                    TDomanda.descr.label("descr_domanda"),    # CORRETTO: .descr
                    ProgettoQuestionarioDomanda.id_gruppo_risposta.label("id_gruppo_risposta")
                )
                .join(TDomanda, ProgettoQuestionarioDomanda.id_domanda == TDomanda.id) # CORRETTO: TDomanda.id
                .filter(ProgettoQuestionarioDomanda.id_progetto_questionario == pq_id_to_use)
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

# ======================================================================
# 2. NUOVA ROTTA: Ricerca per ID Associazione Progetto-Questionario
#    (CORRETTA: Usa TDomanda.id e TDomanda.descr)
# ======================================================================

@progetto_questionario_domanda_controller.route(
    "/api/progetto_questionario_domande_dettaglio/<int:id_progetto_questionario>", 
    methods=['GET']
)
def get_domande_dettaglio_by_id_pq(id_progetto_questionario):
    """
    Restituisce tutte le domande associate ad uno specifico ID di associazione
    Progetto+Questionario. Corrisponde alla chiamata API del report dettaglio.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Import locali
        try:
            from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda
            from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
            # GruppoRisposta è opzionale
            try:
                from Classi.ClasseQuestionario.Domain_gruppo_risposta import GruppoRisposta
                has_gruppo = True
            except Exception:
                has_gruppo = False
        except Exception as imp_err:
            logging.exception("Import error in get_domande_dettaglio_by_id_pq")
            return jsonify({"error": "Import error: " + str(imp_err)}), 500
        
        pq_id_to_use = id_progetto_questionario

        # 2️⃣ Recupera tutte le domande associate filtrando per id_progetto_questionario
        if has_gruppo:
            query = (
                session.query(
                    ProgettoQuestionarioDomanda.id.label("id_associazione"),
                    TDomanda.id.label("id_domanda"),          # CORRETTO: .id
                    TDomanda.descr.label("descr_domanda"),    # CORRETTO: .descr
                    GruppoRisposta.DESCR.label("descr_gruppo_risposta"),
                    ProgettoQuestionarioDomanda.id_gruppo_risposta.label("gruppo_risposta_id")
                )
                .join(TDomanda, ProgettoQuestionarioDomanda.id_domanda == TDomanda.id) # CORRETTO: TDomanda.id
                .outerjoin(GruppoRisposta, ProgettoQuestionarioDomanda.id_gruppo_risposta == GruppoRisposta.ID_GRUPPO_RISPOSTA)
                .filter(ProgettoQuestionarioDomanda.id_progetto_questionario == pq_id_to_use)
            )
            domande = [
                {
                    "id_associazione": r.id_associazione,
                    "id_domanda": r.id_domanda,
                    "descr_domanda": r.descr_domanda,
                    "descr_gruppo_risposta": r.descr_gruppo_risposta,
                    "gruppo_risposta_id": r.gruppo_risposta_id
                }
                for r in query.all()
            ]
        else:
            # Se non hai GruppoRisposta, esegui query più semplice
            query = (
                session.query(
                    ProgettoQuestionarioDomanda.id.label("id_associazione"),
                    TDomanda.id.label("id_domanda"),          # CORRETTO: .id
                    TDomanda.descr.label("descr_domanda"),    # CORRETTO: .descr
                    ProgettoQuestionarioDomanda.id_gruppo_risposta.label("gruppo_risposta_id")
                )
                .join(TDomanda, ProgettoQuestionarioDomanda.id_domanda == TDomanda.id) # CORRETTO: TDomanda.id
                .filter(ProgettoQuestionarioDomanda.id_progetto_questionario == pq_id_to_use)
            )
            domande = [
                {
                    "id_associazione": r.id_associazione,
                    "id_domanda": r.id_domanda,
                    "descr_domanda": r.descr_domanda,
                    "gruppo_risposta_id": r.gruppo_risposta_id
                }
                for r in query.all()
            ]

        return jsonify(domande), 200

    except Exception as e:
        logging.exception("Errore in get_domande_dettaglio_by_id_pq")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()