### MacOS koraci za pokretanje baze

1. `brew install postgresql@15` zatim `brew services start postgresql@15`
ili `sudo systemctl start postgresql`

Samo linux:
1.1 Prebaciti se na postgres (novo kreirani user)
`sudo -i -u postgres`

1.2.
`psql`

1.3.
```sql
CREATE DATABASE zavrsnibaza;
CREATE USER <username> WITH PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE zavrsnibaza TO <username>;
alter user root with superuser;
```



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

