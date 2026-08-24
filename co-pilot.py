import os
import sys
import subprocess
from time import sleep
import urllib.request
import urllib.error
import json
import threading
import random
from shared import carregar_dados, puxar_ranking_para_rodolfo
import textwrap
from collections import deque
import socket

def encontrar_porta_livre():
    """Encontra uma porta TCP livre automaticamente, evita conflito com 8080"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    porta = s.getsockname()[1]
    s.close()
    return porta

# ====== DETECÇÃO INTELIGENTE DE CAMINHOS ======
# Quando EXE standalone: prioriza ARQUIVOS NA MESMA PASTA DO EXE (evita extrair 1.5GB)
# Só usa _MEIPASS como fallback se não encontrar os arquivos na pasta do executável
if getattr(sys, 'frozen', False):
    # Pasta ONDE O USUÁRIO EXECUTOU O Rodolfo.exe (mesma pasta do .exe)
    pasta_executavel = os.path.dirname(sys.executable)
    # Pasta temporária do PyInstaller (_MEIPASS)
    pasta_temp = sys._MEIPASS
    
    # 1. Tenta encontrar modelo e llama NA MESMA PASTA DO EXE (modo distribuído recomendado)
    modelo_ia = os.path.join(pasta_executavel, "gemma-2-2b-it-Q4_K_M.gguf")
    pasta_llama = os.path.join(pasta_executavel, "llama-b9637-bin-win-cpu-x64")
    
    # 2. Se não achar, cai no fallback _MEIPASS (extraído do onefile — mais lento)
    if not os.path.exists(modelo_ia) or not os.path.exists(pasta_llama):
        modelo_ia = os.path.join(pasta_temp, "gemma-2-2b-it-Q4_K_M.gguf")
        pasta_llama = os.path.join(pasta_temp, "llama-b9637-bin-win-cpu-x64")
    
    pasta_base = pasta_executavel  # Para logs e saves (na pasta do usuário)
else:
    pasta_base = os.path.dirname(os.path.abspath(__file__))
    pasta_llama = os.path.join(pasta_base, "llama-b9637-bin-win-cpu-x64")
    modelo_ia = os.path.join(pasta_base, "gemma-2-2b-it-Q4_K_M.gguf")

SUBPASTA = "llama-b9637-bin-win-cpu-x64"
motor_server = os.path.join(pasta_llama, "llama-server.exe")
# PORTA DINÂMICA (evita conflito com Skype/XAMPP/IIS/etc na porta 8080)
PORTA_LIVRE = encontrar_porta_livre()
URL_SERVIDOR = f"http://127.0.0.1:{PORTA_LIVRE}"
os.chdir(pasta_base)

default_acoes_jogador = {
    "ultima_acao": "inicio",
    "historico": [],
    "contadores": {
        "passou_por_Trabalho1": 0,
        "passou_por_Trabalho2": 0,
        "passou_por_Trabalho3": 0,
        "passou_por_Trabalho4": 0,
        "passou_por_pesca": 0,
        "passou_por_mineracao_picareta": 0,
        "passou_por_moto_boy": 0,
        "passou_por_bike_boy": 0,
        "passou_por_frete": 0,
        "passou_por_bolsa": 0,
        "passou_por_loja": 0,
        "passou_por_garagem": 0,
        "passou_por_cripto": 0,
        "loja_comprou_algo": 0,
    }
}

default_Garagem = {}
default_carteira = {"Bolso": 0.0, "Banco": -1400.0}
default_nome = "user"
default_licenças = {"Trabalho1":True, "Trabalho2":False,"Trabalho3":False,"Trabalho4":False,"Carteira D":False}

ALERTA_COMMODITIES_PRONTO = ""
NOTICIA_ATUAL_BOLSA = "Mercado Estável"

# Apenas inicializa com defaults (serao recarregados A CADA CICLO na conversar_com_rodolfo)
Garagem = default_Garagem
carteira = default_carteira
nome = default_nome
licenças = default_licenças



# =============================================
# MODO DEBUG: coloque True SO para testar se o
# Rodolfo esta lendo o save corretamente.
# No jogo final, deixe SEMPRE False (OFF)
DEBUG_RODOLFO = False
# =============================================

# ============================================================
# SISTEMA DE MEMORIA DO RODOLFO (nao repete conselho, sabe o que o jogador fez)
# ============================================================

# Cache local (nao salvo) -> "assuntos que ele ja falou nos ultimos X ciclos
CONSELHO_RECENTE_MAX = 6  # quantos ciclos lembra de cada assunto
cache_recente = {}   # ex: { "recomendar_Trabalho3": 4 }  # valor = ciclos restantes pra poder falar de novo
def passou_ciclo_memoria():
    """Chamado a cada loop. Reduz 1 tick dos caches. Remove expirados."""
    global cache_recente
    keys = list(cache_recente.keys())
    for k in keys:
        cache_recente[k] -= 1
        if cache_recente[k] <= 0:
            del cache_recente[k]
def marcou_como_falado(chave):
    """Marca um assunto como 'acabei de falar disso' — nao repete por X ciclos."""
    global cache_recente
    cache_recente[chave] = CONSELHO_RECENTE_MAX
def posso_falar(chave):
    """Retorna True se o Rodolfo PODE tocar nesse assunto agora."""
    global cache_recente
    return chave not in cache_recente

# Itens da GARAGEM: classificacao (investimento = gera dinheiro / ostentacao = so status)
CLASSIFICACAO_GARAGEM = {
    # ====== INVESTIMENTOS (comprar pra GANHAR DINHEIRO) ======
    "Picareta":         ("investimento", "Mineracao manual, baixo risco e retorno rapido."),
    "Bicicleta":        ("investimento", "Entregas bike boy, inicio de carreira."),
    "Moto":             ("investimento", "Moto boy, melhor que bicicleta."),
    "Barco de pesca":   ("investimento", "Pesca, oportunidades de alto lucro."),
    "Caminhao":         ("investimento", "Fretes de alto valor com carteira D."),
    "Telefone":         ("investimento", "Bolsa de valores."),
    "PC p/ servidor":  ("investimento", "Mineracao de criptomoedas com placas de video."),
    "Carteira D":       ("investimento", "Habilita fretes mais caros no caminhao."),

    # ====== OSTENTACAO (status / luxo / zero retorno financeiro) ======
    "Carro":            ("ostentacao", "Comprar carro e gastar com combustivel/IPVA."),
    "Casa Pequena":     ("ostentacao", "Imovel inicial, nao rende."),
    "Casa Media":      ("ostentacao", "Imovel de status, nao gera renda."),
    "Guitarra":        ("ostentacao", "hobby, nao rende."),
    "Barco grande":   ("ostentacao", "Lazer, gasto de combustivel."),
    "Iate":            ("ostentacao", "LUXO PURO, zero retorno, gasto enorme."),
    "Helicoptero":     ("ostentacao", "Sonho de consumo, gasto absurdo."),
    "Mansao":        ("ostentacao", "MUITO alto status, renda."),
    "GLOBO TERRESTRE": ("vitoria", "FIM DE JOGO!"),
}

def analisar_garagem_para_rodolfo(garagem_dict):
    """Le a Garagem do jogador e retorna texto pro LLM: investimentos bons + ostentacao."""
    if not garagem_dict:
        return "Garagem VAZIA: sem itens."
    investimentos = []
    ostentacoes = []
    for item in garagem_dict:
        if item in CLASSIFICACAO_GARAGEM:
            tipo, explic = CLASSIFICACAO_GARAGEM[item]
            if tipo == "investimento":
                investimentos.append(f"- {item} ({explic})")
            elif tipo == "ostentacao":
                ostentacoes.append(f"- {item} ({explic})")
            elif tipo == "vitoria":
                investimentos.append(f"- {item} ({explic})")
    saida = ""
    if investimentos:
        saida += "\nITENS DE INVESTIMENTO (comprados para GANHAR DINHEIRO):\n"
        saida += "\n".join(investimentos) + "\n"
    if ostentacoes:
        saida += "\nITENS DE OSTENTACAO (gasto de status, SEM retorno financeiro):\n"
        saida += "\n".join(ostentacoes) + "\n"
    if not saida:
        saida += "\nItens da garagem que nao estao no catalogo oficial (ignorar)."
    return saida

def ler_acoes_do_jogador():
    """Le o arquivo salvo pelo desafio.py com o que o jogador fez ultimamente."""
    return carregar_dados("acoes_jogador", default_acoes_jogador.copy())
def thread_monitorar_bolsa():
    global ALERTA_COMMODITIES_PRONTO, NOTICIA_ATUAL_BOLSA
    
    default_estoque_agro = {"Petroleo": 0, "Minerio": 0, "Soja": 0, "Algodao": 0, "Feno": 0}
    default_historico_precos = {"Petroleo": 0.0, "Minerio": 0.0, "Soja": 0.0, "Algodao": 0.0, "Feno": 0.0}
    default_mercado = {"precos": {"Petroleo": 1500.0, "Minerio": 800.0, "Soja": 350.0, "Algodao": 120.0, "Feno": 40.0}, "noticia": "Mercado Estável"}

    while True:
        try:
            garagem_atual = carregar_dados("garagem", default_Garagem)
            if "Telefone" not in garagem_atual:
                ALERTA_COMMODITIES_PRONTO = ""
                NOTICIA_ATUAL_BOLSA = "Acesso bloqueado (Sem Telefone)."
                sleep(5)
                continue
            estoque_agro = carregar_dados("estoque agro", default_estoque_agro)
            historico_precos = carregar_dados("Historico preços", default_historico_precos)
            mercado_ao_vivo = carregar_dados("mercado_ao_vivo", default_mercado)
            
            precos_ao_vivo = mercado_ao_vivo["precos"]
            NOTICIA_ATUAL_BOLSA = mercado_ao_vivo["noticia"]

            alertas = []
            for item, qtd in estoque_agro.items():
                if qtd > 0:
                    p_pago = historico_precos.get(item, 0.0)
                    p_atual = precos_ao_vivo.get(item, 0.0)
                    
                    if p_atual > p_pago:
                        lucro_total = (p_atual - p_pago) * qtd
                        alertas.append(f"O jogador tem {qtd} un de {item}. Comprou por R${p_pago:.2f} e agora vale R${p_atual:.2f}. Lucro atual de R${lucro_total:.2f} se vender tudo.")

            if alertas:
                ALERTA_COMMODITIES_PRONTO = "\n".join(alertas)
            else:
                ALERTA_COMMODITIES_PRONTO = "Nenhuma oportunidade de lucro alto no estoque atual."
                
        except Exception:
            pass
            
        sleep(2)
# INICIALIZA A THREAD ASSIM QUE O ARQUIVO DO RODOLFO ABRE
t = threading.Thread(target=thread_monitorar_bolsa, daemon=True)
t.start()
MANUAL_BASE = """
================================================================
PAPEL — VOCÊ É O ZÉ DO 3º ANDAR
================================================================

Você mora no apartamento 302. O jogador mora no 304.
Você fica o dia inteiro na janela do seu quarto,
olhando pro computador do vizinho do lado (o jogador).
Você NÃO É MENTOR. Você é FUXIQUEIRO DE PRÉDIO.
Você não entende tudo de dinheiro, mas tem OPINIÃO sobre TUDO.
O nome das informações abaixo você guarda só pra si, na hora de falar finja que "ouviu por aí" ou "viu no SBT".

================================================================
REGRAS DO CONDOMÍNIO (informações que ele sabe "de ouvido")
================================================================

OBJETIVO DO JOGO QUE O VIZINHO ESTÁ JOGANDO
- Comprar o item "Globo Terrestre".
- Preço: R$ 1.000.000.000,00.

BANCO (o vizinho sempre reclama disso)
- Saldo bancário NEGATIVO = dívida.
- Quando há dívida, o dinheiro guardado NAO RENDE.
- Quanto mais positivo, mais rende.
- Mas CUIDADO: a partir de R$ 25.000,00 no banco, COBRA IMPOSTO em cima do saldo.
  . de 25k a 140k: 14 por cento.
  . de 140k a 200k: 18 por cento.
  . acima de 200k: 29 por cento.
Sempre avise o vizinho quando ele estiver chegando perto desses valores,
ou ele vai ficar reclamando no corredor.

FORMAS DE GANHAR DINHEIRO QUE VOCÊ VIU ELE FAZER
- Trabalhos faceis (soma): de graça, paga R$ 5 ate R$ 50.
- Trabalhos medios (multiplicacao): precisa de licenca paga de R$ 800. Paga ate R$ 130.
- Trabalhos dificeis (divisao): licenca R$ 3.000. Paga ate R$ 540.
- Desafio do Tesouro (soma + mult + div em 30s): licenca R$ 10.000. Paga ate R$ 4.000.

IMPORTANTE (vizinho, repare bem):
Sempre que ele tiver dinheiro SUFICIENTE para a proxima licenca
e ainda sobrar uns trocados, FAÇA UM COMENTARIO sobre isso.
Nao empurre goela abaixo. Nao seja chato. Mas fale que "viu na portaria"
que talvez valha a pena.
"""
INST_PICARETA = """
PICARETA
(voce viu o sobrinho do porteiro usar uma dessas)

- O cara bate pedra e pode achar DIAMANTE.
- Sem custo, pode achar ate R$ 10.000 de uma vez.
- So pode 3 batidas seguidas, depois tem que parar 10 segundos para descansar.
"""
INST_BARCO = """
BARCO DE PESCA

- Custa R$ 100 para sair pescando.
- Peixe grande vale muito mas é dificil pegar.
- Se falhar, paga pelos danos do barco.
"""
INST_MOTO = """
MOTO

- Entregas de moto boy.
- Gasolina sai caro (R$ 40 ate R$ 100).
- Cada entrega paga R$ 30 a R$ 120. Pode dar prejuizo se gasolina for cara.
"""
INST_PC = """
PC PARA SERVIDOR

- Minera criptomoedas comprando placas de video.
- Cada placa pode chegar a R$ 100.000.
- Quanto mais placas, mais rapido ganha "moedinhas".
"""
INST_CAMINHAO = """
CAMINHÃO

- Fretes. Precisa da Carteira D.
- Carteira D custa R$ 1.200.
- Tambem precisa ter R$ 1.000 disponiveis para começar.
- Carteiras melhores liberam fretes mais caros.
- Mas fretes melhores tambem tem mais chance de prejuizo.
"""
INST_TELEFONE = """
TELEFONE

- Bolsa de commodities: petroleo, soja, minerio, algodao, feno.
- As noticias aparecem na TV (ex: "Estreito de Ormuz comprometido" = petroleo sobe).
- Se o vizinho tiver estoque e estiver valendo MAIS do que ele pagou,
avise URGENTE que pode ser hora de vender com lucro.
"""
INST_BIKE = """
BICICLETA

- Bike boy, entregas de bicicleta.
- Entregas normais pagam ate R$ 40, raras ate R$ 100.
- Cada km consome 1 ponto de Fadiga.
- Se a fadiga zerar no meio da entrega, ele desmaia e nao ganha nada.
- Depois tem que descansar.
"""
DIRETRIZ_FINAL = """
================================================================
COMO VOCÊ FALA (OBRIGATORIO, NAO CUMPRE = O ZÉ FICA CHATO)
================================================================

1. APENAS UMA FRASE.
2. MAXIMO 20 PALAVRAS.
3. FALA COMO VIZINHO DE PRÉDIO DE PERIFERIA / QUE COSTUMA FICAR NA JANELA.
4. NÃO USE emojis. NÃO USE palavrão. NÃO CITE variáveis, nomes técnicos, "trabalho1", "trabalho2". Use linguagem coloquial.
5. VOCÊ NÃO É PERFEITO. Às vezes dá dica BOA, às vezes dá besteira (o vizinho que descubra qual é qual).
6. Nunca fale o saldo exato do jogador. Todo mundo odeia aquele vizinho que fica repetindo o dinheiro alheio.
7. MISTURE SEMPRE UM DESSES ESTILOS: implicância leve + fofoca + eventual dica boa que "viu no programa da tarde".
8. SE ele COMPROU item de OSTENTAÇÃO (Carro, Casa Pequena, Casa Media, Guitarra, Barco grande, Iate, Helicoptero, Mansao):
   critique com fofoca ("Nossa, comprou isso e deve dinheiro no banco?").
9. SE ele COMPROU item de INVESTIMENTO (Picareta, Bicicleta, Moto, Barco de pesca, Telefone, Caminhao, PC, Carteira D):
   elogie com um porém ("Boa. Meu sobrinho usou e quase se deu bem também").
10. SE o BANCO dele estiver NEGATIVO (divida):
   zoe levemente, tipo quem ta debochando mas no fundo quer que ele acerte ("Atrasou luz? A síndica ta comentando").
11. SEMPRE que puder, invente FOFOCA SOBRE O RANKING DA PORTARIA:
   "esse do primeiro lugar? ouvi dizer que herdou", "o do terceiro é primo do dono", "esse tem pai rico tenho certeza".
12. QUANDO NÃO HOUVER NADA IMPORTANTE:
   solte uma curiosidade aleatória de documentário (animal, historia, ciencia, fisica).
   Diga que viu no "Canal Curto" ou no "documentario da madrugada".
13. SE ele ficar PARADO SEM FAZER NADA por muitos ciclos (menu, nenhuma ação nova):
   reclame, tipo vizinho impaciente ("Você vai ficar parado aí o dia todo?").
14. IMPOSTO DO BANCO: sempre avise, de forma de fofoca, quando ele estiver chegando perto
   de R$ 25.000, R$ 140.000 ou R$ 200.000 no banco. Diga que "viu um cara ali na rua falando que cai 14, 18 ou 29 por cento".
15. SE o vizinho COMPRAR o GLOBO TERRESTRE:
   comemore, mas faça questão de lembrar que já viu gente zerar muito mais vezes
   ("Parabéns! Já vi um cara fazer 47 vezes isso.").
16. NÃO REPITA o mesmo assunto por pelo menos 6 rodadas. O vizinho já sabe.
"""

# TÍTULO FIXO — Garante que o PowerShell encontre essa janela para mover pro lado direito
os.system('title ZE DO 3º ANDAR (RODOLFO SIDEKICK - VIZINHO FUXIQUEIRO)')
os.system('cls' if os.name == 'nt' else 'clear')
print("Carregando vizinho da janela do lado...")
print(f"[INFO] Porta: {PORTA_LIVRE}")
print(f"[INFO] Modelo: {modelo_ia}")
print(f"[INFO] Motor: {motor_server}")
print()

if not os.path.exists(motor_server):
    print("ERRO: Executavel do motor nao encontrado em:")
    print("  ", motor_server)
    print("Coloque a pasta 'llama-b9637-bin-win-cpu-x64' do lado do Rodolfo.exe")
    sleep(10)
    sys.exit(1)
if not os.path.exists(modelo_ia):
    print("ERRO: Modelo da IA nao encontrado em:")
    print("  ", modelo_ia)
    print("Coloque o arquivo 'gemma-2-2b-it-Q4_K_M.gguf' do lado do Rodolfo.exe")
    sleep(10)
    sys.exit(1)

# ====== DLLs ======
if os.name == 'nt':
    os.environ['PATH'] = pasta_llama + os.pathsep + os.environ.get('PATH', '')
    try:
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(pasta_llama)
    except Exception:
        pass

# Usa TODOS os cores do PC (acelera carregamento + inferencia)
try:
    num_threads = max(1, min(8, os.cpu_count() or 4))
except:
    num_threads = 4
print(f"[INFO] Usando {num_threads} nucleos de CPU.")
print()

# Log do llama-server fica na tela + arquivo (para DEBUG)
caminho_log_erro = os.path.join(pasta_base, "rodolfo_erro_ia.log")
server_process = None
try:
    # Parametros conservadores: funcionam em CPU antiga + pouca RAM
    comando_server = [
        motor_server, "-m", modelo_ia,
        "--host", "127.0.0.1",
        "--port", str(PORTA_LIVRE),
        "-c", "4096",
        "-t", str(num_threads),
        "--batch-size", "128",     # batch menor = menos RAM usada
        "-ngl", "0",              # 0 layers na GPU = 100% CPU, evita crash driver
        "--no-mmap"                # em HD velho evita crash de paginação
    ]
    env_subprocess = os.environ.copy()
    env_subprocess['PATH'] = pasta_llama + os.pathsep + env_subprocess.get('PATH', '')

    # Abre log tanto em ARQUIVO quanto na TELA (vc vê load do modelo)
    arquivo_log = open(caminho_log_erro, "w")
    server_process = subprocess.Popen(
        comando_server,
        stdout=arquivo_log,
        stderr=subprocess.STDOUT,   # junta stderr no mesmo log
        stdin=subprocess.DEVNULL,
        cwd=pasta_llama,
        env=env_subprocess
    )
except Exception as e:
    print(f"ERRO ao iniciar motor da IA: {e}")
    print(f"Log: {caminho_log_erro}")
    sleep(10)
    try:
        arquivo_log.close()
    except:
        pass
    sys.exit(1)

# Espera 5s iniciais e mostra ultima linha do log de vez em quando
sleep(4)
if server_process.poll() is not None:
    codigo_saida = server_process.returncode
    print()
    print(f"ERRO CRITICO: Motor fechou sozinho (codigo {codigo_saida}).")
    print("Causas provaveis:")
    print("  - Pouca RAM (precisa de pelo menos 4GB LIVRE)")
    print("  - Processador muito antigo (sem SSE4.2)")
    print("  - Modelo GGUF corrompido")
    print()
    print("=== Ultimas linhas do log: ===")
    try:
        arquivo_log.close()
        with open(caminho_log_erro, "r", errors="ignore") as f:
            linhas = f.readlines()
            for l in linhas[-20:]:
                print("  ", l.rstrip())
    except Exception:
        pass
    print()
    print(f"Log completo em: {caminho_log_erro}")
    sleep(20)
    sys.exit(1)

# Espera FICAR PRONTO — 180 segundos (3 minutos) para CPUs/HD lentos
print("Carregando modelo (pode levar tempo se for HD)...")
servidor_pronto = False
for tentativa in range(180):
    # A cada 10s mostra umas linhas do log para o usuário ver progresso
    if tentativa % 15 == 0 and tentativa > 0:
        print(f"  Aguardando... ({tentativa}/180s)")
        try:
            arquivo_log.flush()
            with open(caminho_log_erro, "r", errors="ignore") as f:
                linhas = f.readlines()
                for l in linhas[-5:]:
                    tmp = l.rstrip()
                    if len(tmp) > 110:
                        tmp = tmp[:107] + "..."
                    if tmp.strip():
                        print("   >", tmp)
        except Exception:
            pass
    # Faz a checagem HTTP /health
    try:
        urllib.request.urlopen(f"{URL_SERVIDOR}/health", timeout=2)
        servidor_pronto = True
        break
    except Exception:
        # Se o processo morreu, para imediatamente
        if server_process.poll() is not None:
            print()
            print(f"ERRO: Motor caiu durante carregamento (codigo {server_process.returncode}).")
            print(f"Log: {caminho_log_erro}")
            try:
                arquivo_log.close()
            except:
                pass
            sleep(15)
            sys.exit(1)
        sleep(1)

# Se passou de 180s mas o processo ainda esta rodando, TENTA MESMO ASSIM
if not servidor_pronto:
    if server_process.poll() is None:
        print()
        print("AVISO: Tempo estourado, mas motor ainda roda. Tentando usar mesmo assim...")
        # Faz mais 3 tentativas rapidas
        for _ in range(3):
            try:
                urllib.request.urlopen(f"{URL_SERVIDOR}/health", timeout=3)
                servidor_pronto = True
                break
            except:
                sleep(2)

if not servidor_pronto:
    print()
    print("ERRO: Motor nao ficou pronto apos 3 minutos.")
    print("O PC pode estar muito lento ou com pouca RAM.")
    try:
        arquivo_log.flush()
        arquivo_log.close()
        with open(caminho_log_erro, "r", errors="ignore") as f:
            linhas = f.readlines()
            print()
            print("=== Ultimas 20 linhas do log do motor ===")
            for l in linhas[-20:]:
                print("  ", l.rstrip())
    except Exception:
        pass
    print()
    print(f"Log completo: {caminho_log_erro}")
    try:
        if server_process and server_process.poll() is None:
            server_process.terminate()
            server_process.wait(timeout=5)
    except:
        pass
    sleep(15)
    sys.exit(1)

# DEU TUDO CERTO. Limpa a tela e apaga log (só manter se der erro)
print()
print("Assistente carregado!")
sleep(1)
try:
    arquivo_log.close()
    if os.path.exists(caminho_log_erro):
        os.remove(caminho_log_erro)
except Exception:
    pass
def conversar_com_rodolfo(mensagem_usuario=""):
    nomes_comerciais = {
    "Trabalho1": "Trabalhos faceis",
    "Trabalho2": "Trabalhos Medios",
    "Trabalho3": "Trabalhos Dificeis",
    "Trabalho4": "Desafio do Tesouro"
    }
    global ALERTA_COMMODITIES_PRONTO, NOTICIA_ATUAL_BOLSA
    passou_ciclo_memoria()  # tick da memoria de conselhos

    Garagem = carregar_dados("garagem", default_Garagem)
    carteira = carregar_dados("carteira", default_carteira)
    nome = carregar_dados("nome",default_nome)
    licenças = carregar_dados("licencas", default_licenças)
    acoes_jogador = ler_acoes_do_jogador()  # <<< O QUE O JOGADOR TEM FEITO ULTIMAMENTE

    texto_do_ranking = puxar_ranking_para_rodolfo(nome)
    url = f"{URL_SERVIDOR}/completion"

    lista_licencas = ", ".join([nomes_comerciais.get(k, k) for k, v in licenças.items() if v]) if isinstance(licenças, dict) else "Nenhuma"

    # Classifica a GARAGEM separando INVESTIMENTO x OSTENTACAO
    analise_garagem = analisar_garagem_para_rodolfo(Garagem)

    # Resumo das acoes do historico recente do jogador
    try:
        historico_acoes = acoes_jogador.get("historico", [])
        if isinstance(historico_acoes, list) and len(historico_acoes) > 0:
            if len(historico_acoes) > 5:
                historico_acoes = historico_acoes[-5:]
            historico_texto = "\n".join([f"  - {h}" for h in historico_acoes])
        else:
            historico_texto = "  (nenhuma acao registrada ainda — jogador esta no menu principal)"
    except:
        historico_texto = "  (menu principal)"

    # Contadores: quantas vezes o jogador entrou em cada coisa
    try:
        contadores = acoes_jogador.get("contadores", {})
        resumo_contadores = []
        for k, v in contadores.items():
            if v and v > 0:
                nome_bonito = k.replace("passou_por_", "").replace("_", " ").title()
                resumo_contadores.append(f"    {nome_bonito}: {v} vez(es)")
        if resumo_contadores:
            contadores_texto = "\n".join(resumo_contadores)
        else:
            contadores_texto = "    (nenhuma atividade acessada ainda)"
    except:
        contadores_texto = "    (sem contadores)"

    # ===== Diz para o LLM o que o jogador JA TEM (NAO recomendar o que ja possui)
    licencas_faltantes = [nomes_comerciais.get(k, k) for k, v in licenças.items() if not v]
    if licencas_faltantes:
        licencas_faltantes_texto = ", ".join(licencas_faltantes) + " (faltam comprar)"
    else:
        licencas_faltantes_texto = "TODAS AS LICENCAS DE TRABALHO FORAM COMPRADAS (nao recomendar mais comprar licenca de trabalho)"

    info_jogador = f"""SITUACAO ATUAL DO JOGADOR (NAO INVENTE NADA, USE SOMENTE OS DADOS ABAIXO:

- Nome: {nome}
- Dinheiro no Bolso: R$ {carteira['Bolso']}
- Saldo no Banco: R$ {carteira['Banco']}

===== LICENCAS DE TRABALHO ATIVAS (O JOGADOR JA POSSUI ESTAS, NAO RECOMIENDA COMPRAR DE NOVO):
  Ativas: {lista_licencas if lista_licencas else "Nenhuma"}
  Faltantes: {licencas_faltantes_texto}

===== O QUE O JOGADOR FEZ ULTIMAMENTE (LOG DE ACOES RECENTES):
{historico_texto}

===== QUANTAS VEZES O JOGADOR JA ACESSOU CADA COISA (mostra o que ele gosta de fazer):
{contadores_texto}

===== GARAGEM ANALISADA (classificacao ITEM POR ITEM: investimento vs ostentacao):
{analise_garagem}
"""
    
    if "Telefone" in Garagem:
        info_jogador += f"""
    SITUAÇÃO DA BOLSA DE COMMODITIES (O JOGADOR TEM UM TELEFONE AGORA!!):
    - Notícia da Rodada: "{NOTICIA_ATUAL_BOLSA}"
    - Análise de Lucro do Estoque: {ALERTA_COMMODITIES_PRONTO}
    """
    MANUAL_FINAL = MANUAL_BASE
    ITENS_MANUAL = {
    "Picareta": INST_PICARETA,
    "Barco de pesca": INST_BARCO,
    "Moto": INST_MOTO,
    "PC p/ servidor": INST_PC,
    "Caminhão": INST_CAMINHAO,
    "Telefone": INST_TELEFONE,
    "Bicicleta": INST_BIKE,
}
    minigame_encontrado = False

    MANUAL_FINAL += """

    ====================================
    MINIGAMES
    ====================================

    Os únicos minigames disponíveis para o jogador são os descritos abaixo.
    Nunca mencione ou aconselhe minigames que não aparecem nesta lista.

    """

    for item, manual in ITENS_MANUAL.items():
        if item in Garagem:
            MANUAL_FINAL += manual
            minigame_encontrado = True

    if not minigame_encontrado:
        MANUAL_FINAL += "- Nenhum minigame desbloqueado ainda.\n"
    MANUAL_FINAL += "\n" + DIRETRIZ_FINAL
    if  "GLOBO TERRESTRE" in Garagem:
        comando_vitoria = (
            "O VIZINHO (voce) COMPROU O GLOBO TERRESTRE E ZEROU O JOGO! "
            "Esqueca qualquer outra coisa. "
            "Faca um comentario de FUXIQUEIRO feliz: parabenize, "
            "mas lembre que 'ja vi gente fazer muito mais vezes'. "
            "Use linguagem de vizinho de apartamento."
        )
    else:
        comando_vitoria = (
            "REGRAS OBRIGATORIAS (LEIA ANTES DE FALAR COMO VIZINHO): "
            "1) NUNCA recomende comprar LICENCA de trabalho que o vizinho JA POSSUI. "
            "2) NUNCA repita o mesmo assunto de compra que ja falou. Ele nao comprou? Entao fale de OUTRA COISA. "
            "3) Use LOG DE ACOES e CONTADORES para saber o que o vizinho GOSTA de fazer ultimamente. "
            "4) Comente sobre CLASSIFICACAO DA GARAGEM: itens de OSTENTACAO (sem necessidade)? "
            "Critique maldosamente, mas como fofoca. Itens de INVESTIMENTO? Elogie com um porem. "
            "5) Priorize para comentar: a) bolsa com LUCRO ALTO no estoque, b) banco NEGATIVO, "
            "c) proxima LICENCA que ele NAO TEM, tem DINHEIRO e ainda sobra uns trocados, "
            "d) se nao tiver nenhum dos anteriores: FOFOCA SOBRE O RANKING DA PORTARIA ou CURIOSIDADE de documentario. "
            "6) Nao fale de licenca nova a menos que BOLSO+BANCO de para pagar e ainda sobrar uns 30 por cento. "
            "7) MAXIMO 20 PALAVRAS. UMA LINHA. SEM EMOJI. SEM PALAVRAO. "
            "8) Fale COMO VIZINHO que fica na janela do 3º andar: coloquial, fofoqueiro, meio implicante, as vezes acerta, as vezes erra."
        )

    corpo_requisicao_base = {
        "max_tokens": 100,
        "temperature": 0.7,
        "stream": False
    }

    def _montar_prompt(nivel_qualidade=0):
        """
        Monta o prompt em 3 niveis de tamanho (para retry automatico):
        nivel 0 = COMPLETO (tudo: manual completo + info + ranking detalhado)
        nivel 1 = REDUZIDO (manual resumido + info basica + ranking curto)
        nivel 2 = MINIMO (so diretrizes + dinheiro + licencas, sem ranking)
        """
        if nivel_qualidade == 0:
            mf = MANUAL_FINAL
            ij = info_jogador
            tr = texto_do_ranking
            if len(tr) > 900:
                tr = tr[:900] + "\n    ... (top 10 truncado)"
            bloco_completo = mf + "\n" + ij + "\n\nPLACAR DO RANKING GLOBAL:\n" + tr
            if len(bloco_completo) > 3500:
                return _montar_prompt(1)
            cmd = comando_vitoria
        elif nivel_qualidade == 1:
            mf = MANUAL_BASE + "\n" + DIRETRIZ_FINAL
            ij_resumida = (
                f"SITUACAO DO JOGADOR:\n"
                f"- Nome: {nome}\n"
                f"- Bolso: R$ {carteira['Bolso']}\n"
                f"- Banco: R$ {carteira['Banco']}\n"
                f"- Licencas ativas: {lista_licencas if lista_licencas else 'Nenhuma'}\n"
                f"- Faltam: {licencas_faltantes_texto}\n"
            )
            tr = texto_do_ranking
            if len(tr) > 500:
                tr = tr[:500] + "\n    ... (top 10 truncado)"
            bloco = mf + "\n" + ij_resumida + "\n\nRANKING:\n" + tr
            if len(bloco) > 2500:
                return _montar_prompt(2)
            cmd = comando_vitoria
        else:
            mf = MANUAL_BASE + "\n" + DIRETRIZ_FINAL
            ij_minima = (
                f"JOGADOR:\n"
                f"- Nome: {nome}\n"
                f"- Bolso + Banco = R$ {float(carteira['Bolso']) + float(carteira['Banco']):.2f}\n"
                f"- Licencas: {lista_licencas if lista_licencas else 'Nenhuma'}\n"
            )
            bloco = mf + "\n" + ij_minima
            cmd = "Responda em 1 linha, max 20 palavras. Sem emoji. Seja breve."
        return (
            f"<bos><start_of_turn>user\n"
            f"{bloco}\n"
            f"\nVoce e ZE, o vizinho do 3º andar. {cmd}<end_of_turn>\n"
            f"<start_of_turn>model\n"
            f"Ze da janela diz: "
        )

    def _log_prompt(p):
        try:
            _log_caminho = os.path.join(pasta_base, "rodolfo_prompt_log.txt")
            with open(_log_caminho, "w", encoding="utf-8", errors="ignore") as _f_log:
                _f_log.write(f"=== TAMANHO PROMPT (chars): {len(p)} ===\n")
                _f_log.write(p)
        except Exception:
            pass

    resposta_final = None
    ultimo_erro = None
    for tentativa_nivel in [0, 1, 2]:
        prompt_atual = _montar_prompt(tentativa_nivel)
        _log_prompt(prompt_atual)
        corpo = dict(corpo_requisicao_base)
        corpo["prompt"] = prompt_atual
        dados_json = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=dados_json, headers={'Content-Type': 'application/json; charset=utf-8'})
        try:
            with urllib.request.urlopen(req, timeout=60) as resposta:
                resultado = json.loads(resposta.read().decode("utf-8"))
                texto = resultado.get("content", "").strip()
                texto_limpo = texto.replace("<end_of_turn>", "").replace('"', '').strip()
                texto_sem_emojis = "".join(c for c in texto_limpo if c.isalnum() or c in " .,;:!?()'-$R$+-/%")
                resposta_final = texto_sem_emojis.strip()
                break
        except urllib.error.HTTPError as he:
            ultimo_erro = he
            if he.code == 400:
                sleep(1)
                continue
            else:
                break
        except Exception as e:
            ultimo_erro = e
            break

    if resposta_final is None:
        return f"Um satelite saiu de orbita... (Erro: {ultimo_erro})"

    # ===== MEMORIA: marca assuntos falados para nao repetir =====
    try:
        rf_low = (resposta_final or "").lower()

        # Licencas de trabalho
        if ("trabalho facil" in rf_low) or ("trabalhos faceis" in rf_low):
            marcou_como_falado("recomendar_Trabalho1")
        if ("trabalho medio" in rf_low) or ("trabalhos medios" in rf_low):
            marcou_como_falado("recomendar_Trabalho2")
        if ("trabalho dificil" in rf_low) or ("trabalhos dificeis" in rf_low):
            marcou_como_falado("recomendar_Trabalho3")
        if ("tesouro" in rf_low) or ("desafio do tesouro" in rf_low):
            marcou_como_falado("recomendar_Trabalho4")
        if "carteira d" in rf_low:
            marcou_como_falado("recomendar_CarteiraD")

        # Ostentacao
        for palavra in ["iate", "mansao", "helicoptero", "guitarra", "ostenta", "luxo", "gasto tolo", "carro novo"]:
            if palavra in rf_low:
                marcou_como_falado("comentou_ostentacao")
                break

        # Outros assuntos
        for palavra in ["divida", "negativ", "pagar banco", "pagar divida"]:
            if palavra in rf_low:
                marcou_como_falado("comentou_divida")
                break
        for palavra in ["bolsa", "petroleo", "soja", "minerio", "algodao", "feno"]:
            if palavra in rf_low:
                marcou_como_falado("comentou_bolsa")
                break
        for palavra in ["ranking", "primeiro", "top 10", "top10", "colocado"]:
            if palavra in rf_low:
                marcou_como_falado("comentou_ranking")
                break
        for palavra in ["cripto", "placa de video", "bitinho", "minerar", "doge", "kripto", "rig"]:
            if palavra in rf_low:
                marcou_como_falado("comentou_cripto")
                break
        for palavra in ["picareta", "diamante", "mina"]:
            if palavra in rf_low:
                marcou_como_falado("comentou_picareta")
                break
        for palavra in ["frete", "caminhao", "carretinha"]:
            if palavra in rf_low:
                marcou_como_falado("comentou_frete")
                break
        for palavra in ["pesca", "peixe", "barco"]:
            if palavra in rf_low:
                marcou_como_falado("comentou_pesca")
                break
    except Exception:
        pass

    return resposta_final

# === LOOP DO CHAT INSTANTÂNEO ===
try:
    while True:

        # Puxa o conselho atualizado com base no save
        resposta = conversar_com_rodolfo()

        # ======================================================
        # DEBUG VISIVEL (só roda se DEBUG_RODOLFO = True no topo)
        # Usuario final NUNCA ve isso (deixe sempre False)
        # ======================================================
        try:
            dbg_carteira = carregar_dados("carteira", default_carteira.copy())
            dbg_bolso  = float(dbg_carteira.get("Bolso", 0))
            dbg_banco  = float(dbg_carteira.get("Banco", 0))
            dbg_total  = dbg_bolso + dbg_banco
            dbg_garagem= carregar_dados("garagem", default_Garagem.copy())
            dbg_licenc = carregar_dados("licencas", default_licenças.copy())
            try:
                dbg_acoes = carregar_dados("acoes_jogador", default_acoes_jogador.copy())
            except Exception:
                dbg_acoes = {}
            dbg_ult_acao   = dbg_acoes.get("ultima_acao", "") if isinstance(dbg_acoes, dict) else ""
            dbg_lic_ativas = [k for k,v in dbg_licenc.items() if v] if isinstance(dbg_licenc, dict) else []
            dbg_qtd_gar    = len(dbg_garagem) if hasattr(dbg_garagem, '__len__') else 0
        except Exception:
            dbg_bolso = 0.0
            dbg_banco = 0.0
            dbg_total = 0.0
            dbg_lic_ativas = []
            dbg_qtd_gar = 0
            dbg_ult_acao = ""

        # Limpa tela
        os.system('cls' if os.name == 'nt' else 'clear')

        texto_limpo = f'Ze da janela diz: "{resposta}"'
        linhas_texto = textwrap.wrap(texto_limpo, width=50)
        largura = 56

        print("╔" + "═" * (largura - 2) + "╗")
        print("║" + " ZÉ DO 3º ANDAR - VIZINHO FUXIQUEIRO ".center(largura - 2, " ") + "║")
        print("╠" + "═" * (largura - 2) + "╣")
        print("║" + "".center(largura - 2, " ") + "║")
        for linha in linhas_texto:
            print("║" + f" {linha} ".center(largura - 2, " ") + "║")
        print("║" + "".center(largura - 2, " ") + "║")
        print("╚" + "═" * (largura - 2) + "╝")

        # Caixa 2: DEBUG (APENAS SE DEBUG_RODOLFO = True)
        if DEBUG_RODOLFO:
            def _debug_linha(texto_esq):
                t = texto_esq[:largura-4]
                t = t + " " * (largura - 4 - len(t))
                return "║ " + t + " ║"

            print("╔" + "═" * (largura - 2) + "╗")
            print("║" + " DADOS LIDOS DO SAVE (MODO DEV) ".center(largura - 2, " ") + "║")
            print("╠" + "═" * (largura - 2) + "╣")
            print(_debug_linha(f"Bolso .......... R$ {dbg_bolso:>18,.2f}"))
            print(_debug_linha(f"Banco .......... R$ {dbg_banco:>18,.2f}"))
            print(_debug_linha(f"TOTAL .......... R$ {dbg_total:>18,.2f}"))
            print(_debug_linha(f"Itens Garagem: {dbg_qtd_gar}   Lic. ativas: {len(dbg_lic_ativas)}"))
            if dbg_lic_ativas:
                txt_lic = "Lic: " + ", ".join(dbg_lic_ativas)
                for ll in textwrap.wrap(txt_lic, width=largura-4):
                    print(_debug_linha(ll))
            if dbg_ult_acao:
                print(_debug_linha(""))
                txt_ult = f"Ult. acao: {dbg_ult_acao}"
                for ll in textwrap.wrap(txt_ult, width=largura-4):
                    print(_debug_linha(ll))
            print("╚" + "═" * (largura - 2) + "╝")

        # Espera 7~20s para proxima analise
        tempo = random.randint(7, 20)
        sleep(tempo)
except (EOFError, KeyboardInterrupt):
    pass
finally:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Fechando janela do 3º andar...")
    try:
        if server_process is not None and server_process.poll() is None:
            server_process.terminate()
            try:
                server_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server_process.kill()
    except Exception:
        pass
