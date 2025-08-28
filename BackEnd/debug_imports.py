import os
import sys

print("--- Informazioni sull'ambiente di esecuzione ---")
print(f"Directory di lavoro corrente (os.getcwd()): {os.getcwd()}")
print(f"Directory dello script (os.path.dirname(__file__)): {os.path.dirname(os.path.abspath(__file__))}\n")

print("--- Contenuto di sys.path (dove Python cerca i moduli) ---")
for i, p in enumerate(sys.path):
    print(f"{i}: {p}")
    print("---------------------------------------------------\n")

    print("--- Tentativo di importazione del modulo 'forms' ---")
    try:
        # Questo � il percorso che il tuo server.py sta cercando
        from Classi.ClasseForm import forms
        print(f"SUCCESS: Modulo 'forms' importato con successo da: {forms.__file__}")
    except ImportError as e:
        print(f"ERRORE: Impossibile importare il modulo 'forms'. Dettagli: {e}")
        print("Ci� indica che la struttura dei pacchetti o i file __init__.py non sono corretti.")
    except Exception as e:
        print(f"ERRORE INATTESO durante l'importazione: {e}")

    print("\n--- Verifica presenza file __init__.py e directories ---")

    base_path = os.path.dirname(os.path.abspath(__file__)) # c:\Python_tmp\Resilienza\progetto_resilienza\BackEnd\

    paths_to_check = [
        os.path.join(base_path, 'Classi'),
        os.path.join(base_path, 'Classi', '__init__.py'),
        os.path.join(base_path, 'Classi', 'ClasseForm'),
        os.path.join(base_path, 'Classi', 'ClasseForm', '__init__.py'),
        os.path.join(base_path, 'Classi', 'ClasseForm', 'forms.py'),
        # Aggiungi qui anche gli altri percorsi di pacchetto che usi, ad esempio:
        os.path.join(base_path, 'Classi', 'ClasseDB', '__init__.py'),
        os.path.join(base_path, 'Classi', 'Classe_menu_principale', '__init__.py'),
        os.path.join(base_path, 'Classi', 'ClasseUtenti', '__init__.py'),
        os.path.join(os.path.join(base_path, 'Classi', 'ClasseUtenti', 'Classe_t_funzionalita'), '__init__.py'),
        os.path.join(os.path.join(base_path, 'Classi', 'ClasseUtenti', 'Classe_t_funzionalitaUtenti'), '__init__.py'),
        os.path.join(os.path.join(base_path, 'Classi', 'ClasseUtenti', 'Classe_t_ruolo'), '__init__.py'),
        os.path.join(os.path.join(base_path, 'Classi', 'ClasseUtenti', 'Classe_t_utenti'), '__init__.py'),
    ]

    for p in paths_to_check:
        status = "ESISTE" if os.path.exists(p) else "NON ESISTE"
        is_dir = " (DIR)" if os.path.isdir(p) else ""
        is_file = " (FILE)" if os.path.isfile(p) else ""
        print(f"  {p}: {status}{is_dir}{is_file}")

    