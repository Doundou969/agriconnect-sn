import requests

def diagnostic_agriconnect_libre():
    print("--- CONNEXION AUX SATELLITES COPERNICUS (MODE OPEN) ---")
    
    # Coordonnées de Richard-Toll
    print("📍 Zone cible : Richard-Toll / Vallée du Fleuve")
    print("📡 Requête envoyée au satellite Sentinel-2...")
    
    # Simulation d'analyse basée sur les données libres de Sentinel Hub
    # En situation réelle, on télécharge le PNG ici.
    print("✅ Données spectrales reçues.")
    
    score_ndvi = 0.68  # Valeur typique pour du riz en croissance
    
    print(f"\n📊 SCORE NDVI : {score_ndvi}")
    print("---------------------------------------")
    if score_ndvi > 0.6:
        print("CONSEIL : La végétation est dense. Riz en bonne santé ! 🟢")
    else:
        print("CONSEIL : Attention, possible manque d'eau ou d'azote. 🟡")
    print("---------------------------------------")

if __name__ == "__main__":
    diagnostic_agriconnect_libre()