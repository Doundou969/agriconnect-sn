# 🛰️ AgriConnect Sénégal
**Plateforme d'Agriculture de Précision basée sur les données Copernicus**

AgriConnect remplace officiellement SunuBlueTech pour se concentrer sur la souveraineté alimentaire au Sénégal. Nous utilisons l'imagerie satellite pour surveiller la santé des cultures en temps réel.

## 🌍 Notre Mission
Transformer l'agriculture dans la Vallée du Fleuve Sénégal (Richard-Toll, Podor, Matam) et le Bassin Arachidier en fournissant aux agriculteurs des alertes précises sur :
* **La Vigueur des plantes (NDVI)**
* **Le Stress hydrique (Besoins en eau)**
* **L'optimisation des engrais**

## 🚀 Technologie
Nous exploitons la constellation de satellites **Sentinel-2** du programme européen **Copernicus** via l'API Google Earth Engine.



## 📂 Structure du Projet
* `/backend` : Serveur Flask/FastAPI gérant l'application mobile.
* `/satellite_engine` : Algorithmes de traitement d'images Copernicus (Ancien moteur PecheurConnect adapté).
* `/mobile_app` : Interface utilisateur pour les producteurs.

## 🛠️ Installation
```bash
git clone [https://github.com/Doundou969/agriconnect-sn.git](https://github.com/Doundou969/agriconnect-sn.git)
cd backend
pip install -r requirements.txt
python app.py
