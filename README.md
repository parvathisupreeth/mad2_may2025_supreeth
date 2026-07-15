# mad2_may2025_supreeth
"A role-based Placement Portal built with Flask and Vue.js for managing campus recruitment, placement drives, and student applications."
# steps to run this file
# Virtual Environtment

Run the below commands to create python virtual environment

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate # Windows

source venv/bin/activate # linux
```

```bash
pip install -r requirements.txt
```

if you want to add new package then after installing run this to update requirements.txt

```bash
pip freeze > requirements.txt
```
if directories are installed in another drive 
try this:

```bash
$env:Path += ";C:\Program Files\nodejs\"
```
# Run Backend APIs

```bash
python app.py
```

# Run Frontend

in another terminal

```bash
cd frontend
npm install
npm run dev
```

# Celery Worker in backend

```bash
celery -A celery_config.celery worker --pool=solo --loglevel=INFO

celery -A extensions.celery worker --loglevel=info --pool=solo

```

# Celery Beat

```bash
celery -A celery_config.celery beat --loglevel=INFO
```

#run --- redis-server.exe
#run ---- MailHog_windows_amd64.exe