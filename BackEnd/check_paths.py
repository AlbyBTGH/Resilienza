# -*- coding: utf-8 -*-
import os
import sys

print("--- Informazioni sul percorso di esecuzione ---")
print(f"Current Working Directory (CWD): {os.getcwd()}")
print(f"Directory dello script (os.path.dirname(__file__)): {os.path.dirname(os.path.abspath(__file__))}\n")

print("--- sys.path (dove Python cerca i moduli) ---")
for i, p in enumerate(sys.path):
    print(f"{i}: {p}")
print("---------------------------------------------\n")

# Percorsi attesi in base all'importazione 'from Classi.ClasseForm.forms import ...'
# Relativi alla directory 'BackEnd'
base_dir_of_server_py = os.path.dirname(os.path.abspath(__file__))
expected_classi_dir = os.path.join(base_dir_of_server_py, 'Classi')
expected_classeform_dir = os.path.join(expected_classi_dir, 'ClasseForm')
expected_forms_file = os.path.join(expected_classeform_dir, 'forms.py')

print("--- Verifica esistenza cartelle e __init__.py ---")

print(f"Verifico la cartella 'Classi': {expected_classi_dir}")
print(f"  Esiste come directory: {os.path.isdir(expected_classi_dir)}")
print(f"  Contiene __init__.py: {os.path.exists(os.path.join(expected_classi_dir, '__init__.py'))}\n")

print(f"Verifico la cartella 'ClasseForm': {expected_classeform_dir}")
print(f"  Esiste come directory: {os.path.isdir(expected_classeform_dir)}")
print(f"  Contiene __init__.py: {os.path.exists(os.path.join(expected_classeform_dir, '__init__.py'))}\n")

print(f"Verifico il file 'forms.py': {expected_forms_file}")
print(f"  Esiste come file: {os.path.isfile(expected_forms_file)}\n")

print("--- Risultato previsto per l'importazione ---")
if os.path.isdir(expected_classi_dir) and \
   os.path.exists(os.path.join(expected_classi_dir, '__init__.py')) and \
   os.path.isdir(expected_classeform_dir) and \
   os.path.exists(os.path.join(expected_classeform_dir, '__init__.py')) and \
   os.path.isfile(expected_forms_file):
    print("Tutti i componenti del percorso sembrano essere al loro posto per l'importazione.")
    print("Se l'errore persiste, potrebbe esserci un problema di cache di Python.")
    print("Prova a pulire la cache di Python (cartelle __pycache__) e riavviare.")
else:
    print("ATTENZIONE: Mancano uno o pi� componenti nel percorso del modulo 'Classi.ClasseForm.forms'.")
    print("Ricontrolla attentamente la struttura delle cartelle e la presenza di tutti i file __init__.py.")

