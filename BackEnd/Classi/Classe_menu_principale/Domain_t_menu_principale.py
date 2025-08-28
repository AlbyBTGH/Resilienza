# Classi/Classe_menu_principale/Domain_t_menu_principale.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TMenuPrincipale(Base):
    __tablename__ = 't_menu_principale' 

    id = Column(Integer, primary_key=True, autoincrement=True)
    titolo = Column(String(100), default=None)
    label = Column(String(100), default=None)
    icon = Column(String(100), default=None)
    link = Column(String(100), default=None)
    ordinatore = Column(Integer, nullable=False)
    foto = Column(String(255), default=None)
    target = Column(String(15), nullable=False)
    dataCancellazione = Column(DateTime, default=None)

    # Relationship with TFunzionalita
    funzionalita_rel = relationship('TFunzionalita', back_populates='menu_principale_rel')

    def __repr__(self):
        return f"<TMenuPrincipale(id={self.id}, titolo='{self.titolo}', label='{self.label}')>"