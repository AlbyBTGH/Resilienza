# File: Classi/ClassePunteggi/Service_progetto_questionario_punteggio.py
# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePunteggi.Repository_progetto_questionario_punteggio import RepositoryProgettoQuestionarioPunteggio

class ServiceProgettoQuestionarioPunteggio:
    """
    Service dedicato al calcolo, salvataggio e recupero dei punteggi.
    """
    def __init__(self):
        self.repository = RepositoryProgettoQuestionarioPunteggio()
        self.Session = sessionmaker(bind=engine)

    # ======================================================================
    # MODIFICATO: Aggiunto parametro 'version' con default 'Baseline'
    # ======================================================================
    def calcola_e_salva_punteggio(self, id_progetto_questionario, version='Baseline'):
        """
        Esegue il calcolo aggregato del punteggio e salva i risultati in modo transazionale,
        includendo la versione ('Baseline' o 'Actual').
        """
        session = self.Session()
        try:
            # Chiama il Repository per eseguire il calcolo e l'INSERT/UPDATE
            risultati = self.repository.calcola_e_salva_punteggio_per_categoria(
                session=session,
                id_progetto_questionario=id_progetto_questionario,
                version=version # ARGOMENTO PASSATO AL REPOSITORY
            )
            
            session.commit()
            return risultati
            
        except SQLAlchemyError as e:
            session.rollback()
            # MODIFICA: Aggiunto {version} nel messaggio di log
            logging.error(f"Errore transazionale nel calcolo e salvataggio punteggio ({version}) per PQD {id_progetto_questionario}: {e}")
            raise Exception("Errore nel database durante il calcolo del punteggio.") from e
        except Exception as e:
            session.rollback()
            # MODIFICA: Aggiunto {version} nel messaggio di log
            logging.error(f"Errore generico nel calcolo e salvataggio punteggio ({version}) per PQD {id_progetto_questionario}: {e}")
            raise 

    # ======================================================================
    # MODIFICATO: get_punteggio_per_categorie per supportare il filtro versione
    # ======================================================================
    def get_punteggio_per_categorie(self, id_progetto_questionario, version=None):
        """
        Recupera il punteggio totale per ciascuna categoria di un questionario, 
        filtrando opzionalmente per versione ('Baseline' o 'Actual').
        """
        session = self.Session() # Sessione per la sola lettura
        try:
            # Chiama il Repository passando il filtro
            dati = self.repository.get_punteggio_per_categorie(
                session, 
                id_progetto_questionario, 
                version=version # FILTRO VERSIONE PASSATO AL REPOSITORY
            ) 
            
            session.close()
            return dati
            
        except Exception as e:
            session.close()
            # MODIFICA: Aggiunto {version} nel messaggio di log
            logging.error(f"Errore Service recupero punteggi per categorie ({version}): {e}")
            # Rilancia l'eccezione per essere gestita dal Controller
            raise