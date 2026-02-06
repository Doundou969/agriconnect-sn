from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

# Configuration pour s'assurer que Flask trouve les bons dossiers
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def home():
    """
    Page d'accueil de PecheurConnect avec le diagnostic satellite
    """
    # Ces données simulent le retour de votre script satellite_engine/ndvi_open.py
    # À l'avenir, nous pourrons automatiser la lecture du fichier data.json
    sat_data = {
        'projet': "PecheurConnect - Agri",
        'zone': "Richard-Toll, Vallée du Fleuve",
        'score_ndvi': 0.68,
        'etat': "🟢 Santé Excellente",
        'recommandation': "La densité de chlorophylle est optimale. Pas d'épandage d'urée nécessaire cette semaine.",
        'derniere_maj': "06 Février 2026"
    }
    
    return render_template('index.html', data=sat_data)

@app.route('/api/status')
def api_status():
    """
    Route API pour permettre à d'autres services de lire vos données satellite
    """
    return jsonify({
        "status": "online",
        "connection": "Copernicus Sentinel-2 Active",
        "current_score": 0.68
    })

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    # On récupère le port défini par le serveur (pour le déploiement)
    # Si on est en local, on utilise le port 5000
    port = int(os.environ.get("PORT", 5000))
    
    print(f"--- Lancement de PecheurConnect sur le port {port} ---")
    app.run(host='0.0.0.0', port=port, debug=True)
