# File: Classi/ClassePunteggi/Repository_progetto_questionario_punteggio.py
# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text 
# Assumendo l'importazione del tuo engine di connessione
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePunteggi.Domain_progetto_questionario_punteggio import ProgettoQuestionarioPunteggio 
# ⭐ Importazione essenziale per la JOIN ORM (se usi l'ORM per la lettura)
from Classi.ClasseAnagrafica.ClasseCategoria.Domain_t_categoria import TCategoria 
# Alternativa: se usi la query SQL esplicita, potresti non aver bisogno di TCategoria qui.

class RepositoryProgettoQuestionarioPunteggio:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def calcola_e_salva_punteggio_per_categoria(self, session, id_progetto_questionario):
        """
        Esegue la query SQL fornita dall'utente per calcolare il punteggio aggregato
        e inserisce/aggiorna i risultati nella tabella progetto_questionario_punteggio.
        """
        
        # 1. Query di Calcolo (SELECT) per recuperare i dati da inserire
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
        
        # 2. Eliminazione dei risultati precedenti per garantire l'UPSERT (MySQL DELETE)
        session.execute(
            text("DELETE FROM progetto_questionario_punteggio WHERE ID_PROGETTO_QUESTIONARIO = :id_pq"),
            {"id_pq": id_progetto_questionario}
        )
        
        # 3. Logica di inserimento (INSERT INTO... SELECT)
        insert_query = f"""
            INSERT INTO progetto_questionario_punteggio (
                ID_PROGETTO, 
                ID_QUESTIONARIO, 
                ID_CLIENTE,
                ID_PROGETTO_QUESTIONARIO, 
                ID_CATEGORIA, 
                PESO_TOTALE,
                DATA_CHIUSURA
            )
            SELECT
                t.id_progetto,
                t.id_questionario,
                t.id_cliente,
                t.id_progetto_questionario,
                t.id_categoria,
                t.peso_totale,
                CURRENT_TIMESTAMP() 
            FROM
                ({calcolo_query}) t
        """
        
        # Esecuzione della query di inserimento
        result = session.execute(
            text(insert_query), 
            {
                "id_pq": id_progetto_questionario 
            }
        )
        
        # Restituisce il conteggio delle righe interessate
        return {"rows_affected": result.rowcount}
        
    # ======================================================================
    # ⭐ METODO AGGIUNTO/CORRETTO: get_punteggio_per_categorie
    # Questo metodo risolve l'errore 'object has no attribute'
    # ======================================================================
    def get_punteggio_per_categorie(self, session, id_progetto_questionario):
        """
        Recupera il peso_totale e la descrizione della categoria dal punteggio salvato.
        Utilizza l'ORM per unire Punteggio e TCategoria.
        """
        sql_query = """
            SELECT
                t2.DESCR AS nome_categoria,
                t1.PESO_TOTALE AS peso_totale
            FROM
                progetto_questionario_punteggio t1
            JOIN
                categoria t2 ON t1.ID_CATEGORIA = t2.ID
            WHERE
                t1.ID_PROGETTO_QUESTIONARIO = :id_pq
            ORDER BY
                t2.DESCR;
        """
        
        try:
            # Esegue la query SQL
            result = session.execute(
                text(sql_query), 
                {"id_pq": id_progetto_questionario}
            )
            
            # Mappa le righe in una lista di dizionari, convertendo il PESO_TOTALE in float
            dati_grafico = [
                {'nome_categoria': row.nome_categoria, 'peso_totale': float(row.peso_totale)}
                for row in result.all()
            ]
            
            return dati_grafico
            
        except Exception as e:
            logging.error(f"Errore DB in get_punteggio_per_categorie (SQL): {e}")
            raise # Rilancia l'errore per la gestione nel Service