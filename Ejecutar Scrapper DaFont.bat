@echo off
cd /d %~dp0

echo ============================
echo  SCRAPER DAFONT INICIADO
echo ============================

call C:\ProgramData\miniconda3\Scripts\activate.bat base

python main.py

echo ============================
echo  SCRAPER FINALIZADO
echo ============================

pause