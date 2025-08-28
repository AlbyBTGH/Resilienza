from werkzeug.security import generate_password_hash

password_desiderata = "Password123!"
# Assicurati che il metodo sia lo stesso usato nel tuo Repository_t_utenti.py
hashed_password_for_update = generate_password_hash(password_desiderata, method='pbkdf2:sha256')

print(f"L'hash di '{password_desiderata}' è: {hashed_password_for_update}")