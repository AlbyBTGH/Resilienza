from Classi.ClasseUtenti.Classe_t_tipiUtenti.Repository_t_tipiUtenti import Repository_t_tipiUtente


class Service_t_tipiUtenti:

    def __init__(self) -> None:
        self.repository = Repository_t_tipiUtente()

    def create_table_if_not_exists(self):
        return self.repository.create_table_if_not_exists()
    
    def create_default_tipo_utente(self):
        return self.repository.create_default_tipo_utente()
        
    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def get_all(self):
        return self.repository.get_all()
    
    def create(self):
        return self.repository.create()
    
    def update(self,public_id, nomeTipoUtente):
        return self.repository.update(public_id, nomeTipoUtente)
    
    def delete(self, public_id):
        return self.repository.delete(public_id)