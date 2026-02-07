import os, datetime, sqlite3, random
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DATABASE'] = 'baolsat.db'

# --- INITIALISATION DE LA BASE ---
def init_db():
    if not os.path.exists(app.config['UPLOAD_FOLDER']): 
        os.makedirs(app.config['UPLOAD_FOLDER'])
    with sqlite3.connect(app.config['DATABASE']) as conn:
        # Table Chat
        conn.execute('''CREATE TABLE IF NOT EXISTS chat 
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        user TEXT, text TEXT, photo TEXT, time TEXT, is_critical INTEGER DEFAULT 0)''')
        # Table Bourse (Prix du jour)
        conn.execute('''CREATE TABLE IF NOT EXISTS bourse 
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        produit TEXT, prix INTEGER, tendance TEXT, unite TEXT)''')
        
        # Insertion des prix par défaut si vide
        check = conn.execute("SELECT count(*) FROM bourse").fetchone()[0]
        if check == 0:
            prix_init = [
                ('Arachide', 325, 'up', 'kg'),
                ('Riz (Padie)', 190, 'stable', 'kg'),
                ('Oignon local', 450, 'down', 'kg'),
                ('Anacarde', 425, 'up', 'kg')
            ]
            conn.executemany("INSERT INTO bourse (produit, prix, tendance, unite) VALUES (?,?,?,?)", prix_init)

# --- LOGIQUE AGRONOMIQUE & SENTINEL-2 ---
def get_agronomic_data():
    # Ici on fusionne tes zones avec les données de télédétection
    data = [
        {"zone": "Bassin Arachidier", "culture": "Arachide", "temp": 35, "ndvi": 0.71, "coords": [14.65, -16.15], "coef": 2.0},
        {"zone": "Vallée du Fleuve", "culture": "Riz", "temp": 32, "ndvi": 0.85, "coords": [16.03, -16.50], "coef": 7.0},
        {"zone": "Niayes", "culture": "Oignon", "temp": 28, "ndvi": 0.82, "coords": [15.00, -17.00], "coef": 30.0},
        {"zone": "Casamance", "culture": "Anacarde", "temp": 30, "ndvi": 0.88, "coords": [12.58, -16.27], "coef": 1.5},
        {"zone": "Sénégal Oriental", "culture": "Coton", "temp": 38, "ndvi": 0.45, "coords": [13.77, -13.66], "coef": 1.8}
    ]
    for item in data:
        item["rendement"] = round(1000 * (item["ndvi"] * item["coef"]), 1) # Simulation simple
        item["alerte_bio"] = "⚠️ RISQUE MOUCHE" if (item["zone"] == "Niayes" and item["temp"] > 25) else "STABLE"
    return data

# --- ROUTES ---
@app.route('/')
def home():
    agri_data = get_agronomic_data()
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.row_factory = sqlite3.Row
        msgs = conn.execute("SELECT * FROM chat ORDER BY id DESC LIMIT 15").fetchall()
        prices = conn.execute("SELECT * FROM bourse").fetchall()
    
    return render_template('index.html', data={
        "status": "OPÉRATIONNEL",
        "station": "BaolSat-Diourbel-01",
        "agri_data": agri_data, 
        "prices": prices,
        "messages": msgs, 
        "now": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    })

@app.route('/api/agro_thermal')
def agro_thermal():
    # Route API pour tes graphiques JS
    return jsonify(get_agronomic_data())

@app.route('/send_message', methods=['POST'])
def send_message():
    user = request.form.get('user', 'Agriculteur')
    text = request.form.get('text', '')
    file = request.files.get('photo')
    filename = None
    if file and file.filename != '':
        filename = secure_filename(f"{datetime.datetime.now().strftime('%H%M%S')}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.execute("INSERT INTO chat (user, text, photo, time, is_critical) VALUES (?,?,?,?,0)",
                    (user, text, filename, datetime.datetime.now().strftime("%H:%M")))
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    print("\n" + "="*45)
    print("   BAOLSAT CORE SYSTEM v2.0 : PRÊT")
    print("="*45 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)