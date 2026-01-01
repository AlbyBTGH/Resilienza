# File: Classi/ClasseCorrettive/Service_correttiva.py
# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseCorrettive.Repository_correttiva import RepositoryCorrettiva
from datetime import datetime

class ServiceCorrettiva:
    def __init__(self):
        self.repository = RepositoryCorrettiva()
        self.Session = sessionmaker(bind=engine)

    def salva_nuova_correttiva(self, dati_correttiva, nome_utente_autore):
        """
        Salva una nuova azione correttiva in modo transazionale.
        """
        session = self.Session()
        try:
            id_pqd = dati_correttiva.get('id_progetto_questionario_domanda')
            descrizione = dati_correttiva.get('descrizione_correttiva')
            responsabile = dati_correttiva.get('responsabile')
            data_scadenza_str = dati_correttiva.get('data_scadenza')
            costo = dati_correttiva.get('costo')          
            data_effettiva_intervento_str = dati_correttiva.get('data_effettiva_intervento')
            stato = dati_correttiva.get('stato', 'Aperta')
            note = dati_correttiva.get('note') 

            if not all([id_pqd, descrizione, data_scadenza_str]):
                raise ValueError("Campi obbligatori mancanti: ID domanda, descrizione o data scadenza.")
            
            # Conversione stringa data a oggetto Date (Data Scadenza)
            try:
                data_scadenza = datetime.strptime(data_scadenza_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Formato data scadenza non valido (atteso YYYY-MM-DD).")
                
            # Conversione stringa data a oggetto Date (Data Effettiva Intervento)
            data_effettiva_intervento = None
            if data_effettiva_intervento_str:
                try:
                    data_effettiva_intervento = datetime.strptime(data_effettiva_intervento_str, '%Y-%m-%d').date()
                except ValueError:
                    # Non è un campo obbligatorio, ma se presente deve essere valido
                    raise ValueError("Formato data effettiva intervento non valido (atteso YYYY-MM-DD).")
            
            # Chiama la Repository (AGGIORNATA)
            nuova_correttiva = self.repository.save_new_correttiva(
                session=session,
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

            session.commit()
            return nuova_correttiva.id
            
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore transazionale nel salvataggio correttiva: {e}")
            raise Exception("Errore nel database durante il salvataggio della correttiva.") from e
        except Exception as e:
            session.rollback()
            logging.error(f"Errore generico nel salvataggio correttiva: {e}")
            raise
        finally:
            session.close()

    def verifica_correttiva_attiva(self, id_pqd):
        """
        Verifica l'esistenza di una correttiva attiva per l'ID domanda specificato.
        """
        session = self.Session()
        try:
            if id_pqd is None:
                raise ValueError("ID_PROGETTO_QUESTIONARIO_DOMANDA non può essere nullo.")
                
            return self.repository.check_active_correttiva(session, id_pqd)
            
        except Exception as e:
            session.rollback()
            logging.error(f"Errore nella verifica della correttiva attiva: {e}")
            raise
        finally:
            session.close()

    def get_lista_correttive(self, id_pqd):
        """Recupera la lista delle correttive per una domanda specifica in modo transazionale."""
        session = self.Session()
        try:
            lista_correttive = self.repository.get_correttive_by_pqd(
                session=session,
                id_pqd=id_pqd
            )
            session.commit()
            return lista_correttive
        except Exception as e:
            session.rollback()
            logging.error(f"Errore nel recupero della lista correttive per PQD {id_pqd}: {e}")
            raise Exception("Errore nel database durante il recupero delle correttive.") from e
        
    def get_dettaglio_correttiva(self, correttiva_id):
        """Recupera il dettaglio di una singola correttiva in modo transazionale."""
        
        # Verifica l'ID in ingresso (buona pratica)
        if correttiva_id is None:
            raise ValueError("ID Correttiva non può essere nullo.")
            
        session = self.Session()
        try:
            # Chiama il Repository
            dettaglio = self.repository.get_correttiva_by_id(session, correttiva_id)
            session.commit() 
            return dettaglio
        except Exception as e:
            session.rollback()
            logging.error(f"Errore nel recupero del dettaglio correttiva ID {correttiva_id}: {e}")
            # Rilancia l'eccezione, il Controller la gestirà
            raise 
        finally:
            session.close()