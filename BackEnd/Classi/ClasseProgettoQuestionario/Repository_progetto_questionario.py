# File: Classi/ClasseProgettoQuestionario/Repository_progetto_questionario.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text 
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario
from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
# Importa RispostaCliente
from Classi.ClasseRisposteCliente.Domain_risposta_cliente import RispostaCliente # ⭐ NUOVO IMPORT
import logging

class RepositoryProgettoQuestionario:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    # --- METODO ESISTENTE (LASCIO SOLO PER RIFERIMENTO SE IL TUO CODICE HA ALTRI METODI) ---
    def associate_questionario(self, id_progetto, id_questionario, domande_gruppo_list):
        """
        Associa un questionario a un progetto e le domande ai gruppi di risposta.
        (Lasciato invariato)
        """
        session = self.Session()
        try:
            # logica per associazione progetto-questionario...
            pq = ProgettoQuestionario(id_progetto=id_progetto, id_questionario=id_questionario)
            session.add(pq)
            session.flush() # Ottiene l'ID di pq prima del commit

            from Classi.ClasseProgettoQuestionarioDomanda.Domain_progetto_questionario_domanda import ProgettoQuestionarioDomanda
            
            for item in domande_gruppo_list:
                pqd = ProgettoQuestionarioDomanda(
                    id_progetto_questionario=pq.id,
                    id_domanda=item['id_domanda'],
                    id_gruppo_risposta=item['id_gruppo_risposta']
                )
                session.add(pqd)
            
            session.commit()
            return pq
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore SQL nell'associazione questionario: {e}")
            raise
        finally:
            session.close()


    # --- METODO AGGIORNATO PER IL DETTAGLIO REPORT CON RISPOSTE SALVATE (FILTRO UTENTE) ---
    # 🟢 MODIFICA 1: Aggiunta di nome_utente_autore alla firma del metodo
    def get_dettaglio_domande_risposte(self, id_progetto_questionario, nome_utente_autore):
        """
        Recupera le domande, le risposte possibili e l'eventuale risposta già salvata
        dall'utente specifico per un dato progetto_questionario.
        Include ora il nome della CATEGORIA per il raggruppamento.
        """
        session = self.Session()
        try:
            # Query SQL Raw per gestire i JOIN complessi e la risposta dell'utente
            query = text("""
                SELECT 
                    pqd.ID AS ID_ASSOCIAZIONE,
                    d.ID AS ID_DOMANDA,
                    d.DESCR AS TESTO_DOMANDA,
                    dr.DESCR AS DRIVER_DESCR,
                    c.DESCR AS CATEGORIA_DESCR,  
                    pqd.ID_GRUPPO_RISPOSTA AS ID_GRUPPO_RISPOSTA,
                    r.ID_RISPOSTA AS ID_RISPOSTA_POSSIBILE,
                    r.DESCR_RISPOSTA AS DESCR_RISPOSTA_POSSIBILE,
                    r.PESO AS PESO_RISPOSTA_POSSIBILE,
                    rc.ID_RISPOSTA AS ID_RISPOSTA_SALVATA
                FROM progetto_questionario_domanda pqd
                JOIN domande d ON pqd.ID_DOMANDA = d.ID
                JOIN driver dr ON d.ID_DRIVER = dr.ID        -- JOIN AL DRIVER
                JOIN categoria c ON dr.ID_CATEGORIA = c.ID   -- JOIN ALLA CATEGORIA
                LEFT JOIN gruppo_risposta_risposta grr ON pqd.ID_GRUPPO_RISPOSTA = grr.ID_GRUPPO_RISPOSTA
                LEFT JOIN risposta r ON grr.ID_RISPOSTA = r.ID_RISPOSTA
                LEFT JOIN risposta_cliente rc ON rc.ID_PROGETTO_QUESTIONARIO_DOMANDA = pqd.ID 
                     AND rc.MODIFICATO_DA = :nome_utente_autore
                WHERE pqd.ID_PROGETTO_QUESTIONARIO = :id_pq
                ORDER BY c.DESCR, pqd.ID, r.ID_RISPOSTA
            """)

            result = session.execute(query, {
                'id_pq': id_progetto_questionario,
                'nome_utente_autore': nome_utente_autore
            })

            dettaglio_domande = {}

            for row in result:
                id_associazione = row.ID_ASSOCIAZIONE
                
                # 1. Se è la prima volta che incontriamo questa domanda, creiamo l'oggetto
                if id_associazione not in dettaglio_domande:
                    dettaglio_domande[id_associazione] = {
                        'id_associazione': id_associazione,
                        'id_domanda': row.ID_DOMANDA,
                        'testo': row.TESTO_DOMANDA,
                        'driver_descr': row.DRIVER_DESCR,
                        'categoria_descr': row.CATEGORIA_DESCR,
                        'gruppo_risposta_id': row.ID_GRUPPO_RISPOSTA,
                        'risposta_salvata_id': row.ID_RISPOSTA_SALVATA, 
                        'risposte_possibili': []
                    }
                
                # 2. Aggiunge le risposte possibili (evitando duplicati)
                if row.ID_RISPOSTA_POSSIBILE is not None:
                    risposta_ids = [r['id'] for r in dettaglio_domande[id_associazione]['risposte_possibili']]
                    if row.ID_RISPOSTA_POSSIBILE not in risposta_ids:
                        dettaglio_domande[id_associazione]['risposte_possibili'].append({
                            'id': row.ID_RISPOSTA_POSSIBILE,
                            'descr': row.DESCR_RISPOSTA_POSSIBILE,
                            'peso': float(row.PESO_RISPOSTA_POSSIBILE) if row.PESO_RISPOSTA_POSSIBILE else None
                        })
            
            return list(dettaglio_domande.values())
            
        except SQLAlchemyError as e:
            logging.error(f"Errore query dettaglio report: {str(e)}")
            session.rollback()
            raise e
        finally:
            session.close()