# Jogo-CMD-Escalonado
Projeot feito para treino pessoal e diversão entre amigos!

# 💰 A ARTE DO CAPITALISMO

> *"Se o mundo é cheio de gente preguiçosa, resolver problemas bobos é uma mina de ouro."*

Simulador de vida econômica em terminal Python com um **mentor financeiro de IA LOCAL** (não precisa de Ollama, nem de internet, nem de chave de API — zero instalações extras).

Comece **devendo R$1.400**, trabalhe, invista e chegue até **R$ 10 BILHÕES** para comprar o **Globo Terrestre** e zerar o jogo.

---

## ✨ Principais características

- **4 níveis de emprego** com licenças desbloqueáveis
- **7 minigames** liberados conforme você compra itens na loja
- **Bolsa de commodities AO VIVO** com eventos mundiais aleatórios
- **Mineração de criptomoedas** com rig de placas de vídeo
- **Imposto progressivo** + **juros compostos no banco**
- **Ranking global em nuvem** (MongoDB) — TOP 10 jogadores
- **O Rodolfo** 🧓: mentor financeiro de IA LOCAL que abre em janela separada, lê seu save em tempo real, monitora a bolsa e te dá conselhos com personalidade de velho ranzinza sarcástico
- Várias formas de ganhar dinheiro — descubra quais valem mais a pena 😉

---

## 🤖 Sobre o Rodolfo (a IA)

Rodolfo Cavalcanti é um modelo **Gemma 2 2B** rodando 100% local via `llama.cpp`. Ele:
- Não precisa de Ollama
- Não precisa de internet
- Não precisa de instalação nenhuma no PC do usuário
- Abre automaticamente ao lado do jogo (PowerShell posiciona as janelas)
- Diferentes conselhos baseados no seu dinheiro atual, itens, dívidas e ranking

---

## 💻 Requisitos

| Item | Mínimo |
|------|--------|
| SO | Windows 7 SP1 / 8 / 10 / 11 **64-bit** |
| RAM | **4 GB** (recomendado 6 GB+) |
| CPU | Intel/AMD 2012+ (com SSE4.2) |
| Armazenamento | ~2 GB livres (modelo GGUF + DLLs) |
| GPU | Não precisa (100% CPU) |

---

## 🚀 Como jogar

### EXE pronto (não precisa instalar nada)
1. Baixe a pasta **COMPLETA** `dist/` (não é só o .exe!)
2. Confira se tem isso tudo DENTRO da mesma pasta:
   ```
   ├── LIFE-GAME.exe
   ├── Rodolfo.exe
   ├── gemma-2-2b-it-Q4_K_M.gguf    ← NÃO APAGUE
   └── llama-b9637-bin-win-cpu-x64/ ← NÃO APAGUE ESSA PASTA
   ```
3. **2 cliques no `LIFE-GAME.exe`** → seja feliz.

---

## 🛠️ Buildar do zero (Desenvolvedor)

Pré-requisitos: Python 3.11+ instalado e com **PATH** configurado.

```cmd
:: 2 cliques no build automático
PARA EXE.bat
```

Ou se preferir manual:
```cmd
pyinstaller --clean Rodolfo.spec
copy gemma-2-2b-it-Q4_K_M.gguf dist\
xcopy llama-b9637-bin-win-cpu-x64 dist\llama-b9637-bin-win-cpu-x64\ /E /I /H /Y
pyinstaller --clean LIFE-GAME.spec
```

---

## 📁 Estrutura do código

| Arquivo | O que faz |
|---------|-----------|
| `desafio.py` | Jogo principal em terminal (toda a lógica) |
| `co-pilot.py` | Rodolfo, a IA mentor (integração c/ llama.cpp) |
| `shared.py` | Código compartilhado: saves em base64 + ranking MongoDB |
| `Rodolfo.spec` / `LIFE-GAME.spec` | Configs do PyInstaller |
| `PARA EXE.bat` | Build automático de tudo |

---

## 🧠 Dica inicial

Pague a dívida inicial **o mais rápido que conseguir**. Enquanto seu saldo no banco for negativo, os juros compostos não trabalham a seu favor. Depois disso... é só exploração. 🤑

> *"Tentou seguir a vida que todos DIZIAM ser a chave para o sucesso. E olha você agora..."*
>
> — Intro do jogo

### 📐 Arquitetura do Rodolfo (Como funciona SEM Ollama)
