# Swastik_Paints

## PostgreSQL setup

Install the Python dependencies:

```powershell
python -m pip install -r requirements.txt
````

Create a PostgreSQL database named `swastik_paints`.

Create a `.env` file in the project root:

```env
POSTGRES_DB=swastik_paints
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

The `.env` file is ignored by Git and should not be committed.

Apply the migrations:

```powershell
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```
