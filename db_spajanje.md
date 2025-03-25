### MacOS koraci za pokretanje baze

1. `brew install postgresql@15` zatim `brew services start postgresql@15`
2. Na kraj `.zshrc`/`.bashrc` file-a dodati: `export PATH="/opt/homebrew/Cellar/postgresql@15/15.12_1/bin:$PATH"`
3. `createdb zavrsnibaza`
4. `psql postgres`
5. `select current_user;`
6. `alter user current_user with password 'password';` zatim `exit`
7. U ~/.pg_service.conf staviti
```
[zavrsni]
host=localhost
user=current_user
dbname=zavrsnibaza
port=5432
```
8. U ~/.my_pgpass staviti
```
localhost:5432:zavrsnibaza:current_user:password
```

9. Instalirati (u aktivirani venv) `python3 -m pip install "psycopg[binary]"`

10. Zatim se pozicionirati se u `/project` `python3 manage.py migrate`

---

TODO:
 - [ ] Linux (Ubuntu)  
 - [ ] Windows

