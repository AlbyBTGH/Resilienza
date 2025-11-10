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

    def calcola_e_salva_punteggio(self, id_progetto_questionario):
        """
        Esegue il calcolo aggregato del punteggio e salva i risultati in modo transazionale.
        """
        session = self.Session()
        try:
            # Chiama il Repository per eseguire il calcolo e l'INSERT/UPDATE
            risultati = self.repository.calcola_e_salva_punteggio_per_categoria(
                session=session,
                id_progetto_questionario=id_progetto_questionario
            )
            
            session.commit()
            return risultati
            
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore transazionale nel calcolo e salvataggio punteggio per PQD {id_progetto_questionario}: {e}")
            raise Exception("Errore nel database durante il calcolo del punteggio.") from e
        except Exception as e:
            session.rollback()
            logging.error(f"Errore generico nel calcolo e salvataggio punteggio per PQD {id_progetto_questionario}: {e}")
            raise 

    # ======================================================================
    # ⭐ METODO CORRETTO: Recupero dati per grafico radar
    # Il nome è ora allineato con la chiamata nel Controller!
    # ======================================================================
    def get_punteggio_per_categorie(self, id_progetto_questionario):
        """Recupera il punteggio totale per ciascuna categoria di un questionario."""
        session = self.Session() # Sessione per la sola lettura
        try:
            # Chiama il Repository. Assumiamo che il Repository usi questo stesso nome
            # o il nome che era stato deciso in precedenza (es. get_punteggi_per_grafico)
            dati = self.repository.get_punteggio_per_categorie(session, id_progetto_questionario) 
            
            session.close()
            return dati
            
        except Exception as e:
            session.close()
            logging.error(f"Errore Service recupero punteggi per categorie: {e}")
            # Rilancia l'eccezione per essere gestita dal Controller
            raise