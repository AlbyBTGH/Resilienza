# Classi/ClasseUtenti/Classe_t_utenti/Service_t_utenti.py (Assumendo questo percorso)
from Classi.ClasseUtenti.Classe_t_utenti.Repository_t_utenti import Repository_t_utenti
from werkzeug.security import check_password_hash

class Service_t_utenti:
    def __init__(self):
        self.repository = Repository_t_utenti()

    def create_table_if_not_exists(self):
        return self.repository.create_table_if_not_exists()

    def create_default_admin_user(self):
        return self.repository.create_default_admin_user()

    def login_user(self, email, password):
        user = self.repository.get_user_by_email(email)
        if user and check_password_hash(user.password, password):
            self.repository.update_user_last_access(user)
            return user
        return None

    def get_user_by_public_id(self, public_id):
        return self.repository.get_user_by_public_id(public_id)

    def create_user(self, email, password, nome, cognome, id_ruolo): # <--- CAMBIATO QUI: da fkTipoUtente a id_ruolo
        return self.repository.create_user(email, password, nome, cognome, id_ruolo)

    def change_password(self, public_id, old_password, new_password):
        return self.repository.change_password(public_id, old_password, new_password)

    # Aggiungi altri metodi di servizio se necessari per gli utenti