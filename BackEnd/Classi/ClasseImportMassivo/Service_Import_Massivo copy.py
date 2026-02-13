import pandas as pd
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine

# Import dei Domain necessari
from Classi.ClasseAnagrafica.ClasseAmbito.Domain_t_ambito import TAmbito
from Classi.ClasseAnagrafica.ClasseCategoria.Domain_t_categoria import TCategoria
from Classi.ClasseAnagrafica.ClasseDriver.Domain_t_driver import TDriver
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda

class ServiceImportMassivo:
    @staticmethod
    def esegui_importazione(file_path, utente_loggato):
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            # Lettura file
            df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            
            # Normalizziamo i nomi delle colonne per evitare errori di maiuscole/minuscole
            # df.columns = [c.strip().capitalize() for c in df.columns]

            # Normalizza tutto in MAIUSCOLO
            df.columns = [c.strip().upper() for c in df.columns]

            # Colonne attese: Ambito, Categoria, Driver, Domanda

            contatori = {"Ambiti": 0, "Categorie": 0, "Driver": 0, "Domande": 0}

            for index, row in df.iterrows():
                # --- PULIZIA DATI E CONTROLLO RIGHE VUOTE ---
                # Trasformiamo in stringa e togliamo spazi extra
                val_ambito = str(row['AMBITO']).strip()
                val_cat = str(row['CATEGORIA']).strip()
                val_driver = str(row['DRIVER']).strip()
                val_domanda = str(row['DOMANDA']).strip()

                # FILTRO ANTI-SPORCO: Salta se uno dei campi è 'nan', vuoto o troppo corto
                # Controlliamo tutti i campi prima di fare QUALSIASI operazione sul DB
                campi_da_validare = [val_ambito, val_cat, val_driver, val_domanda]

                # Se i campi fondamentali sono "nan" (vuoti in Excel) o stringhe vuote, saltiamo la riga
                if any(c.lower() == 'nan' or not c for c in campi_da_validare):
                    print(f"--- Riga {index+1} saltata: contiene campi vuoti o 'nan' ---")
                    continue

                print(f"--- Elaborazione riga {index+1} ---") # DEBUG

                # 1. GESTIONE AMBITO
                ambito = session.query(TAmbito).filter(TAmbito.descrizione.ilike(val_ambito)).first()
                if not ambito:
                    print(f"DEBUG: Ambito '{val_ambito}' non trovato, lo creo...") 
                    # Creazione acronimo sicuro
                    acronimo = val_ambito[:10].upper().replace(" ", "")
                    ambito = TAmbito(descrizione=val_ambito, codice=acronimo, modificato_da=utente_loggato)
                    session.add(ambito)
                    session.flush()
                    contatori["Ambiti"] += 1
                else:
                    print(f"DEBUG: Ambito '{val_ambito}' già esistente (ID: {ambito.id})")

                # 2. GESTIONE CATEGORIA
                categoria = session.query(TCategoria).filter(
                    TCategoria.descr.ilike(val_cat), 
                    TCategoria.id_ambito == ambito.id
                ).first()
                if not categoria:
                    print(f"DEBUG: Categoria '{val_cat}' non trovata, la creo...") 
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
                    print(f"DEBUG: Driver '{val_driver}' non trovato, lo creo...") 
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
                    print(f"DEBUG: Inserimento nuova domanda: {val_domanda[:50]}...") 
                    domanda = TDomanda(descr=val_domanda, id_driver=driver.id, modificato_da=utente_loggato)
                    session.add(domanda)
                    contatori["Domande"] += 1

            session.commit()
            msg = f"Import completato: {contatori['Ambiti']} Ambiti, {contatori['Categorie']} Categ., {contatori['Driver']} Driver, {contatori['Domande']} Domande."
            return True, msg

        except Exception as e:
            session.rollback()
            return False, f"Errore critico durante l'importazione: {str(e)}"
        finally:
            session.close()