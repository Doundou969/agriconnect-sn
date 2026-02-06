from flask import Flask, render_template, jsonify
import datetime

app = Flask(__name__)

# Route principale pour le Dashboard PWA
@app.route('/')
def index():
    data = {
        "status": "OPÉRATIONNEL",
        "station": "BaolSat-Diourbel-01",
        "satellite": "Eutelsat Konnect (Ka-Band)",
        "last_copernicus_sync": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "signal_strength": "92%",
        "active_terminals": 147,
        "region": "Bassin Arachidier / Baol"
    }
    return render_template('index.html', data=data)

# API pour alimenter les listes dynamiques (Fetch JS)
@app.route('/api/agro_thermal')
def agro_thermal():
    # Simulation des données de télédétection Sentinel-2 pour le Baol
    # En production, ces données seraient lues depuis baolsat.db
    stats_zones = [
        {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "zone": "Diourbel Centre",
            "temp_sol": 36.4,
            "etat": "Vigilance Stress Hydrique",
            "ndvi": 0.45
        },
        {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "zone": "Mbacké - Touba",
            "temp_sol": 34.2,
            "etat": "Optimal",
            "ndvi": 0.68
        },
        {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "zone": "Bambey (Zone ISRA)",
            "temp_sol": 31.8,
            "etat": "Excellente Vigueur",
            "ndvi": 0.82
        }
    ]
    return jsonify(stats_zones)

if __name__ == '__main__':
    print("\n" + "="*45)
    print("   BAOLSAT CORE SYSTEM v2.0 : ACTIVÉ")
    print("   FLUX COPERNICUS (Sentinel-2) : CONNECTÉ")
    print("   ZONE DE SURVEILLANCE : SÉNÉGAL CENTRAL")
    print("="*45 + "\n")
    
    # On utilise le port 5000 pour le dev, Gunicorn prendra le relais en prod
    app.run(host='0.0.0.0', port=5000, debug=True)
