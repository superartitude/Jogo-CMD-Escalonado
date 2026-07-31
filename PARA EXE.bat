@echo off
chcp 65001 >nul
title BUILD - A ARTE DO CAPITALISMO + RODOLFO
setlocal

:: ============================================================
::  BUILD AUTOMÁTICO - LIFE-GAME.exe + RODOLFO.exe
::  Clique duplo neste .bat ou execute no CMD.
::
::  ATUALIZAÇÃO 2026-07-31 (Foco em compatibilidade TOTAL):
::  → NÃO empacota mais modelo GGUF de 1.5GB DENTRO do Rodolfo.exe
::  → Modelo e llama.cpp ficam NA MESMA PASTA do EXE (abre + rápido)
::  → Ignora gui.py temporariamente (foco 100% CMD)
:: ============================================================

cls
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║  💰 BUILD - A ARTE DO CAPITALISMO + RODOLFO    ║
echo  ║     (Modo COMPATIBILIDADE TOTAL - sem Ollama)  ║
echo  ╚══════════════════════════════════════════════════╝
echo.

:: Garante que está na pasta do script (.bat)
cd /d "%~dp0"
echo  [+] Pasta de trabalho: %CD%
echo.

:: Verifica se tem python
where python >nul 2>nul
if errorlevel 1 (
    echo  [ERRO] Python nao encontrado no PATH!
    echo         Instale Python (marque "Add to PATH" na instalacao).
    pause
    exit /b 1
)

:: Verifica se tem PyInstaller (se nao, instala automaticamente)
python -c "import PyInstaller" >nul 2>nul
if errorlevel 1 (
    echo  [!] PyInstaller nao detectado. Instalando agora...
    python -m pip install --upgrade pip
    python -m pip install pyinstaller pymongo certifi
    echo  [OK] PyInstaller + dependencias instalados.
    echo.
)

:: ============================================================
::  PASSO 1: LIMPEZA (apaga builds antigos, MANTEM os .spec!)
:: ============================================================
echo  [1/5] Limpando builds antigos (build/, dist/*.exe)...
if exist build rmdir /s /q build
if exist dist\LIFE-GAME.exe     del /q dist\LIFE-GAME.exe
if exist dist\Rodolfo.exe       del /q dist\Rodolfo.exe
if exist dist\rodolfo_erro_ia.log del /q dist\rodolfo_erro_ia.log
echo        Concluido.
echo.

:: ============================================================
::  PASSO 2: RODOLFO.EXE  (assistente IA, SEM modelo dentro)
::  Usa Rodolfo.spec — edite o .spec se quiser mudar algo no build
:: ============================================================
if not exist "Rodolfo.spec" (
    echo  [ERRO] Arquivo 'Rodolfo.spec' nao encontrado na pasta raiz!
    echo         Ele e obrigatorio e veio junto com o projeto.
    pause
    exit /b 2
)
echo  [2/5] Compilando RODOLFO.EXE usando Rodolfo.spec...
echo        (Modelo e llama.cpp NAO vao dentro do EXE — serao copiados depois)
echo.
python -m PyInstaller --clean Rodolfo.spec

if errorlevel 1 (
    echo.
    echo  [ERRO] Falha ao gerar Rodolfo.exe! Veja o log acima.
    pause
    exit /b 2
)
echo.
echo  [OK] RODOLFO.EXE gerado!
echo.

:: ============================================================
::  PASSO 3: COPIA MODELO GGUF + LLAMA.CPP PARA A PASTA DIST
:: ============================================================
echo  [3/5] Copiando modelo da IA e motor llama.cpp para pasta dist\...
echo        (1.5GB + DLLs — demora um pouco no HD, rapido no SSD)
echo.

:: Copia o modelo Gemma (obrigatorio)
if exist "gemma-2-2b-it-Q4_K_M.gguf" (
    copy /Y "gemma-2-2b-it-Q4_K_M.gguf" "dist\gemma-2-2b-it-Q4_K_M.gguf" >nul
    echo        [OK] gemma-2-2b-it-Q4_K_M.gguf copiado.
) else (
    echo        [ERRO] Arquivo 'gemma-2-2b-it-Q4_K_M.gguf' NAO ENCONTRADO na pasta raiz!
    echo               Baixe o modelo ou cole ele aqui antes de buildar.
    pause
    exit /b 4
)

:: Copia a pasta COMPLETA do llama.cpp (DLLs + llama-server.exe — obrigatorio)
if exist "llama-b9637-bin-win-cpu-x64\" (
    if exist "dist\llama-b9637-bin-win-cpu-x64" rmdir /s /q "dist\llama-b9637-bin-win-cpu-x64"
    xcopy "llama-b9637-bin-win-cpu-x64" "dist\llama-b9637-bin-win-cpu-x64\" /E /I /H /Y >nul
    echo        [OK] Pasta llama-b9637-bin-win-cpu-x64 copiada (todas as DLLs + motor).
) else (
    echo        [ERRO] Pasta 'llama-b9637-bin-win-cpu-x64' NAO ENCONTRADA na pasta raiz!
    echo               Ela vem junto com o projeto e é obrigatoria.
    pause
    exit /b 5
)
echo.

:: ============================================================
::  PASSO 4: LIFE-GAME.EXE  (jogo principal CMD)
::  Usa LIFE-GAME.spec — edite o .spec se quiser mudar algo no build
:: ============================================================
if not exist "LIFE-GAME.spec" (
    echo  [ERRO] Arquivo 'LIFE-GAME.spec' nao encontrado na pasta raiz!
    echo         Ele e obrigatorio e veio junto com o projeto.
    pause
    exit /b 3
)
echo  [4/5] Compilando LIFE-GAME.EXE usando LIFE-GAME.spec...
python -m PyInstaller --clean LIFE-GAME.spec

if errorlevel 1 (
    echo.
    echo  [ERRO] Falha ao gerar LIFE-GAME.exe! Veja o log acima.
    pause
    exit /b 3
)
echo  [OK] LIFE-GAME.EXE gerado!
echo.

:: ============================================================
::  PASSO 5: RESUMO + VALIDAÇÃO
:: ============================================================
echo  [5/5] Validando arquivos finais na pasta dist\...
echo.

:: Lista tudo que tem em dist\ para o usuário conferir
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                    📂 PASTA FINAL: dist\                     ║
echo  ╠══════════════════════════════════════════════════════════════╣
echo  ║  EXEs:                                                       ║
for %%f in (dist\*.exe) do (
    echo  ║    ✅ %%~nxf
)
echo  ║                                                              ║
echo  ║  Modelo da IA:                                               ║
if exist dist\gemma-2-2b-it-Q4_K_M.gguf (
    echo  ║    ✅ gemma-2-2b-it-Q4_K_M.gguf  (1.5GB - obrigatorio)
) else (
    echo  ║    ❌ FALTANDO gemma-2-2b-it-Q4_K_M.gguf
)
echo  ║                                                              ║
echo  ║  Motor llama.cpp (roda SEM Ollama):                          ║
if exist dist\llama-b9637-bin-win-cpu-x64\llama-server.exe (
    echo  ║    ✅ pasta llama-b9637-bin-win-cpu-x64\  (DLLs + motor)
) else (
    echo  ║    ❌ FALTANDO llama-b9637-bin-win-cpu-x64\
)
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo  🎯 DISTRIBUIÇÃO:
echo     Para rodar o jogo em OUTRO PC, basta copiar a PASTA DIST INTEIRA.
echo     NÃO precisa instalar nada. NÃO precisa de Python. NÃO precisa de Ollama.
echo     Basta dar 2 cliques no LIFE-GAME.exe e o Rodolfo abre automaticamente.
echo.
echo  💡 Requisitos minimos do PC alvo:
echo     → Windows 7/8/10/11 de 64 bits
echo     → 4GB de RAM no minimo (ideal 6GB+)
echo     → Qualquer CPU Intel/AMD de 2012 ou mais novo
echo.
pause
endlocal