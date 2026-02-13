import pandas as pd
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine

# Import dei Domain necessari
from Classi.ClasseAnagrafica.ClasseAmbito.Domain_t_ambito import TAmbito
from Classi.ClasseAnagrafica.ClasseCategoria.Domain_t_categoria import TCategoria
from Classi.ClasseAnagrafica.ClasseDriver.Domain_t_driver import TDriver
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
from Classi.ClasseQuestionario.Domain_t_questionario import TQuestionario # Aggiunto

class ServiceImportMassivo:
    @staticmethod
    def esegui_importazione(file_path, utente_loggato, nome_questionario=None):
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            # Lettura file
            df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            
            # Normalizza tutto in MAIUSCOLO
            df.columns = [c.strip().upper() for c in df.columns]

            contatori = {"Ambiti": 0, "Categorie": 0, "Driver": 0, "Domande": 0}
            
            # Usiamo un set per raccogliere gli oggetti Domanda (evita duplicati se la stessa riga appare più volte)
            domande_per_questionario = set()

            for index, row in df.iterrows():
                # 1. Recupero e pulizia stringhe (Prendiamo tutto subito)
                val_ambito = str(row.get('AMBITO', '')).strip()
                val_cat = str(row.get('CATEGORIA', '')).strip()
                val_driver = str(row.get('DRIVER', '')).strip()
                val_domanda = str(row.get('DOMANDA', '')).strip()

                # FILTRO ANTI-SPORCO
                campi_da_validare = [val_ambito, val_cat, val_driver, val_domanda]
                if any(c.lower() == 'nan' or not c for c in campi_da_validare):
                    continue

                # 1. GESTIONE AMBITO
                ambito = session.query(TAmbito).filter(TAmbito.descrizione.ilike(val_ambito)).first()
                if not ambito:
                    acronimo = val_ambito[:10].upper().replace(" ", "")
                    ambito = TAmbito(descrizione=val_ambito, codice=acronimo, modificato_da=utente_loggato)
                    session.add(ambito)
                    session.flush()
                    contatori["Ambiti"] += 1

                # 2. GESTIONE CATEGORIA
                categoria = session.query(TCategoria).filter(
                    TCategoria.descr.ilike(val_cat), 
                    TCategoria.id_ambito == ambito.id
                ).first()
                if not categoria:
                    categoria = TCategoria(descr=val_cat, id_ambito=ambito.id, modificato_da=utente_loggato)
                    session.add(categoria)
                    session.flush()
                    contatori["Categorie"] += 1

                # 3. GESTIONE DRIVER
                driver = session.query(TDriver).filter(
                    TDriver.descr.ilike(val_driver), 
                    TDriver.id_categoria == categoria.id
                ).first()
                if not driver:
                    driver = TDriver(descr=val_driver, id_categoria=categoria.id, modificato_da=utente_loggato)
                    session.add(driver)
                    session.flush()
                    contatori["Driver"] += 1

                # 4. GESTIONE DOMANDA
                domanda = session.query(TDomanda).filter(
                    TDomanda.descr.ilike(val_domanda), 
                    TDomanda.id_driver == driver.id
                ).first()
                if not domanda:
                    domanda = TDomanda(descr=val_domanda, id_driver=driver.id, modificato_da=utente_loggato)
                    session.add(domanda)
                    session.flush()
                    contatori["Domande"] += 1
                
                # Aggiungiamo l'oggetto domanda alla collezione per il questionario
                domande_per_questionario.add(domanda)

            # --- GESTIONE CREAZIONE QUESTIONARIO ---
            msg_quest = ""
            if nome_questionario and domande_per_questionario:
                nuovo_q = TQuestionario(
                    descr=nome_questionario,
                    creato_da=utente_loggato,
                    modificato_da=utente_loggato
                )
                # Grazie al backref 'domande' in TQuestionario, popoliamo direttamente la tabella di unione
                nuovo_q.domande = list(domande_per_questionario)
                session.add(nuovo_q)
                msg_quest = f" Creato anche questionario '{nome_questionario}' con {len(domande_per_questionario)} domande."

            session.commit()
            msg = f"Import completato: {contatori['Ambiti']} Ambiti, {contatori['Categorie']} Categ., {contatori['Driver']} Driver, {contatori['Domande']} Domande.{msg_quest}"
            return True, msg

        except Exception as e:
            session.rollback()
            return False, f"Errore critico durante l'importazione: {str(e)}"
        finally:
            session.close()