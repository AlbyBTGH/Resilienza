# Classi/ClasseUtenti/Classe_t_funzionalita/Service_t_funzionalita.py
from Classi.ClasseUtenti.Classe_t_funzionalita.Repository_t_funzionalita import TFunzionalitaRepository


class Service_t_funzionalita:
    
    
    def __init__(self):
        self.repository = TFunzionalitaRepository()

    def create_table_if_not_exists(self):
        return self.repository.create_table_if_not_exists()

    def get_all_menus(self):
        return self.repository.get_all()
    
    def get_all_by_menu_iniziale(self, fkMenuPrincipale): 
        return self.repository.get_all_by_menu_iniziale( fkMenuPrincipale )
    
    def get_menu_by_id(self, menu_id):
        return self.repository.get_by_id(menu_id)
    
    def get_all_children(self, fkPadre):
        return self.repository.get_by_padre(fkPadre)
    
    def can_access(self, user_role_id, page_link): # Modificato per usare user_role_id
        return self.repository.can_access(user_role_id, page_link)

    def get_menu_for_role_and_app(self, ruolo_id, app_id):
        """
        Recupera il menu completo (padre e figli) per un dato ruolo e applicazione.
        """
        funzionalita = self.repository.get_funzionalita_by_role_and_menu(ruolo_id, app_id)
        
        # Costruisci una struttura ad albero padre-figlio
        menu_tree = []
        funzionalita_map = {f.id: f for f in funzionalita}
        
        for f in funzionalita:
            if f.fkPadre is None: # È una voce padre
                parent_item = {
                    'id': f.id,
                    'label': f.label,
                    'link': f.link,
                    'icon': f.icon,
                    'target': f.target,
                    'ordinatore': f.ordinatore,
                    'children': []
                }
                for child in funzionalita:
                    if child.fkPadre == f.id: # È un figlio di questa voce padre
                        parent_item['children'].append({
                            'id': child.id,
                            'label': child.label,
                            'link': child.link,
                            'icon': child.icon,
                            'target': child.target,
                            'ordinatore': child.ordinatore
                        })
                # Ordina i figli
                parent_item['children'].sort(key=lambda x: x['ordinatore'])
                menu_tree.append(parent_item)
        
        # Ordina le voci padre
        menu_tree.sort(key=lambda x: x['ordinatore'])
        return menu_tree