@echo off
title BAOLSAT CORE SYSTEM - PRODUCTION
cd /d "C:\Users\PC\baolsat-core"

:: Activation de l'environnement virtuel
call venv\Scripts\activate

:: Définition des secrets (remplace par tes vraies clés)
set COPERNICUS_USERNAME=ton_user
set COPERNICUS_PASSWORD=ton_pass
set TG_TOKEN=ton_token
set TG_ID=ton_chat_id

echo Lancement de BAOLSAT sur le port 8000...
python wsgi.py
pause