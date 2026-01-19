# File: Classi/ClasseCorrettive/Repository_correttiva.py
# -*- coding: utf-8 -*-
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
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
        
    # ======================================================================
    # Recupera Singola Correttiva per ID Primario
    # ======================================================================
    def get_correttiva_by_id(self, session, correttiva_id):
        """Recupera una singola azione correttiva per ID e la mappa in un dizionario serializzabile."""
        try:
            correttiva = (
                session.query(Correttiva)
                .filter(Correttiva.id == correttiva_id) # Filtra per l'ID primario
                .first()
            )
            
            if not correttiva:
                return None

            # Mappa l'oggetto ORM in un dizionario per il Service
            return {
                'ID': correttiva.id,
                'DESCRIZIONE': correttiva.descrizione_correttiva,
                'RESPONSABILE_ID': correttiva.responsabile, # Usa il campo del DB
                # Formatta le date per il frontend
                'DATA_SCADENZA': correttiva.data_scadenza.strftime('%Y-%m-%d') if correttiva.data_scadenza else None,
                'DATA_EFFETTIVA_INTERVENTO': correttiva.data_effettiva_intervento.strftime('%Y-%m-%d') if correttiva.data_effettiva_intervento else None,
                'STATO': correttiva.stato,
                'COSTO': correttiva.costo,
                'NOTE': correttiva.note,
                'ID_PROGETTO_QUESTIONARIO_DOMANDA': correttiva.id_progetto_questionario_domanda,
                'DATA_INSERIMENTO': correttiva.data_inserimento.strftime('%Y-%m-%d %H:%M:%S') if correttiva.data_inserimento else None
            }
        except SQLAlchemyError as e:
            # Rilancia l'errore SQL per la gestione transazionale nel Service
            raise e
        
    def update_correttiva(self, session, id_correttiva, dati_update, nome_utente_modifica):
        """Aggiorna un'azione correttiva esistente."""
        try:
            correttiva = session.query(Correttiva).get(id_correttiva)
            if not correttiva:
                raise ValueError(f"Correttiva con ID {id_correttiva} non trovata.")

            # --- Aggiornamento dei campi ---
            
            # Descrizione: Se è una stringa vuota, solleva errore perché nullable=False
            if 'descrizione_correttiva' in dati_update and dati_update['descrizione_correttiva']:
                correttiva.descrizione_correttiva = dati_update['descrizione_correttiva']
            elif 'descrizione_correttiva' in dati_update and not dati_update['descrizione_correttiva']:
                # Se il Service ha inviato '' per la descrizione, e questa è obbligatoria, solleviamo errore
                raise ValueError("Descrizione correttiva è obbligatoria.")

            if 'responsabile' in dati_update:
                correttiva.responsabile = dati_update['responsabile']
                
            # Gestione sicura della data e check nullability
            if 'data_scadenza' in dati_update:
                data_scadenza_str = dati_update['data_scadenza']
                if data_scadenza_str:
                    # Esegue la conversione solo se la stringa non è vuota
                    try:
                        correttiva.data_scadenza = datetime.strptime(data_scadenza_str, '%Y-%m-%d').date()
                    except ValueError:
                        raise ValueError("Formato data scadenza non valido (atteso YYYY-MM-DD).")
                else:
                    # Data Scadenza è nullable=False, quindi non possiamo salvarla vuota
                    raise ValueError("Data scadenza è obbligatoria.")

            if 'stato' in dati_update:
                correttiva.stato = dati_update['stato'] # L'ORM verifica l'Enum
                
            if 'costo' in dati_update:
                valore_costo = dati_update['costo']
                if isinstance(valore_costo, bool):
                    correttiva.costo = valore_costo
                elif isinstance(valore_costo, str):
                    correttiva.costo = valore_costo.lower() == 'true'
                else:
                    correttiva.costo = bool(valore_costo)

            if 'note' in dati_update:
                correttiva.note = dati_update['note']
                
            # Aggiornamento tracciabilità
            correttiva.modificato_da = nome_utente_modifica
            
            session.add(correttiva)
            return correttiva
        
        except SQLAlchemyError as e:
            session.rollback()
            # Non mostrare dettagli interni di SQLAlchemy al frontend.
            raise ValueError(f"Errore di database durante l'aggiornamento.")
        except Exception as e:
            # Questo cattura il ValueError sulla data/descrizione e lo rilancia al Controller (che lo trasforma in 400)
            raise

    def get_correttive_by_list_id_pqd(self, session, list_id_pqd):
            """
            Recupera tutte le correttive che appartengono a una lista di ID domande.
            """
            try:
                return session.query(Correttiva).filter(
                    Correttiva.id_progetto_questionario_domanda.in_(list_id_pqd)
                ).all()
            except Exception as e:
                print(f"ERRORE REPOSITORY CORRETTIVA: {e}")
                return []