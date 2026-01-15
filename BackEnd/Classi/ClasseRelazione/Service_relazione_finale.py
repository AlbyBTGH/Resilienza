# File: Classi/ClasseRelazione/Service_relazione_finale.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseRelazione.Repository_relazione_finale import RepositoryRelazioneFinale

class ServiceRelazioneFinale:
    def __init__(self):
        self.repository = RepositoryRelazioneFinale()
        self.Session = sessionmaker(bind=engine)

    def salva_relazione(self, dati_relazione):
        session = self.Session()
        try:
            relazione = self.repository.upsert_relazione(session, dati_relazione)
            session.commit()
            return relazione.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def ottieni_relazione(self, id_pq):
        session = self.Session()
        try:
            return self.repository.get_by_id_pq(session, id_pq)
        finally:
            session.close()