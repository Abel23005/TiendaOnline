@echo off
echo ========================================
echo    SISTEMA ECOMMERCE DJANGO - INICIO
echo ========================================
echo.

echo [1/5] Instalando dependencias...
pip install -r requirements.txt

echo.
echo [2/5] Creando migraciones...
python manage.py makemigrations

echo.
echo [3/5] Aplicando migraciones...
python manage.py migrate

echo.
echo [4/5] Poblando base de datos...
python manage.py poblar_datos

echo.
echo [5/5] Iniciando servidor...
echo.
echo ========================================
echo   SERVIDOR INICIADO EN: http://localhost:8000
echo   ADMIN PANEL: http://localhost:8000/admin
echo   API: http://localhost:8000/api/
echo ========================================
echo.
python manage.py runserver
