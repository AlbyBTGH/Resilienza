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
    def get_dettaglio_domande_risposte(self, id_progetto_questionario: int, nome_utente_autore: str):
        """
        Recupera le domande, le risposte possibili e la risposta salvata
        dall'utente loggato (nome_utente_autore) per un ProgettoQuestionario.
        """
        session = self.Session()
        try:
            # Query che recupera: Associazione Domanda, Domanda, Risposte Possibili e Risposta Salvata (RC FILTRATA)
            sql_query = text("""
                SELECT
                    PQD.ID AS ID_ASSOCIAZIONE,
                    D.ID AS ID_DOMANDA,
                    D.DESCR AS TESTO_DOMANDA,
                    -- Utilizza l'ID GRUPPO RISPOSTA dalla tabella di associazione
                    PQD.ID_GRUPPO_RISPOSTA AS ID_GRUPPO_RISPOSTA,
                    R.ID_RISPOSTA AS ID_RISPOSTA_POSSIBILE,
                    R.DESCR_RISPOSTA AS DESCR_RISPOSTA_POSSIBILE,
                    R.PESO AS PESO_RISPOSTA_POSSIBILE,
                    -- Campo chiave per la pre-selezione. È NULL se non c'è risposta salvata da QUESTO utente.
                    RC.ID_RISPOSTA AS ID_RISPOSTA_SALVATA
                FROM
                    progetto_questionario_domanda PQD
                JOIN
                    domande D ON PQD.ID_DOMANDA = D.ID
                -- JOIN per collegare le risposte possibili
                LEFT JOIN
                    gruppo_risposta_risposta GRR ON PQD.ID_GRUPPO_RISPOSTA = GRR.ID_GRUPPO_RISPOSTA
                LEFT JOIN
                    risposta R ON GRR.ID_RISPOSTA = R.ID_RISPOSTA
                LEFT JOIN
                    risposta_cliente RC 
                    ON RC.ID_PROGETTO_QUESTIONARIO_DOMANDA = PQD.ID
                    -- 🟢 MODIFICA 2: Filtra la risposta cliente SOLO per l'utente loggato
                    AND RC.MODIFICATO_DA = :nome_utente_autore
                    
                WHERE
                    PQD.ID_PROGETTO_QUESTIONARIO = :id_pq
                ORDER BY
                    PQD.ID, R.ID_RISPOSTA
            """)
            
            # 🟢 MODIFICA 3: Passa entrambi i parametri all'esecuzione della query
            result = session.execute(sql_query, {
                "id_pq": id_progetto_questionario,
                "nome_utente_autore": nome_utente_autore 
            })
            
            dettaglio_domande = {}

            for row in result:
                id_associazione = row.ID_ASSOCIAZIONE
                
                # 1. Inizializza la struttura della domanda/associazione
                if id_associazione not in dettaglio_domande:
                    dettaglio_domande[id_associazione] = {
                        'id_associazione': id_associazione,
                        'id_domanda': row.ID_DOMANDA,
                        'testo': row.TESTO_DOMANDA,
                        'gruppo_risposta_id': row.ID_GRUPPO_RISPOSTA,
                        # ID della risposta salvata da QUESTO utente (sarà NULL se non ha risposto)
                        'risposta_salvata_id': row.ID_RISPOSTA_SALVATA, 
                        'risposte_possibili': []
                    }
                
                # 2. Aggiunge le risposte possibili
                if row.ID_RISPOSTA_POSSIBILE is not None:
                    # Evita duplicati nella lista risposte_possibili (causati dal join con RC)
                    risposta_ids = [r['id'] for r in dettaglio_domande[id_associazione]['risposte_possibili']]
                    if row.ID_RISPOSTA_POSSIBILE not in risposta_ids:
                        dettaglio_domande[id_associazione]['risposte_possibili'].append({
                            'id': row.ID_RISPOSTA_POSSIBILE,
                            'descr': row.DESCR_RISPOSTA_POSSIBILE,
                            'peso': float(row.PESO_RISPOSTA_POSSIBILE) if row.PESO_RISPOSTA_POSSIBILE else None
                        })
            
            # Ritorna la lista strutturata
            return list(dettaglio_domande.values())
            
        except SQLAlchemyError as e:
            logging.error(f"Errore SQL nel recupero dettaglio questionario: {e}")
            raise
        finally:
            session.close()