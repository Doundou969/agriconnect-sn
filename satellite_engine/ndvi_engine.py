import ee

# 1. Connexion sécurisée à Google Earth Engine
try:
    ee.Initialize()
except Exception:
    print("Authentification requise. Tapez 'python -c \"import ee; ee.Authenticate()\"' dans votre terminal.")

def analyser_parcelle_riz(lon, lat):
    point = ee.Geometry.Point([lon, lat])
    zone_etude = point.buffer(1000)

    # Récupération image Sentinel-2 (Copernicus)
    image = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
             .filterBounds(zone_etude)
             .filterDate('2025-01-01', '2026-02-05')
             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))
             .sort('system:time_start', False)
             .first())

    if not image:
        return "Aucune image claire trouvée."

    # Calcul NDVI
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    stats = ndvi.reduceRegion(reducer=ee.Reducer.mean(), geometry=zone_etude, scale=10).getInfo()
    score = stats['NDVI']
    
    if score > 0.6:
        etat = "🟢 Riz en excellente santé"
    elif score > 0.3:
        etat = "🟡 Vigilance requise"
    else:
        etat = "🔴 Alerte : Stress détecté !"

    return f"Score : {score:.2f} -> {etat}"

if __name__ == "__main__":
    print("--- DIAGNOSTIC SATELLITE AGRICONNECT ---")
    # Test sur Richard-Toll
    print(analyser_parcelle_riz(-16.44, 16.46))