# Classi/ClasseAnagrafica/ClasseCategoria/Repository_t_categoria.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseCategoria.Domain_t_categoria import TCategoria
from Classi.ClasseAnagrafica.ClasseAmbito.Domain_t_ambito import TAmbito
import logging
from datetime import datetime

class Repository_t_categoria:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        session = self.Session()
        try:
            TCategoria.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'categoria' creata o già esistente (secondo il modello TCategoria).")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'categoria': {str(e)}")
            raise
        finally:
            session.close()

    def get_all(self, id_ambito_filter: int = None):
        session = self.Session()
        try:
            query = session.query(TCategoria, TAmbito).join(TAmbito)
            if id_ambito_filter is not None:
                query = query.filter(TCategoria.id_ambito == id_ambito_filter)

            categorie = query.all()
            
            result = []
            for cat_obj, ambito_obj in categorie:
                result.append({
                    'id': cat_obj.id,
                    'id_ambito': cat_obj.id_ambito,
                    'descr': cat_obj.descr,
                    'tipo_categoria': cat_obj.tipo_categoria, # Aggiunto: tipo_categoria
                    'ambito_descrizione': ambito_obj.descrizione,
                    'data_ultima_modifica': cat_obj.data_ultima_modifica.isoformat() if cat_obj.data_ultima_modifica else None,
                    'modificato_da': cat_obj.modificato_da
                })
            logging.info(f"Recuperate {len(result)} categorie.")
            return result
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero di tutte le categorie: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_id(self, categoria_id: int):
        session = self.Session()
        try:
            categoria = session.query(TCategoria, TAmbito).join(TAmbito).filter(TCategoria.id == categoria_id).first()
            if categoria:
                cat_obj, ambito_obj = categoria
                return {
                    'id': cat_obj.id,
                    'id_ambito': cat_obj.id_ambito,
                    'descr': cat_obj.descr,
                    'tipo_categoria': cat_obj.tipo_categoria, # Aggiunto: tipo_categoria
                    'ambito_descrizione': ambito_obj.descrizione,
                    'data_ultima_modifica': cat_obj.data_ultima_modifica.isoformat() if cat_obj.data_ultima_modifica else None,
                    'modificato_da': cat_obj.modificato_da
                }
            return None
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero categoria {categoria_id}: {str(e)}")
            raise
        finally:
            session.close()

    # Rimosso: get_by_acronimo
    # Rimosso: get_by_acronimo_excluding_self

    # Modifica qui: Aggiunto 'tipo_categoria', rimosso 'note' e 'acronimo'
    def create(self, id_ambito: int, descr: str, tipo_categoria: str = None, creato_da: str = 'system'):
        session = self.Session()
        try:
            new_categoria = TCategoria(
                id_ambito=id_ambito,
                descr=descr,
                tipo_categoria=tipo_categoria, # Aggiunto: tipo_categoria
                modificato_da=creato_da,
                data_ultima_modifica=datetime.now()
            )
            session.add(new_categoria)
            session.commit()
            session.refresh(new_categoria)
            logging.info(f"Categoria '{new_categoria.descr}' creata con successo (ID: {new_categoria.id}).")
            
            return {
                'id': new_categoria.id,
                'id_ambito': new_categoria.id_ambito,
                'descr': new_categoria.descr,
                'tipo_categoria': new_categoria.tipo_categoria, # Aggiunto: tipo_categoria
                'data_ultima_modifica': new_categoria.data_ultima_modifica.isoformat() if new_categoria.data_ultima_modifica else None,
                'modificato_da': new_categoria.modificato_da
            }
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nella creazione della categoria: {str(e)}")
            raise
        finally:
            session.close()

    # Modifica qui: Aggiunto 'tipo_categoria', rimosso 'note' e 'acronimo'
    def update(self, categoria_id: int, id_ambito: int, descr: str, tipo_categoria: str = None, modificato_da: str = 'system'):
        session = self.Session()
        try:
            categoria = session.query(TCategoria).filter_by(id=categoria_id).first()
            if categoria:
                categoria.id_ambito = id_ambito
                categoria.descr = descr
                categoria.tipo_categoria = tipo_categoria # Aggiunto: tipo_categoria
                categoria.data_ultima_modifica = datetime.now()
                categoria.modificato_da = modificato_da
                session.commit()
                session.refresh(categoria)
                logging.info(f"Categoria {categoria_id} aggiornata.")
                
                return {
                    'id': categoria.id,
                    'id_ambito': categoria.id_ambito,
                    'descr': categoria.descr,
                    'tipo_categoria': categoria.tipo_categoria, # Aggiunto: tipo_categoria
                    'data_ultima_modifica': categoria.data_ultima_modifica.isoformat() if categoria.data_ultima_modifica else None,
                    'modificato_da': categoria.modificato_da
                }
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento della categoria {categoria_id}: {str(e)}")
            raise
        finally:
            session.close()

    def delete(self, categoria_id: int):
        session = self.Session()
        try:
            categoria = session.query(TCategoria).filter_by(id=categoria_id).first()
            if categoria:
                session.delete(categoria)
                session.commit()
                logging.info(f"Categoria {categoria_id} eliminata fisicamente.")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione della categoria {categoria_id}: {str(e)}")
            raise
        finally:
            session.close()
