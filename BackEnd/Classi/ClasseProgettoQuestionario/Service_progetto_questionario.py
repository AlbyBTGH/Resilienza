# File: Classi/ClasseProgettoQuestionario/Service_progetto_questionario.py
# -*- coding: utf-8 -*-
import logging
from Classi.ClasseProgettoQuestionario.Repository_progetto_questionario import RepositoryProgettoQuestionario 
from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario

class ServiceProgettoQuestionario:
    def __init__(self):
        self.repository = RepositoryProgettoQuestionario()

    # --- METODO ESISTENTE (LASCIATO INVARIATO) ---
    def associate_questionario(self, id_progetto, id_questionario, domande_gruppo_list):
        # ... (Logica per l'associazione)
        try:
            pq = self.repository.associate_questionario(id_progetto, id_questionario, domande_gruppo_list)
            return {"id": pq.id, "id_progetto": pq.id_progetto, "id_questionario": pq.id_questionario}, 201
        except Exception as e:
            logging.error(f"Errore nel service nell'associare questionario: {str(e)}")
            return {"error": "Errore interno"}, 500


    # 🟢 METODO AGGIORNATO PER IL DETTAGLIO REPORT
    def get_dettaglio_report(self, id_progetto_questionario: int, nome_utente_autore: str):
        """
        Recupera i dati del report di dettaglio (domande e risposte) delegando al repository,
        filtrando la risposta salvata per l'utente loggato.
        """
        try:
            # 🟢 Passa il nome utente al repository
            domande_risposte_strutturate = self.repository.get_dettaglio_domande_risposte(
                id_progetto_questionario, 
                nome_utente_autore # <--- Parametro cruciale
            )
            
            return domande_risposte_strutturate
            
        except Exception as e:
            # Cattura qualsiasi errore dal Repository (es. SQLAlchemyError)
            logging.error(f"Errore nel service nel recupero dettaglio report per PQD ID {id_progetto_questionario} e utente {nome_utente_autore}: {str(e)}")
            # Rilancia l'eccezione per farla gestire al Controller che gestirà il 500
            raise