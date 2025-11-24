# File: Classi/ClasseCorrettive/Repository_correttiva.py
# -*- coding: utf-8 -*-
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseCorrettive.Domain_correttiva import Correttiva

class RepositoryCorrettiva:
    """Gestisce le operazioni CRUD per la tabella CORRETTIVA."""

    def save_new_correttiva(self, session, id_pqd, descrizione, responsabile, data_scadenza, costo, nome_utente_autore, data_effettiva_intervento=None, stato='Aperta', note=None):
        """Salva una nuova azione correttiva."""
        try:
            nuova_correttiva = Correttiva(
                id_pqd=id_pqd,
                descrizione=descrizione,
                responsabile=responsabile,
                data_scadenza=data_scadenza,
                costo=costo,
                nome_utente_autore=nome_utente_autore,
                data_effettiva_intervento=data_effettiva_intervento,
                stato=stato,
                note=note
            )
            session.add(nuova_correttiva)
            session.flush() # Ottiene l'ID
            return nuova_correttiva
        except SQLAlchemyError as e:
            raise e
        
    def check_active_correttiva(self, session, id_pqd):
        """
        Verifica se esiste una correttiva Aperta, In Corso o Pending per un dato ID_PROGETTO_QUESTIONARIO_DOMANDA.
        """
        try:
            # Stati considerati "attivi" o "in corso"
            active_states = ['Aperta', 'In Corso', 'Pending'] 
            
            # Conta quante righe soddisfano i criteri
            count = session.query(Correttiva).filter(
                Correttiva.id_progetto_questionario_domanda == id_pqd,
                Correttiva.stato.in_(active_states)
            ).count()
            
            return count > 0
        except SQLAlchemyError as e:
            raise e
        
    def get_correttive_by_pqd(self, session, id_pqd):
        """Recupera tutte le correttive (aperte, completate, ecc.) per un dato ID_PROGETTO_QUESTIONARIO_DOMANDA."""
        try:
            correttive = (
                session.query(Correttiva)
                .filter(Correttiva.id_progetto_questionario_domanda == id_pqd)
                .order_by(Correttiva.data_inserimento.desc())
                .all()
            )
            # Converte gli oggetti Correttiva in un formato serializzabile (lista di dict)
            return [
                {
                    'id': c.id,
                    'descrizione_correttiva': c.descrizione_correttiva,
                    'responsabile': c.responsabile,
                    'data_scadenza': c.data_scadenza.strftime('%Y-%m-%d') if c.data_scadenza else None,
                    'data_effettiva_intervento': c.data_effettiva_intervento.strftime('%Y-%m-%d') if c.data_effettiva_intervento else None,
                    'stato': c.stato,
                    'costo': c.costo,
                    'note': c.note,
                    'data_inserimento': c.data_inserimento.strftime('%Y-%m-%d %H:%M:%S') if c.data_inserimento else None,
                    'modificato_da': c.modificato_da
                }
                for c in correttive
            ]
        except SQLAlchemyError as e:
            raise e