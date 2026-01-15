# File: Classi/ClasseRelazione/Domain_relazione_finale.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, text, String, Text, Numeric
from Classi.ClasseDB.db_connection import Base 

class RelazioneFinale(Base):
    __tablename__ = 'relazione_finale'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    id_progetto_questionario = Column('ID_PROGETTO_QUESTIONARIO', Integer, 
                                      ForeignKey('progetto_questionario.ID'), 
                                      unique=True, nullable=False)
    
    data_generazione = Column('DATA_GENERAZIONE', DateTime, server_default=text('CURRENT_TIMESTAMP'))
    sintesi_introduttiva = Column('SINTESI_INTRODUTTIVA', Text, nullable=True)
    analisi_criticita_iniziali = Column('ANALISI_CRITICITA_INIZIALI', Text, nullable=True)
    descrizione_interventi = Column('DESCRIZIONE_INTERVENTI', Text, nullable=True)
    conclusioni_analista = Column('CONCLUSIONI_ANALISTA', Text, nullable=True)
    
    score_baseline = Column('SCORE_BASELINE', Numeric(5, 4), nullable=True)
    score_actual = Column('SCORE_ACTUAL', Numeric(5, 4), nullable=True)
    
    img_radar_baseline = Column('IMG_RADAR_BASELINE', Text, nullable=True) 
    img_radar_actual = Column('IMG_RADAR_ACTUAL', Text, nullable=True)     
    
    firma_analista = Column('FIRMA_ANALISTA', String(150), nullable=True)
    stato = Column('STATO', String(20), default='BOZZA')