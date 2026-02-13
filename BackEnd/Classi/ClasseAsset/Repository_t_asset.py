# Classi/ClasseAsset/Repository_t_asset.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAsset.Domain_t_asset import TAsset
import logging

class Repository_t_asset:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def create_or_update_massivo(self, id_cliente, asset_list, modificato_da):
        session = self.Session()
        count_nuovi = 0
        try:
            for nome_asset in asset_list:
                # Verifica duplicato per lo stesso cliente (case-insensitive)
                esistente = session.query(TAsset).filter(
                    TAsset.id_cliente == id_cliente,
                    TAsset.descr == nome_asset
                ).first()

                if not esistente:
                    nuovo = TAsset(
                        descr=nome_asset,
                        id_cliente=id_cliente,
                        modificato_da=modificato_da,
                        stato='DA_MAPPARE'
                    )
                    session.add(nuovo)
                    count_nuovi += 1
            
            session.commit()
            return count_nuovi
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'upload asset: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_cliente(self, id_cliente):
        session = self.Session()
        try:
            return session.query(TAsset).filter_by(id_cliente=id_cliente).all()
        finally:
            session.close()

    def get_by_cliente(self, id_cliente):
        session = self.Session()
        try:
            # Recupera tutti gli asset filtrati per ID_CLIENTE
            return session.query(TAsset).filter(TAsset.id_cliente == id_cliente).all()
        except SQLAlchemyError as e:
            logging.error(f"Errore recupero asset per cliente {id_cliente}: {str(e)}")
            return []
        finally:
            session.close()