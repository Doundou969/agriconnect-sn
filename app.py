from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Simulation de données Copernicus & BaolSat
    data = {
        "status": "OPÉRATIONNEL",
        "station": "BaolSat-Diourbel-01",
        "satellite": "Eutelsat Konnect (Ka-Band)",
        "last_copernicus_sync": datetime.datetime.now().strftime("%H:%M:%S"),
        "signal_strength": "92%",
        "active_terminals": 147,
        "region": "Bassin Arachidier / Baol"
    }
    return render_template('index.html', data=data)

if __name__ == '__main__':
    print("-------------------------------------------")
    print("   BAOLSAT CORE SYSTEM : ACTIVÉ")
    print("   FLUX COPERNICUS : CONNECTÉ")
    print("-------------------------------------------")
    app.run(host='0.0.0.0', port=5000, debug=True)
