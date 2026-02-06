from app import app
from waitress import serve
import logging

# Configuration des logs pour surveiller les accès à Dakar
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('waitress')

if __name__ == "__main__":
    print("\n" + "═"*45)
    print(" 🛰️  BAOLSAT PRODUCTION SERVER ACTIVATED")
    print(" 🌍 Zone : Sénégal (Bassin Arachidier)")
    print(" 📡 Port : 8000 | Host : 0.0.0.0")
    print(" 🔌 Status : Connected to Copernicus")
    print("═"*45 + "\n")

    # Serveur multi-threadé robuste
    serve(app, host='0.0.0.0', port=8000, threads=6)
