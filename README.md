# Andrija Škontra završni rad

### Preduvjeti

- Python (verzija 3.6 ili novija)
- Git
- Lokalna PostgreSQL baza podataka [pogledaj](./db_spajanje.md)

### Koraci

> [!NOTE]
> Ovisno o vašoj python instalaciji, komanda `python3`
> se možda treba zamijeniti s komandom `python`

1. Lokalno klonirate projekt i pozicionirajte se unutar `zavrsni-rad` direktorija

    ```bash
    git clone https://github.com/AndrijaSkontra/zavrsni-rad && cd zavrsni-rad
    ```

2. Inicijalizirajte Python virtualno okruzenje

    ```bash
    python3 -m venv .venv
    ``` 

3. Aktivirajte Python virtualno okruzenje i pozicionirajte se unutar `project` direktorija

- Linux/MacOS:

   ```bash
   source ./.venv/bin/activate && cd project
   ```

- Windows:

  ```powershell
  .venv\Scripts\Activate.ps1; cd project
  ```

4. Instalirajte Django framework, ili sve pakete iz requierments.txt

    ```bash
    python3 -m pip install Django
    ```

5. Pokrenite Django aplikaciju

    ```bash
    python3 manage.py runserver
    ```



