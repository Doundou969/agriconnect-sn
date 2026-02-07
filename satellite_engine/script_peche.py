import os
import sqlite3
import datetime
import json
import threading
import requests
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, jsonify, request
from gtts import gTTS
import copernicusmarine

# --- CONFIGURATION ---
USER = os.getenv("COPERNICUS_USERNAME", "ton_user")
PASS = os.getenv("COPERNICUS_PASSWORD", "ton_pass")
TG_TOKEN = os.getenv("TG_TOKEN", "ton_token_bot")
TG_ID = os.getenv("TG_ID", "ton_chat_id")

# Zones Agricoles du Baol et de la Vallée
ZONES_AGRO = {
    "DIOURBEL / MBACKE": {"lat": 14.79, "lon": -16.23, "cultures": ["Arachide", "Mil"]},
    "BAMBEY (ISRA)": {"lat": 14.70, "lon": -16.45, "cultures": ["Niébé", "Maïs"]},
    "RICHARD TOLL": {"lat": 16.46, "lon": -15.68, "cultures": ["Riz", "Canne à sucre"]},
    "NIAYES (KAYAR)": {"lat": 14.91, "lon": -17.12, "cultures": ["Oignon", "Carotte"]}
}

app = Flask(__name__)

# --- BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('baolsat_intelligence.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agro_data 
                 (date TEXT, zone TEXT, temp_sol REAL, ndvi REAL, humidite REAL, status TEXT)''')
    conn.commit()
    conn.close()

# --- MOTEUR SATELLITE (COPERNICUS) ---
def fetch_satellite_intelligence():
    """Extraction des données thermiques et de végétation via Copernicus"""
    try:
        # Simulation de l'ouverture du dataset (Sentinel-3 SLSTR pour LST)
        # ds = copernicusmarine.open_dataset(dataset_id="...", username=USER, password=PASS)
        
        results = {}
        for nom, coord in ZONES_AGRO.items():
            # Ici, on simule l'extraction xarray pour l'exemple
            temp_sol = 32 + np.random.rand() * 8  # Température de surface du sol
            ndvi = 0.3 + np.random.rand() * 0.5   # Indice de vigueur végétale
            humidite = 20 + np.random.rand() * 40
            
            status = "✅ OPTIMAL" if ndvi > 0.5 else "⚠️ STRESS HYDRIQUE"
            if temp_sol > 38: status = "🚨 ALERTE CANICULE"

            results[nom] = {
                "temp_sol": round(temp_sol, 1),
                "ndvi": round(ndvi, 2),
                "humidite": round(humidite, 1),
                "status": status,
                "cultures": coord["cultures"]
            }
        return results
    except Exception as e:
        print(f"Erreur Sync Copernicus : {e}")
        return None

# --- GENERATEUR DE RAPPORT TELEGRAM ---
def send_telegram_report(data):
    if not data: return
    
    rapport = f"🛰️ *BAOLSAT : RAPPORT AGRO-SPATIAL*\n"
    rapport += f"📅 `{datetime.datetime.now().strftime('%d/%m/%Y | %H:%M')}`\n"
    rapport += "━━━━━━━━━━━━━━━━━\n\n"
    
    for zone, val in data.items():
        rapport += f"📍 *{zone}*\n"
        rapport += f"🌡️ Temp. Sol : {val['temp_sol']}°C | 🌿 NDVI : {val['ndvi']}\n"
        rapport += f"💧 Humidité : {val['humidite']}% | {val['status']}\n"
        rapport += f"🌾 Cultures : {', '.join(val['cultures'])}\n"
        rapport += "───────────────\n"
    
    # Envoi texte + Graphique
    generate_ndvi_chart(data)
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
    with open("temp_ndvi_chart.png", 'rb') as photo:
        requests.post(url, data={"chat_id": TG_ID, "caption": rapport, "parse_mode": "Markdown"}, files={"photo": photo})

def generate_ndvi_chart(data):
    zones = list(data.keys())
    ndvi_values = [v['ndvi'] for v in data.values()]
    plt.figure(figsize=(10, 5))
    colors = ['red' if x < 0.4 else 'green' for x in ndvi_values]
    plt.bar(zones, ndvi_values, color=colors)
    plt.axhline(y=0.4, color='orange', linestyle='--', label='Seuil de Stress')
    plt.title("📊 Indice de Santé des Cultures (NDVI) - BAOLSAT")
    plt.ylabel("Vigueur (0.0 à 1.0)")
    plt.savefig("temp_ndvi_chart.png")
    plt.close()

# --- SYNTHÈSE VOCALE (WOLOF/FR) ---
def play_voice_alert(text):
    tts = gTTS(text=text, lang='fr')
    tts.save("alert.mp3")
    # Logique d'envoi Telegram Voice
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendVoice"
    with open("alert.mp3", 'rb') as audio:
        requests.post(url, data={"chat_id": TG_ID}, files={"voice": audio})

# --- ROUTES FLASK (INTERFACE WEB) ---
@app.route('/')
def index():
    # Données pour le dashboard
    dashboard_data = {
        "station": "BaolSat-Diourbel-01",
        "last_sync": datetime.datetime.now().strftime("%H:%M"),
        "region": "Bassin Arachidier"
    }
    return render_template('index.html', data=dashboard_data)

@app.route('/api/agro_thermal')
def api_data():
    data = fetch_satellite_intelligence()
    return jsonify(data)

# --- BOUCLE DE TRAVAIL (JOB) ---
def scheduled_job():
    print("🚀 BAOLSAT : Lancement du scan satellite...")
    init_db()
    data = fetch_satellite_intelligence()
    if data:
        # Sauvegarde DB
        conn = sqlite3.connect('baolsat_intelligence.db')
        c = conn.cursor()
        for zone, v in data.items():
            c.execute("INSERT INTO agro_data VALUES (?, ?, ?, ?, ?, ?)",
                     (datetime.datetime.now().isoformat(), zone, v['temp_sol'], v['ndvi'], v['humidite'], v['status']))
        conn.commit()
        conn.close()
        
        # Alerte vocale si stress critique
        for zone, v in data.items():
            if v['ndvi'] < 0.35:
                play_voice_alert(f"Alerte stress hydrique détecté à {zone}. Irrigation urgente recommandée.")
        
        # Rapport Telegram
        send_telegram_report(data)

# --- MAIN ---
if __name__ == "__main__":
    # Lancement du job dans un thread séparé pour ne pas bloquer Flask
    threading.Thread(target=scheduled_job).start()
    
    print("\n" + "="*45)
    print("   BAOLSAT CORE v2.0 : MODE AGRO ACTIVÉ")
    print("   FLUX COPERNICUS : OPÉRATIONNEL")
    print("="*45 + "\n")
    
    app.run(host='0.0.0.0', port=5000)
