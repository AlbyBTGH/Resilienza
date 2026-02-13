# Classi/ClasseAsset/Service_t_asset.py
# -*- coding: utf-8 -*-
import logging
from Classi.ClasseAsset.Repository_t_asset import Repository_t_asset

class Service_t_asset:
    def __init__(self):
        self.repository = Repository_t_asset()

    def _to_dict(self, asset):
        return {
            'id': asset.id,
            'descr': asset.descr,
            'id_cliente': asset.id_cliente,
            'r_val': asset.r_val,
            'i_val': asset.i_val,
            'd_val': asset.d_val,
            'v_score': asset.v_score,
            'stato': asset.stato,
            'id_driver': asset.id_driver
        }

    def import_from_list(self, id_cliente, asset_list, utente):
        try:
            nuovi = self.repository.create_or_update_massivo(id_cliente, asset_list, utente)
            return {"message": f"Importati {nuovi} nuovi asset"}, 201
        except Exception as e:
            logging.error(f"Errore nel servizio asset: {str(e)}")
            return {"error": str(e)}, 500
        
    def get_assets_by_cliente(self, id_cliente):
        try:
            assets = self.repository.get_by_cliente(id_cliente)
            return [self._to_dict(a) for a in assets], 200
        except Exception as e:
            logging.error(f"Errore nel servizio asset (get_by_cliente): {str(e)}")
            return {"error": str(e)}, 500