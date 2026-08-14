@echo off

cd /d "%~dp0"

echo ========================================
echo       SALES ETL PIPELINE
echo ========================================
echo.
echo Pressione Enter para iniciar o pipeline...
pause > nul

echo.
echo Executando pipeline...
echo.

python scripts\main.py

echo.
echo ========================================
echo       PIPELINE FINALIZADO
echo ========================================
echo.
echo Pressione Enter para fechar...
pause > nul