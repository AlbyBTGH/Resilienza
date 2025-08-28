# Classi/ClasseUtenti/Classe_t_funzionalitaUtenti/Service_t_funzionalitaUtente.py
import logging # Assicurati che logging sia importato
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Repository_t_funzionalitaUtente import TFunzionalitaUtenteRepository
from Classi.Classe_menu_principale.Service_t_menu_principale import Service_t_menu_principale

class Service_t_FunzionalitaUtente:
    def __init__(self):
        self.repository = TFunzionalitaUtenteRepository()
        self.menu_principale_service = Service_t_menu_principale()

    def create_table_if_not_exists(self):
        return self.repository.create_table_if_not_exists()

    def get_funzionalita_utente_by_id(self, funzionalita_utente_id: int):
        return self.repository.get_funzionalita_utente_by_id(funzionalita_utente_id)

    def get_funzionalita_utenti_by_user_type(self, tipo_utente_id: int):
        return self.repository.get_funz_utenti_by_user_type(tipo_utente_id)

    def get_funzionalita_utenti_by_funzionalita(self, funzionalita_id: int):
        return self.repository.get_funzionalita_utenti_by_funzionalita(funzionalita_id)

    def get_all_funzionalita_utenti(self):
        return self.repository.get_all_funzionalita_utenti()

    def build_menu_structure(self, role_id: int):
        """
        Costruisce la struttura gerarchica del menu (padri, figli, nipoti)
        per un dato ID di ruolo e l'ID dell'applicazione 'RESILIENZA'.
        """
        logging.info(f"DEBUG Service: Inizio build_menu_structure per role_id: {role_id}")

        # Recupera l'ID del menu principale 'RESILIENZA'
        resilienza_app = self.menu_principale_service.get_by_title("RESILIENZA")
        
        if not resilienza_app:
            logging.error("ERRORE Service: Menu principale 'RESILIENZA' non trovato. Impossibile costruire il menu.")
            return []

        # Assicurati che resilienza_app sia l'oggetto Domain e non un dizionario, per accedere a .id
        # Se get_by_title restituisce un dict, potresti dover fare resilienza_app['id']
        # Basandomi sui tuoi file, get_by_title nel repository restituisce l'oggetto Domain.
        app_id = resilienza_app.id
        logging.info(f"DEBUG Service: Trovato RESILIENZA app con ID: {app_id}")

        # Passa anche app_id al repository
        data = self.repository.get_menu_data(role_id, app_id)
        logging.info(f"DEBUG Service: Dati grezzi dal repository (numero di elementi): {len(data)}")
        # logging.info(f"DEBUG Service: Dati grezzi dal repository: {data}") # Scommenta per vedere tutti i dati

        # Mappa per un accesso più rapido agli elementi per ID
        all_items_map = {item.funzionalita_id: {
            'id': item.funzionalita_id,
            'titolo': item.funzionalita_titolo,
            'label': item.funzionalita_label,
            'icon': item.funzionalita_icon,
            'link': item.funzionalita_link,
            'ordinatore': item.funzionalita_ordinatore,
            'target': item.funzionalita_target,
            'fkPadre': item.funzionalita_fkPadre,
            'fkMenuPrincipale': item.funzionalita_fkMenuPrincipale,
            'figli': [],
            'nipoti': [] # Questo campo verrà usato solo per i figli che hanno nipoti
        } for item in data}

        menu_tree = []

        # Popola i figli e i nipoti
        for item_id, item_dict in all_items_map.items():
            fkPadre = item_dict['fkPadre']
            if fkPadre is None:
                # È una voce padre
                menu_tree.append(item_dict)
            elif fkPadre in all_items_map:
                # È un figlio o nipote di una voce accessibile
                parent_of_current = all_items_map[fkPadre]
                # Determina se è un figlio diretto di un padre o un nipote
                if parent_of_current['fkPadre'] is None: # Se il genitore è un padre principale
                    parent_of_current['figli'].append(item_dict)
                else: # Se il genitore è un figlio (quindi l'elemento corrente è un nipote)
                    # Trova il "nonno" (il padre del padre)
                    grandparent_id = parent_of_current['fkPadre']
                    if grandparent_id in all_items_map:
                        grandparent_of_current = all_items_map[grandparent_id]
                        # Aggiungi il nipote al figlio corretto del nonno
                        for figlio in grandparent_of_current['figli']:
                            if figlio['id'] == fkPadre:
                                figlio['nipoti'].append(item_dict)
                                break

        # Ordina i figli e i nipoti per ordinatore
        for parent_item in menu_tree:
            parent_item['figli'].sort(key=lambda x: x['ordinatore'])
            for child_item in parent_item['figli']:
                child_item['nipoti'].sort(key=lambda x: x['ordinatore'])

        # Ordina le voci padre
        menu_tree.sort(key=lambda x: x['ordinatore'])
        
        logging.info(f"DEBUG Service: Struttura menu finale (numero di padri): {len(menu_tree)}")
        # logging.info(f"DEBUG Service: Struttura menu finale: {menu_tree}") # Scommenta per vedere la struttura completa
        return menu_tree

    def get_padri(self, role_id: int):
        logging.info(f"DEBUG Service: Inizio get_padri per role_id: {role_id}")
        resilienza_app = self.menu_principale_service.get_by_title("RESILIENZA")
        if not resilienza_app:
            logging.error("ERRORE Service: Menu principale 'RESILIENZA' non trovato in get_padri.")
            return []
        app_id = resilienza_app.id
        logging.info(f"DEBUG Service: Trovato RESILIENZA app ID: {app_id} in get_padri.")

        data = self.repository.get_menu_data(role_id, app_id)
        logging.info(f"DEBUG Service: Dati grezzi dal repository in get_padri (numero di elementi): {len(data)}")
        
        padri = []
        for item in data:
            if item.funzionalita_fkPadre is None:
                item_dict = {
                    'id': item.funzionalita_id,
                    'titolo': item.funzionalita_titolo,
                    'label': item.funzionalita_label,
                    'icon': item.funzionalita_icon,
                    'link': item.funzionalita_link,
                    'ordinatore': item.funzionalita_ordinatore,
                    'target': item.funzionalita_target,
                }
                padri.append(item_dict)
        logging.info(f"DEBUG Service: Numero di padri trovati: {len(padri)}")
        return padri
