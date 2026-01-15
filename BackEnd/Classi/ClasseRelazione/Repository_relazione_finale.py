# File: Classi/ClasseRelazione/Repository_relazione_finale.py
from Classi.ClasseRelazione.Domain_relazione_finale import RelazioneFinale

class RepositoryRelazioneFinale:
    def upsert_relazione(self, session, dati):
        try:
            # 1. Ricerca: usa il nome dell'attributo del Domain (minuscolo)
            relazione = session.query(RelazioneFinale).filter_by(
                id_progetto_questionario=dati['id_pq']
            ).first()

            if not relazione:
                # 2. Crea l'istanza senza parametri per evitare l'errore gkpj
                relazione = RelazioneFinale()
                session.add(relazione)

            # 3. Assegnazione manuale agli attributi del Domain (NON i nomi SQL)
            # Questi nomi a sinistra devono essere IDENTICI a quelli nel Domain_relazione_finale.py
            relazione.id_progetto_questionario = dati['id_pq']
            relazione.sintesi_introduttiva = dati.get('sintesi_introduttiva')
            relazione.analisi_criticita_iniziali = dati.get('analisi_criticita')
            relazione.descrizione_interventi = dati.get('descrizione_interventi')
            relazione.conclusioni_analista = dati.get('conclusioni_analista')
            relazione.firma_analista = dati.get('firma_analista')
            relazione.img_radar_baseline = dati.get('img_radar_baseline')
            relazione.img_radar_actual = dati.get('img_radar_actual')
            relazione.stato = dati.get('stato', 'COMPLETATA')
            
            # Sincronizza i cambiamenti
            session.flush()
            return relazione
        except Exception as e:
            print(f"ERRORE REPOSITORY: {e}")
            raise e
        
    def get_by_id_pq(self, session, id_pq):
        return session.query(RelazioneFinale).filter_by(id_progetto_questionario=id_pq).first()