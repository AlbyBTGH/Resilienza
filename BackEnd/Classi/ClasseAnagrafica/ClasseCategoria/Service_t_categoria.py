# Classi/ClasseAnagrafica/ClasseCategoria/Service_t_categoria.py

import logging
from Classi.ClasseAnagrafica.ClasseCategoria.Repository_t_categoria import Repository_t_categoria
from Classi.ClasseAnagrafica.ClasseAmbito.Repository_t_ambito import Repository_t_ambito
from datetime import datetime

class Service_t_categoria:
    def __init__(self):
        self.repository = Repository_t_categoria()
        self.ambito_repository = Repository_t_ambito()

    def create_table_if_not_exists(self):
        self.repository.create_table_if_not_exists()

    def get_all_categorie(self, id_ambito_filter: int = None):
        try:
            categorie = self.repository.get_all(id_ambito_filter)
            logging.info(f"Recuperate {len(categorie)} categorie.")
            return categorie
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero di tutte le categorie: {str(e)}")
            return []

    def get_categoria_by_id(self, categoria_id: int):
        try:
            categoria = self.repository.get_by_id(categoria_id)
            if categoria:
                logging.info(f"Recuperata categoria con ID: {categoria_id}")
            else:
                logging.warning(f"Categoria con ID: {categoria_id} non trovata.")
            return categoria
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero della categoria con ID {categoria_id}: {str(e)}")
            return None

    # Modifica qui: Aggiunto 'tipo_categoria', rimosso 'note' e 'acronimo'
    def create_categoria(self, id_ambito: int, descr: str, tipo_categoria: str = None, creato_da: str = 'system'):
        try:
            if not descr:
                return {"error": "Descrizione è obbligatoria."}, 400

            ambito_exists = self.ambito_repository.get_by_id(id_ambito)
            if not ambito_exists:
                logging.warning(f"Tentativo di creare categoria con ID ambito {id_ambito} non esistente.")
                return {"error": "Ambito specificato non esistente."}, 400

            # Rimosso il controllo sull'acronimo esistente

            new_categoria = self.repository.create(id_ambito, descr, tipo_categoria, creato_da)
            logging.info(f"Nuova categoria creata con successo (ID: {new_categoria['id']}).")
            return new_categoria, 201

        except Exception as e:
            logging.error(f"Errore nel servizio durante la creazione della categoria: {str(e)}")
            return {"error": f"Errore durante la creazione della categoria: {str(e)}"}, 500

    # Modifica qui: Aggiunto 'tipo_categoria', rimosso 'note' e 'acronimo'
    def update_categoria(self, categoria_id: int, id_ambito: int, descr: str, tipo_categoria: str = None, modificato_da: str = 'system'):
        try:
            if not descr:
                return {"error": "Descrizione è obbligatoria."}, 400

            existing_categoria = self.repository.get_by_id(categoria_id)
            if not existing_categoria:
                logging.warning(f"Tentativo di aggiornare categoria con ID {categoria_id} non trovata.")
                return {"error": "Categoria non trovata."}, 404

            ambito_exists = self.ambito_repository.get_by_id(id_ambito)
            if not ambito_exists:
                logging.warning(f"Tentativo di aggiornare categoria con ID ambito {id_ambito} non esistente.")
                return {"error": "Ambito specificato non esistente."}, 400

            # Rimosso il controllo sull'acronimo esistente per l'aggiornamento

            updated_categoria = self.repository.update(categoria_id, id_ambito, descr, tipo_categoria, modificato_da)
            logging.info(f"Categoria con ID {categoria_id} aggiornata con successo.")
            return updated_categoria, 200

        except Exception as e:
            logging.error(f"Errore nel servizio durante l'aggiornamento della categoria con ID {categoria_id}: {str(e)}")
            return {"error": f"Errore durante l'aggiornamento della categoria: {str(e)}"}, 500

    def delete_categoria(self, categoria_id: int):
        try:
            success = self.repository.delete(categoria_id)
            if success:
                logging.info(f"Categoria con ID {categoria_id} eliminata fisicamente con successo.")
                return {"message": "Categoria eliminata con successo."}, 200
            else:
                logging.warning(f"Tentativo di eliminare categoria con ID {categoria_id} non trovata.")
                return {"error": "Categoria non trovata."}, 404
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'eliminazione della categoria con ID {categoria_id}: {str(e)}")
            return {"error": f"Errore durante la cancellazione della categoria: {str(e)}"}, 500
