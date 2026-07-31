@echo off
title BUILD GAME
setlocal

cd /d "%~dp0"

REM --- PASSO 0: VERIFICA PYTHON ---
where python >nul 2>nul
if errorlevel 1 (
    echo ERRO: Python nao encontrado no PATH.
    echo Instale Python marcando "Add to PATH".
    pause
    exit /b 1
)

REM --- PASSO 0.5: INSTALA PIP SE PRECISAR ---
python -c "import PyInstaller" >nul 2>nul
if errorlevel 1 (
    echo Instalando PyInstaller e dependencias...
    python -m pip install --upgrade pip
    python -m pip install pyinstaller pymongo certifi
)

REM --- PASSO 1: LIMPA ---
echo [1/5] Limpando...
if exist build rmdir /s /q build
if exist dist\Rodolfo.exe del /q dist\Rodolfo.exe
if exist dist\LIFE-GAME.exe del /q dist\LIFE-GAME.exe

REM --- PASSO 2: BUILDA RODOLFO ---
echo [2/5] Buildando Rodolfo.exe...
python -m PyInstaller --clean Rodolfo.spec
if errorlevel 1 (
    echo ERRO no Rodolfo.exe
    pause
    exit /b 2
)
echo OK: Rodolfo.exe

REM --- PASSO 3: COPIA MODELO E LLAMA ---
echo [3/5] Copiando modelo e llama.cpp para dist\...

if not exist "gemma-2-2b-it-Q4_K_M.gguf" (
    echo ERRO: gemma-2-2b-it-Q4_K_M.gguf nao encontrado na pasta raiz.
    pause
    exit /b 4
)
copy /Y "gemma-2-2b-it-Q4_K_M.gguf" "dist\gemma-2-2b-it-Q4_K_M.gguf" >nul
echo OK: modelo copiado.

if not exist "llama-b9637-bin-win-cpu-x64\" (
    echo ERRO: pasta llama-b9637-bin-win-cpu-x64 nao encontrada.
    pause
    exit /b 5
)
if exist "dist\llama-b9637-bin-win-cpu-x64" rmdir /s /q "dist\llama-b9637-bin-win-cpu-x64"
xcopy "llama-b9637-bin-win-cpu-x64" "dist\llama-b9637-bin-win-cpu-x64\" /E /I /H /Y >nul
echo OK: llama.cpp copiado.

REM --- PASSO 4: BUILDA LIFE-GAME ---
echo [4/5] Buildando LIFE-GAME.exe...
python -m PyInstaller --clean LIFE-GAME.spec
if errorlevel 1 (
    echo ERRO no LIFE-GAME.exe
    pause
    exit /b 3
)
echo OK: LIFE-GAME.exe

REM --- PASSO 5: RESUMO ---
echo.
echo [5/5] CONCLUIDO. Arquivos na pasta dist\:
dir /b dist\*.exe
echo.

if exist dist\gemma-2-2b-it-Q4_K_M.gguf (echo [OK] modelo GGUF na pasta dist\) else (echo [FALTA] modelo GGUF)
if exist dist\llama-b9637-bin-win-cpu-x64\llama-server.exe (echo [OK] llama-server.exe na pasta dist\) else (echo [FALTA] llama-server.exe)

echo.
echo Pronto. Copie a pasta DIST inteira para rodar em outro PC.
pause
endlocal
