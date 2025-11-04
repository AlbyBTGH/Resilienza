# File: Classi/ClasseRisposteCliente/Service_risposta_cliente.py
# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseRisposteCliente.Repository_risposta_cliente import RepositoryRispostaCliente

class ServiceRispostaCliente:
    def __init__(self):
        self.repository = RepositoryRispostaCliente()
        self.Session = sessionmaker(bind=engine)

    def salva_risposte_massive(self, risposte_list, nome_utente_autore):
        """
        Salva o aggiorna un elenco di risposte in modo transazionale.
        """
        session = self.Session()
        try:
            for risposta_data in risposte_list:
                id_pqd = risposta_data.get('id_progetto_questionario_domanda')
                id_risposta = risposta_data.get('id_risposta')

                if not id_pqd or not id_risposta:
                    continue # Salta risposte incomplete

                # Chiama la Repository per l'UPSERT
                self.repository.upsert_risposta(
                    session=session,
                    id_pqd=id_pqd,
                    id_risposta=id_risposta,
                    nome_utente_autore=nome_utente_autore
                )

            session.commit()
            return risposte_list
            
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore transazionale nel salvataggio risposte massive: {e}")
            raise Exception("Errore nel database durante il salvataggio massivo.") from e
        except Exception as e:
            session.rollback()
            logging.error(f"Errore generico nel salvataggio risposte massive: {e}")
            raise
        finally:
            session.close()