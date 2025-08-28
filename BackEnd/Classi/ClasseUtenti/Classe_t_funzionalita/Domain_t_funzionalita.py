# Classi/ClasseUtenti/Classe_t_funzionalita/Domain_t_funzionalita.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
# Assumendo che questo import sia corretto per il tuo dominio del menu principale
from Classi.Classe_menu_principale.Domain_t_menu_principale import TMenuPrincipale 
# Rimosso l'import di TFunzionalitaUtente qui per evitare l'importazione circolare diretta
# from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Domain_t_funzionalitaUtente import TFunzionalitaUtente


class TFunzionalita(Base):
    __tablename__ = 't_funzionalita'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # La colonna 'menuPrincipale' di tipo Boolean, come da CREATE TABLE fornito.
    menuPrincipale = Column(Boolean, default=True) 

    # fkPadre per la relazione padre-figlio all'interno della stessa tabella t_funzionalita
    fkPadre = Column(Integer, ForeignKey('t_funzionalita.id'), nullable=True) 
    
    titolo = Column(String(100), nullable=True)
    label = Column(String(100), nullable=True)
    icon = Column(String(100), nullable=True)
    link = Column(String(100), nullable=True)
    ordinatore = Column(Integer, nullable=False)
    target = Column(String(15), nullable=False)
    dataCancellazione = Column(DateTime, nullable=True)
    
    # Nuova colonna fkMenuPrincipale per il collegamento a t_menu_principale
    fkMenuPrincipale = Column(Integer, ForeignKey('t_menu_principale.id'), nullable=False) 

    # Relationships
    # Modificato per usare una stringa per evitare l'importazione circolare.
    # Assicurati che TFunzionalitaUtente sia definita nel suo modulo.
    funzionalita_utente_rel = relationship("TFunzionalitaUtente", back_populates="funzionalita_rel")
    
    # Relazione con TMenuPrincipale usando fkMenuPrincipale
    menu_principale_rel = relationship("TMenuPrincipale", back_populates="funzionalita_rel", foreign_keys=[fkMenuPrincipale])
    
    # Relazione padre-figlio auto-referenziale
    # Modificato per usare una stringa per evitare l'importazione circolare.
    children = relationship("TFunzionalita", backref="parent_rel", remote_side=[id])

    def __repr__(self):
        return f"<TFunzionalita(id={self.id}, titolo='{self.titolo}', fkPadre={self.fkPadre}, fkMenuPrincipale={self.fkMenuPrincipale})>"
