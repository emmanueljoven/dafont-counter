@echo off
cd /d %~dp0

call C:\ProgramData\miniconda3\Scripts\activate.bat base

echo Lanzando visor de graficos...
streamlit run visor_graficos.py

pause