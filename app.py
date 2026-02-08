import os, sys, datetime, sqlite3, random
from flask import Flask, render_template, request, redirect, url_for

# --- CONFIGURATION DES CHEMINS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ajout du dossier satellite_engine au PATH pour les imports
sys.path.append(os.path.join(BASE_DIR, 'satellite_engine'))

try:
    from ndvi_engine import BaolSatEngine
    sat_engine = BaolSatEngine()
    print("✅ Moteur BAOLSAT (Copernicus) : CHARGÉ")
except ImportError:
    sat_engine = None
    print("⚠️ Moteur NDVI introuvable, passage en mode simulation.")

app = Flask(__name__)
# La DB sera créée à la racine sur Render
app.config['DATABASE'] = os.path.join(BASE_DIR, 'baolsat.db')

# --- INITIALISATION DE LA DB ---
def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        # Table Chat (ex-PecheurConnect adapté)
        cursor.execute('''CREATE TABLE IF NOT EXISTS chat 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, text TEXT, time TEXT, is_critical INTEGER)''')
        # Table Bourse Agricole
        cursor.execute('''CREATE TABLE IF NOT EXISTS bourse 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, produit TEXT, prix INTEGER, tendance TEXT)''')
        
        # Données initiales si vide
        cursor.execute("SELECT count(*) FROM bourse")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO bourse (produit, prix, tendance) VALUES (?, ?, ?)", 
                [('Arachide', 285, 'up'), ('Riz Local', 425, 'down'), ('Oignon', 350, 'up')])
        conn.commit()

init_db()

# --- LOGIQUE MÉTIER ---
def get_map_data():
    zones = {
        "Saint-Louis": [16.01, -16.48], "Dahra": [15.33, -15.48],
        "Kaolack": [14.14, -16.07], "Ziguinchor": [12.58, -16.27]
    }
    agri_data = []
    for zone, coords in zones.items():
        # Simulation ou appel API Copernicus via le moteur
        val = sat_engine.get_satellite_insight(zone) if sat_engine else {"vigueur": random.uniform(0.4, 0.8)}
        agri_data.append({
            "zone": zone, "lat": coords[0], "lng": coords[1],
            "ndvi": round(val.get("vigueur", 0.5), 2),
            "status": "Optimal" if val.get("vigueur", 0.5) > 0.6 else "Alerte Stress"
        })
    return agri_data

# --- ROUTES ---
@app.route('/')
def home():
    try:
        data = get_map_data()
        with sqlite3.connect(app.config['DATABASE']) as conn:
            conn.row_factory = sqlite3.Row
            prices = conn.execute("SELECT * FROM bourse").fetchall()
            messages = conn.execute("SELECT * FROM chat ORDER BY id DESC LIMIT 10").fetchall()
        
        return render_template('index.html', 
                               agri_data=data, 
                               prices=prices, 
                               messages=messages,
                               now=datetime.datetime.now().strftime("%H:%M"))
    except Exception as e:
        return f"Erreur BAOLSAT : {str(e)}", 500

if __name__ == '__main__':
    # Indispensable pour Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
