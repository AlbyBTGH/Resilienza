from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Domain_t_tipiUtenti import TTipiUtenti
from werkzeug.exceptions import NotFound
import logging
import uuid

class Repository_t_tipiUtente:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def create_table_if_not_exists(self):
        """Crea la tabella t_tipi_utenti se non esiste già."""
        try:
            # Crea la tabella t_tipi_utenti se non esiste
            TTipiUtenti.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 't_tipi_utenti creata o già esistente.")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 't_tipi_utenti': {str(e)}")
            raise


    def create_default_tipo_utente(self):
        try:
            # UUID predefinito per il Admin
            default_uuid = str(uuid.uuid4())

            # Verifica se esiste già un tipo utente con il nome Admin
            tipo_utente = self.session.query(TTipiUtenti).filter_by(nomeTipoUtente='Admin').first()

            if not tipo_utente:
                tipo_utente = TTipiUtenti(public_id=default_uuid, nomeTipoUtente='Admin')
                self.session.add(tipo_utente)
                self.session.commit()
                print("Admin creato con successo.")
            else:
                print("Il Admin esiste già.")

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Errore durante la creazione del tipo utente: {e}")
        finally:
            if self.session:
                self.session.close()


    def get_by_id(self, id):
        try:
            result = self.session.query(TTipiUtenti).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'public_id':result.public_id, 'nomeTipoUtente': result.nomeTipoUtente}
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error getting alimento by ID {id}: {e}")
            return {'Error': str(e)}, 400
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

        
    def get_all(self):
        try:
            results = self.session.query(TTipiUtenti).all()
            return [{'id': result.id, 'public_id':result.public_id, 'nomeTipoUtente': result.nomeTipoUtente} for result in results]

        except Exception as e:
            # Se si verifica un'eccezione, esegui il rollback della sessione
            self.session.rollback()
            return {'Error': str(e)}, 500

        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            self.session.close()


    def create(self, nomeTipoUtente):
        try:
            # Crea l'oggetto TSchede
            tipo_utente = TTipiUtenti(
                public_id=str(uuid.uuid4()),
                nomeTipoUtente=nomeTipoUtente,

            )

            # Aggiungi l'oggetto alla sessione
            self.session.add(tipo_utente)

            # Esegui il commit
            self.session.commit()

            # Ottieni l'ID del nuovo tipo utente
            new_id = tipo_utente.id

            print(f"Tipo utente aggiunto con successo! ID: {new_id}")
            return new_id

        except Exception as e:
            # Rollback in caso di errore
            self.session.rollback()

            # Stampa l'errore per il debug
            print(f"Errore durante il commit al database: {str(e)}")

            return {'Error': str(e)}, 500

        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def update(self,public_id, nomeTipoUtente,):
        try:
            tipoUtente = self.session.query(TTipiUtenti).filter_by(public_id=public_id).first()
            if tipoUtente:
                tipoUtente.nomeTipoUtente = nomeTipoUtente
            
                self.session.commit()
                return {'alimento': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating tipo utente with ID {id}: {e}")
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()
        
        
    def delete(self, public_id):
        try:
            # Cerca l'elemento da eliminare in base a `public_id`
            tipoUtente = self.session.query(TTipiUtenti).filter_by(public_id=public_id).first()
            
            if tipoUtente:
                # Se esiste, rimuovilo dalla sessione
                self.session.delete(tipoUtente)
                
                # Commit delle modifiche
                self.session.commit()
                
                return {'message': f'Tipo utente with public_id {public_id} deleted successfully'}, 200
            else:
                return {'Error': f'No match found for this public_id: {public_id}'}, 404
        
        except Exception as e:
            # Rollback in caso di errore
            self.session.rollback()
            logging.error(f"Error deleting tipo utente with public_id {public_id}: {e}")
            return {'Error': str(e)}, 500
        
        finally:
            # Chiudi la sessione per evitare perdite di risorse
            if self.session:
                self.session.close()



            