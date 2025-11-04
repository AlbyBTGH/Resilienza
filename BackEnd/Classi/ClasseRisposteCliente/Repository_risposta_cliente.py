# File: Classi/ClasseRisposteCliente/Repository_risposta_cliente.py
# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseRisposteCliente.Domain_risposta_cliente import RispostaCliente

class RepositoryRispostaCliente:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def upsert_risposta(self, session, id_pqd, id_risposta, nome_utente_autore):
        """
        Aggiorna la risposta se esiste (cercando per id_pqd), altrimenti la crea (UPSERT).
        
        NOTA: Senza vincolo UNIQUE, l'aggiornamento si applicherà solo alla PRIMA riga 
        trovata con quell'ID_PROGETTO_QUESTIONARIO_DOMANDA.
        """
        try:
            # 1. Cerca la riga esistente
            risposta_esistente = (
                session.query(RispostaCliente)
                .filter(RispostaCliente.id_progetto_questionario_domanda == id_pqd)
                .first() 
            )

            if risposta_esistente:
                # 2. UPDATE: Aggiorna risposta e tracciabilità
                risposta_esistente.id_risposta = id_risposta
                risposta_esistente.modificato_da = nome_utente_autore
                # DATA_ULTIMA_MODIFICA si aggiorna automaticamente
                return risposta_esistente
            else:
                # 3. INSERT: Crea una nuova riga
                nuova_risposta = RispostaCliente(
                    id_progetto_questionario_domanda=id_pqd,
                    id_risposta=id_risposta,
                    modificato_da=nome_utente_autore
                )
                session.add(nuova_risposta)
                return nuova_risposta

        except SQLAlchemyError as e:
            raise e