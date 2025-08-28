from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TTipiUtenti(Base):
    __tablename__ = 't_tipi_utenti'

    id = Column(Integer, autoincrement=True, primary_key=True)
    public_id = Column(String(255), nullable=True, unique=True)  # ad esempio UUID
    nomeTipoUtente = Column(String(50), nullable=True)  

    
    