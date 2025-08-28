# Classi/ClasseUtenti/Classe_t_funzionalitaUtenti/Repository_t_funzionalitaUtente.py

import logging # Assicurati che logging sia importato
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Domain_t_funzionalitaUtente import TFunzionalitaUtente
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.Classe_menu_principale.Domain_t_menu_principale import TMenuPrincipale
from Classi.ClasseUtenti.Classe_t_ruolo.Domain_t_ruolo import TRuolo
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine, SessionLocal
from sqlalchemy.orm import sessionmaker

class TFunzionalitaUtenteRepository:
    def __init__(self):
        self.Session = SessionLocal

    def create_table_if_not_exists(self):
        session = self.Session()
        try:
            TFunzionalitaUtente.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 't_funzionalita_utente' creata o già esistente.")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 't_funzionalita_utente': {str(e)}")
            raise
        finally:
            session.close()

    def get_funz_utenti_by_user_type(self, tipo_utente_id: int):
        session = self.Session()
        try:
            funzionalita_utenti = session.query(TFunzionalitaUtente).filter(
                TFunzionalitaUtente.fkIdRuolo == tipo_utente_id
            ).all()

            funzionalita_utenti_dicts = []
            for funz in funzionalita_utenti:
                funz_dict = {
                    'id': funz.id,
                    'fkIdRuolo': funz.fkIdRuolo,
                    'fkFunzionalita': funz.fkFunzionalita,
                    'permessi': funz.permessi
                }
                funzionalita_utenti_dicts.append(funz_dict)
            return funzionalita_utenti_dicts
        finally:
            session.close()

    def get_funzionalita_utente_by_id(self, funzionalita_utente_id: int):
        session = self.Session()
        try:
            funzionalita_utente = session.query(TFunzionalitaUtente).get(funzionalita_utente_id)
            if funzionalita_utente:
                return {
                    'id': funzionalita_utente.id,
                    'fkIdRuolo': funzionalita_utente.fkIdRuolo,
                    'fkFunzionalita': funzionalita_utente.fkFunzionalita,
                    'permessi': funzionalita_utente.permessi,
                    'label': funzionalita_utente.funzionalita_rel.label if funzionalita_utente.funzionalita_rel else None,
                    'link': funzionalita_utente.funzionalita_rel.link if funzionalita_utente.funzionalita_rel else None
                }
            return None
        finally:
            session.close()

    def get_funzionalita_utenti_by_funzionalita(self, funzionalita_id: int):
        session = self.Session()
        try:
            funzionalita_utenti = session.query(TFunzionalitaUtente).filter(
                TFunzionalitaUtente.fkFunzionalita == funzionalita_id
            ).all()

            funzionalita_utenti_dicts = []
            for funz in funzionalita_utenti:
                funz_dict = {
                    'id': funz.id,
                    'fkIdRuolo': funz.fkIdRuolo,
                    'fkFunzionalita': funz.fkFunzionalita,
                    'permessi': funz.permessi
                }
                funzionalita_utenti_dicts.append(funz_dict)
            return funzionalita_utenti_dicts
        finally:
            session.close()

    def get_all_funzionalita_utenti(self):
        session = self.Session()
        try:
            funzionalita_utenti = session.query(TFunzionalitaUtente).all()
            return [{'id': f.id, 'fkIdRuolo': f.fkIdRuolo, 'fkFunzionalita': f.fkFunzionalita, 'permessi': f.permessi} for f in funzionalita_utenti]
        finally:
            session.close()

    def get_menu_data(self, role_id: int, app_id: int):
        """
        Recupera i dati del menu per un dato ID di ruolo e ID di applicazione,
        filtrando per permessi e funzionalità non cancellate,
        e includendo informazioni da t_funzionalita e t_menu_principale.
        """
        session = self.Session()
        try:
            logging.info(f"DEBUG Repository: get_menu_data chiamato con role_id={role_id}, app_id={app_id}")
            results = (
                session.query(
                    TFunzionalita.id.label('funzionalita_id'),
                    TFunzionalita.titolo.label('funzionalita_titolo'),
                    TFunzionalita.label.label('funzionalita_label'),
                    TFunzionalita.icon.label('funzionalita_icon'),
                    TFunzionalita.link.label('funzionalita_link'),
                    TFunzionalita.ordinatore.label('funzionalita_ordinatore'),
                    TFunzionalita.target.label('funzionalita_target'),
                    TFunzionalita.fkPadre.label('funzionalita_fkPadre'),
                    TFunzionalita.fkMenuPrincipale.label('funzionalita_fkMenuPrincipale'),
                    TMenuPrincipale.titolo.label('menu_principale_titolo'),
                    TMenuPrincipale.label.label('menu_principale_label')
                )
                .select_from(TFunzionalitaUtente) # Aggiunto per specificare la tabella di partenza
                .join(TFunzionalita, TFunzionalitaUtente.fkFunzionalita == TFunzionalita.id)
                .outerjoin(TMenuPrincipale, TFunzionalita.fkMenuPrincipale == TMenuPrincipale.id)
                .filter(
                    TFunzionalitaUtente.fkIdRuolo == role_id,
                    TFunzionalitaUtente.permessi == True,
                    TFunzionalita.dataCancellazione.is_(None),
                    TFunzionalita.fkMenuPrincipale == app_id
                )
                .order_by(TFunzionalita.ordinatore)
                .all()
            )
            logging.info(f"DEBUG Repository: Trovati {len(results)} elementi per role_id={role_id}, app_id={app_id}")
            # logging.info(f"DEBUG Repository: Risultati query: {results}") # Scommenta per vedere i risultati completi
            return results
        except SQLAlchemyError as e:
            logging.error(f"ERRORE Repository: Errore in get_menu_data per ruolo {role_id} e app {app_id}: {str(e)}")
            return []
        finally:
            session.close()

