from werkzeug.security import check_password_hash

# Prendi questo hash direttamente dal tuo DB per 'configuratore.user'
hashed_password_from_db = 'pbkdf2:sha256:1000000$pghl5gf0N1Gds4Rjpbkdf2:sha256:1000000$7OpmZBbaHAuRtQ3X$e4b1344990dbb6421cbfcc902b5f2ed7009504dc1f7ace6a55223ec3b96cca74'
password_che_digiti = 'Password123!' # Assicurati che questa sia esattamente quella che digiti

if check_password_hash(hashed_password_from_db, password_che_digiti):
    print("Password OK!")
else:
    print("Password NON corrisponde!")
