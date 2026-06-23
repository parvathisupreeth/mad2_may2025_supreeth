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