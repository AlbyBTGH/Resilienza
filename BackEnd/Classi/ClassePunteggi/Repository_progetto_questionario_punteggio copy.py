# File: Classi/ClassePunteggi/Repository_progetto_questionario_punteggio.py
# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text 
# Assumendo l'importazione del tuo engine di connessione
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePunteggi.Domain_progetto_questionario_punteggio import ProgettoQuestionarioPunteggio 
# Importazione essenziale per la JOIN ORM (se usi l'ORM per la lettura)
from Classi.ClasseAnagrafica.ClasseCategoria.Domain_t_categoria import TCategoria 

class RepositoryProgettoQuestionarioPunteggio:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session


    def calcola_e_salva_punteggio_per_categoria(self, session, id_progetto_questionario, version):
            """
            Esegue il calcolo aggregato, elimina i dati precedenti per la stessa versione e salva i risultati.
            (Versione con logging di debug esteso)
            """
            
            try:
                # 1. DELETE: Eliminazione mirata solo per la VERSIONE che si sta salvando.
                logging.info(f"Repository: Esecuzione DELETE per PQ {id_progetto_questionario}, Versione {version}")
                session.execute(
                    text("""
                        DELETE FROM progetto_questionario_punteggio 
                        WHERE ID_PROGETTO_QUESTIONARIO = :id_pq AND VERSIONE = :version
                    """),
                    {"id_pq": id_progetto_questionario, "version": version} 
                )
                
                # 2. Query di Calcolo (SELECT) per recuperare i dati (Assunta invariata)
                calcolo_query = f"""
                    SELECT
                        p.ID AS id_progetto,
                        pq.ID_QUESTIONARIO AS id_questionario,
                        p.ID_CLIENTE AS id_cliente,
                        pq.ID AS id_progetto_questionario,
                        cat.ID AS id_categoria,
                        SUM(r.PESO) AS peso_totale
                    FROM
                        risposta_cliente rc
                    JOIN
                        progetto_questionario_domanda pqd ON rc.ID_PROGETTO_QUESTIONARIO_DOMANDA = pqd.ID
                    JOIN
                        progetto_questionario pq ON pqd.ID_PROGETTO_QUESTIONARIO = pq.ID
                    JOIN
                        progetto p ON pq.ID_PROGETTO = p.ID
                    JOIN
                        cliente c ON p.ID_CLIENTE = c.ID
                    JOIN
                        risposta r ON rc.ID_RISPOSTA = r.ID_RISPOSTA
                    JOIN
                        domande d ON pqd.ID_DOMANDA = d.ID
                    JOIN
                        driver dr ON d.ID_DRIVER = dr.ID
                    JOIN
                        categoria cat ON dr.ID_CATEGORIA = cat.ID
                    WHERE
                        pq.ID = :id_pq
                    GROUP BY
                        p.ID, pq.ID_QUESTIONARIO, p.ID_CLIENTE, pq.ID, cat.ID
                """
                
                # 3. Logica di inserimento (INSERT INTO... SELECT)
                insert_query = f"""
                    INSERT INTO progetto_questionario_punteggio (
                        ID_PROGETTO, 
                        ID_QUESTIONARIO, 
                        ID_CLIENTE,
                        ID_PROGETTO_QUESTIONARIO, 
                        ID_CATEGORIA, 
                        PESO_TOTALE,
                        VERSIONE,              
                        DATA_CHIUSURA
                    )
                    SELECT
                        t.id_progetto,
                        t.id_questionario,
                        t.id_cliente,
                        t.id_progetto_questionario,
                        t.id_categoria,
                        t.peso_totale,
                        :version,            
                        CURRENT_TIMESTAMP() 
                    FROM
                        ({calcolo_query}) t
                """
                
                # Esecuzione della query di inserimento
                logging.info(f"Repository: Esecuzione INSERT per PQ {id_progetto_questionario}, Versione {version}")
                result = session.execute(
                    text(insert_query), 
                    {
                        "id_pq": id_progetto_questionario,
                        "version": version     
                    }
                )
                
                total_rows = result.rowcount
                logging.info(f"Repository: Inserite/Aggiornate {total_rows} righe per la Versione {version}.")
                
                return {"rows_affected": total_rows}
                
            except SQLAlchemyError as e:
                # ⭐ CERCA QUESTO ERRORE NEL TUO LOG
                logging.error(f"ERRORE SQL nel salvataggio punteggio ({version}) per PQ {id_progetto_questionario}: {e}")
                raise 
            except Exception as e:
                # ⭐ CERCA ANCHE QUESTO ERRORE
                logging.error(f"ERRORE GENERICO nel salvataggio punteggio ({version}) per PQ {id_progetto_questionario}: {e}")
                raise
        
    # ======================================================================
    # MODIFICATO:get_punteggio_per_categorie per supportare il filtro versione
    # ======================================================================
    def get_punteggio_per_categorie(self, session, id_progetto_questionario, version=None):
        """
        Recupera il peso_totale e la descrizione della categoria, filtrando opzionalmente per VERSIONE.
        """
        sql_query = """
            SELECT
                t2.DESCR AS nome_categoria,
                t1.PESO_TOTALE AS peso_totale,
                t1.VERSIONE AS versione
            FROM
                progetto_questionario_punteggio t1
            JOIN
                categoria t2 ON t1.ID_CATEGORIA = t2.ID
            WHERE
                t1.ID_PROGETTO_QUESTIONARIO = :id_pq
                
            -- Placeholder per il filtro VERSIONE, riempito dinamicamente
            {version_filter} 
                
            ORDER BY
                t2.DESCR;
        """
        
        # Logica di costruzione del filtro dinamico
        version_filter = ""
        params = {"id_pq": id_progetto_questionario}
        
        if version and version in ['Baseline', 'Actual']:
            version_filter = "AND t1.VERSIONE = :version"
            params["version"] = version

        # Formatta la query SQL con il filtro (vuoto o attivo)
        sql_query = sql_query.format(version_filter=version_filter)
        
        try:
            result = session.execute(
                text(sql_query), 
                params # Utilizza il dizionario dei parametri aggiornato
            )
            
            # Mappa le righe in una lista di dizionari, convertendo il PESO_TOTALE in float
            dati_grafico = [
                {'nome_categoria': row.nome_categoria, 
                 'peso_totale': float(row.peso_totale),
                 'versione': row.versione
                }
                for row in result.all()
            ]
            
            return dati_grafico
            
        except Exception as e:
            logging.error(f"Errore DB in get_punteggio_per_categorie (SQL): {e}")
            raise # Rilancia l'errore per la gestione nel Service