from time import sleep, time
import webbrowser as w
from random import choice, randint, uniform, random,sample
import os
import threading
import json
import sys
import pymongo
import subprocess
import requests

alfabeto_codigo = {
    # Letras Minúsculas (Ajustadas para não gerarem números puros)
    'a': "ATR", 'b': 'ib', 'c': 'cp', 'd': 'DKN',
    'e': 'ELE', 'f': 'FXI', 'g': 'h', 'h': 'HFS', 'i': 'bi',
    'j': 'kj', 'k': 'jk', 'l': 'LTT', 'm': 'tm',
    'n': 'NTR', 'o': 'UIO', 'p': 'qp', 'q': 'pq',
    'r': 'RVP', 's': 'SMG', 't': 'xt', 'u': 'wn',
    'v': 'vlt', 'w': 'mw', 'x': 'xks', 'y': 'yps',
    'z': 'zln', " ": "ç", "!": "@", "?": "Qst",
    "-": "trl", "+": "PLS", "\n": "nm", "\r": "kl", "ç": "Pi",

    # Letras Maiúsculas
    'A': "A_NINE", 'B': 'I_BR', 'C': 'C_SIX', 'D': 'D_FIVE', 'E': 'E_TEN', 
    'F': 'F_THIRTY', 'G': 'H_GT', 'H': 'H_KEY', 'I': 'B_IN', 'J': 'K_JK', 
    'K': 'J_KJ', 'L': 'L_ZERO', 'M': 'T_MT', 'N': 'N_MINUS', 'O': 'iu_O', 
    'P': 'Q_PQ', 'Q': 'P_QP', 'R': 'R_BAR', 'S': 'S_DOL', 'T': 'X_TX', 
    'U': 'W_W', 'V': 'V_GT', 'W': 'M_M', 'X': 'X_PER', 'Y': 'Y_AND', 
    'Z': 'Z_PIPE', "Ç": "iP_C", ":": "CLN", ";": "SCLN",

    # Números quando estão DENTRO de um texto comum
    '0': "ZXL", '1': "WVD", '2': "RFG", '3': "YHM", '4': "KNB",
    '5': "JTS", '6': "QPL", '7': "MXZ", '8': "BDW", '9': "VCF",
    '.': "PNT"
}

# Tabela Numérica Pura (Para quando o valor original for um número int/float real)
numerico_codigo = {
    '0': "ZXL", '1': "WVD", '2': "RFG", '3': "YHM", '4': "KNB",
    '5': "JTS", '6': "QPL", '7': "MXZ", '8': "BDW", '9': "VCF",
    '.': "PNT", '-': "trl"
}

def decodificar(arquivo):
    # Se for Booleano
    if isinstance(arquivo, bool):
        return f"B:{arquivo}"
        
    # Se for Dicionário
    if isinstance(arquivo, dict):
        return {decodificar(k): decodificar(v) for k, v in arquivo.items()}
        
    # Se for Lista
    if isinstance(arquivo, list):
        return [decodificar(item) for item in arquivo]
        
    # Se for Número (Int ou Float)
    if isinstance(arquivo, (int, float)):
        texto_num = str(arquivo)
        num_cripto = "".join(numerico_codigo.get(c, c) for c in texto_num)
        return f"N:{num_cripto}"
        
    # Se for String (Texto comum)
    if isinstance(arquivo, str):
        texto_cripto = "".join(alfabeto_codigo.get(c, c) for c in arquivo)
        return f"S:{texto_cripto}"
        
    return arquivo

def DEScodificar(arquivo):
    # 1. Se for Dicionário
    if isinstance(arquivo, dict):
        return {DEScodificar(k): DEScodificar(v) for k, v in arquivo.items()}
        
    # 2. Se for Lista
    if isinstance(arquivo, list):
        return [DEScodificar(item) for item in arquivo]
        
    # 3. Se for uma String criptografada
    if isinstance(arquivo, str):
        alfabeto_reverso = {v: k for k, v in alfabeto_codigo.items()}
        numerico_reverso = {v: k for k, v in numerico_codigo.items()}
        
        # Caso A: Era um Booleano Original
        if arquivo.startswith("B:"):
            return arquivo[2:] == "True"
            
        # Caso B: Era um Número Original (Usa APENAS a tabela de números)
        if arquivo.startswith("N:"):
            conteudo = arquivo[2:]
            chaves_num = sorted(numerico_reverso.keys(), key=len, reverse=True)
            txt_num = ""
            i = 0
            while i < len(conteudo):
                achou = False
                for cod in chaves_num:
                    if conteudo[i:].startswith(cod):
                        txt_num += numerico_reverso[cod]
                        i += len(cod)
                        achou = True
                        break
                if not achou:
                    txt_num += conteudo[i]
                    i += 1
            return float(txt_num) if "." in txt_num else int(txt_num)
            
        # Caso C: Era um Texto Original (Usa APENAS a tabela de letras)
        if arquivo.startswith("S:"):
            conteudo = arquivo[2:]
            chaves_letra = sorted(alfabeto_reverso.keys(), key=len, reverse=True)
            txt_original = ""
            i = 0
            while i < len(conteudo):
                achou = False
                for cod in chaves_letra:
                    if conteudo[i:].startswith(cod):
                        txt_original += alfabeto_reverso[cod]
                        i += len(cod)
                        achou = True
                        break
                if not achou:
                    txt_original += conteudo[i]
                    i += 1
            return txt_original

    return arquivo

def limpar(): #o os.sla oque
    os.system('cls' if os.name == 'nt' else 'clear')
zerar = 0
VERDE = '\033[32m'
AMARELO = '\033[33m'
AZUL = '\033[34m'
VERMELHO = '\033[31m'
RESET = '\033[0m'
def atualizar_nuvem(nome_usuario, bolso, banco, lista_garagem, zerar, bandeira_empresa, nome_empresa):
    try:
        total = bolso + banco
        if bandeira_empresa == True:
            possui_emrpesa = f"{nome_empresa}| Faturamento de R${empresa['Faturamento']:,.2f}"
        else:
            possui_emrpesa = "Não possui empresa"
            
        ranking_col.update_one(
            {"nome": nome_usuario},
            {"$set": {
                "total": total,
                "bolso": bolso,
                "banco": banco,
                "garagem": lista_garagem, 
                "zerar": zerar,
                "Empresa": possui_emrpesa
            }},
            upsert=True # Se não existir o nome, ele cria um novo jogador
        )
    except Exception as e:
        print(f"Erro ao conectar com o ranking: {e}")

def salvar_dados(nome_arquivo, dados):
    global nome, carteira, Garagem, zerar, bandeira, nome_empresa
    with open(f"{nome_arquivo}.json", "w", encoding="utf-8") as f:
        # 1. Transforma o dicionário em texto puro (string)
        texto_puro = json.dumps(dados, ensure_ascii=False)
        
        # 2. Criptografa o texto puro (Troque 'codificar' pelo nome real da sua função de criptografia)
        dados_criptografados = decodificar(texto_puro)
        
        # 3. Salva no arquivo JSON
        json.dump(dados_criptografados, f, indent=4, ensure_ascii=False)
    if nome_arquivo == "carteira":
        try:
            atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar, bandeira['empresa'], nome_empresa)
        except Exception:
            pass


def carregar_dados(nome_arquivo, valor_padrao):

        try:
            with open(f"{nome_arquivo}.json", "r",encoding='utf-8') as f:
                dados_criptografados = json.load(f)
                texto_descriptografado = DEScodificar(dados_criptografados)
                return json.loads(texto_descriptografado)
        except (FileNotFoundError, Exception):
            return valor_padrao


def menu_leilao_investimento(seu_nome):
    while True:
        try:
            investimento = leilao_invest_col.find_one({"status": "aberto"})
            
            if not investimento:
                limpar()
                print("\n" + "—" * 40)
                print(" NENHUM LEILAO ATIVO NO MOMENTO ".center(40, " "))
                print("—" * 40)
                print("Aguarde o inicio da proxima rodada...")
                input("\nPressione Enter para voltar...")
                break
                
            limpar()
            
            # 🏢 1. MONTA AS LINHAS DA COLUNA DA ESQUERDA (LEILÃO ATUAL)
            col_esquerda = [
                " LEILÃO DE SOCIEDADE E RISCO ".center(50, "$"),
                "—" * 50,
                f" Projeto: {investimento['nome_investimento']}",
                f" Foco: {investimento['disc']}",
                f" Retorno Base: R$ {investimento['valor_prometido']:,.2f}",
                f" Risco de Falência: {investimento['risco_falencia'] * 100:.0f}%",
                f" Lance Mínimo/Atual: R$ {investimento['lance_atual']:,.2f}",
                f" Maior Investidor: {investimento['maior_apostador']}",
                "—" * 50
            ]
            
            # 📜 2. MONTA AS LINHAS DA COLUNA DA DIREITA (HISTÓRICO)
            col_direita = [
                " ÚLTIMOS RESULTADOS ".center(45, "—"),
                "—" * 45
            ]
            
            historicos = list(db["historico_leilao"].find().sort("timestamp", -1).limit(3))
            
            if not historicos:
                col_direita.append(" Nenhum registro anterior encontrado.".center(45))
                # Preenche com linhas vazias para alinhar com o tamanho da esquerda
                col_direita.extend(["", "", "", "", ""])
            else:
                for h in historicos:
                    if h["investidor"] == "nenhum":
                        col_direita.append(f" * {h['empresa']}: Ninguém apostou.")
                        col_direita.append("") # Linha em branco para espaçamento
                    else:
                        sinal = "+" if h["resultado"] == "SUCESSO" else ""
                        col_direita.append(f" * {h['empresa']} -> {h['investidor']}")
                        col_direita.append(f"   Lance: R$ {h['lance']:,.2f}")
                        col_direita.append(f"   Status: {h['resultado']} ({sinal}R$ {h['lucro']:,.2f})")
                
                # Preenche linhas vazias caso falte histórico para bater o tamanho da esquerda
                while len(col_direita) < len(col_esquerda):
                    col_direita.append("")
            
            col_direita.append("—" * 45)

            # 📺 3. IMPRIME AS DUAS COLUNAS LADO A LADO NA TELA
            print("\n" + "=" * 100)
            max_linhas = max(len(col_esquerda), len(col_direita))
            for i in range(max_linhas):
                # Pega a linha ou deixa em branco se a lista acabou
                esq = col_esquerda[i] if i < len(col_esquerda) else ""
                dir_linha = col_direita[i] if i < len(col_direita) else ""
                
                # O {:<50} garante que a coluna da esquerda tenha sempre exatamente 50 caracteres de largura
                print(f"{esq:<50} | {dir_linha}")
            print("=" * 100)
            
            # 🎮 4. MENU DE OPÇÕES (EMBAIXO DOS PAINÉIS)
            print("1-Dar um Lance     [ENTER]|Atualizar o Painel| 2-Sair")
            print("=" * 100)
            
            opcao = input("Escolha uma opcao: ").strip()
            
            if opcao == "1":
                try:
                    saldo_banco = carteira["Banco"]
                    print(f"\nSeu saldo atual no banco: R$ {saldo_banco:,.2f}")
                    
                    novo_lance = float(input("Digite o valor do seu lance: "))
                    
                    if investimento["maior_apostador"] == seu_nome:
                        print("\nErro: Você já é o maior investidor deste projeto!")
                        print("Aguarde outro jogador cobrir seu lance.")
                        input("\nPressione Enter para continuar...")
                        continue
                        
                    if novo_lance > saldo_banco:
                        print("Erro: Voce nao tem todo esse dinheiro no banco!")
                        input("\nPressione Enter para continuar...")
                        continue
                        
                    if novo_lance <= investimento["lance_atual"]:
                        print("Erro: Seu lance precisa ser maior que o lance atual!")
                        input("\nPressione Enter para continuar...")
                        continue
                        
                    leilao_invest_col.update_one(
                        {"_id": investimento["_id"]},
                        {"$set": {"lance_atual": novo_lance, "maior_apostador": seu_nome}}
                    )
                    
                    antigo_apostador = investimento["maior_apostador"]
                    antigo_lance = investimento["lance_atual"]
                    if antigo_apostador != "nenhum" and antigo_apostador != seu_nome:
                        ranking_col.update_one(
                            {"nome": antigo_apostador}, 
                            {"$inc": {"banco": antigo_lance, "total": antigo_lance}}
                        )
                        
                    ranking_col.update_one(
                        {"nome": seu_nome}, 
                        {"$inc": {"banco": -novo_lance, "total": -novo_lance}}
                    )
                    carteira["Banco"] -= novo_lance
                    salvar_dados("carteira", carteira)
                    jogador_atualizado = ranking_col.find_one({"nome": seu_nome})
                    if jogador_atualizado:
                        carteira["Banco"] = jogador_atualizado.get("banco", carteira["Banco"])
                    
                    salvar_dados("carteira", carteira)
                    
                    print(f"\nSucesso! Voce assumiu a lideranca com R$ {novo_lance:,.2f}!")
                    input("\nPressione Enter para atualizar o painel...")
                    continue
                    
                except ValueError:
                    print("Erro: Digite um numero valido.")
                    input("\nPressione Enter para continuar...")
                    continue
                    
            elif opcao == "2":
                print("Saindo do painel de investimentos...")
                sleep(1.2)
                break
            else:
                continue
                
        except Exception:
            print("Erro ao conectar com a nuvem do leilao.")
            input("\nPressione Enter para voltar...")
            break


def render():
    while True:
        sleep(150)
        global carteira
        carteira = carregar_dados("carteira", carteira)
        valor_atual = carteira["Banco"]
        if valor_atual > 350000:
            taxa = 0.15
        elif valor_atual > 100000:
            taxa = 0.12
        elif valor_atual > 50000:
            taxa = 0.1  
        elif valor_atual > 10000:
            taxa = 0.04  # 4% 
        elif valor_atual > 5000:
            taxa = 0.03  # 3%
        elif valor_atual > 500:
                taxa = 0.01  # 1%
        else:
            taxa = 0.008 # 0.8%

        rendimento = valor_atual * taxa
        if rendimento > 800000: 
            rendimento = 800000                

        if rendimento > 0:
            carteira["Banco"] = round(valor_atual + rendimento, 2)
            atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar, bandeira['empresa'], nome_empresa)
            try:
                salvar_dados("carteira", carteira)
                atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar, bandeira['empresa'], nome_empresa)
            except:
                pass


desenho_intro = rf"""{VERDE}
 _      _   __         ____               _                           
| |    (_) / _|  ___  | __ )  _   _  ___ (_) _ __    ___  ___  ___    
| |    | || |_  / _ \ |  _ \ | | | |/ __|| || '_ \  / _ \/ __|/ __|   
| |___ | ||  _||  __/ | |_) || |_| |\__ \| || | | ||  __/\__ \\__ \   
|_____||_||_|   \___| |____/  \__,_||___/|_||_| |_| \___||___/|___/   
 _____  _____  _____  _____  _____  _____  _____  _____  _____  _____ 
|_____||_____||_____||_____||_____||_____||_____||_____||_____||_____|{RESET}{AMARELO}
 ____          _      _  _____       _         _                      
/ ___|   ___  | |  __| ||_   _|_ __ (_)  __ _ | |                     
| |  _  / _ \ | | / _` |  | | | '__|| | / _` || |        15.5V DEBUG dev by 15V          
| |_| || (_) || || (_| |  | | | |   | || (_| || |                     
 \____| \___/ |_| \__,_|  |_| |_|   |_| \__,_||_|                     
 _____  _____  _____  _____  _____  _____  _____                      
|_____||_____||_____||_____||_____||_____||_____|       {RESET} By Arthur R.S (Rogerin)
"""
sleep(4)
default_primeira_intro = 1
default_nome = "INDIVIDADO"
nome = carregar_dados("nome",default_nome)
primeira_intro = carregar_dados("intro", default_primeira_intro)

#INTRO LEGAL
#jogo#
default_carteira = {"Bolso": 0.0, "Banco": -1400.0}
default_Garagem = {}
default_licenças = {"Trabalho1":True, "Trabalho2":False,"Trabalho3":False,"Trabalho4":False,"Carteira D":False,'View_conts': False}
clt_shop = {"Trabalho1": "GRATUITO", "Trabalho2": 800,"Trabalho3": 3000,"Trabalho4":10000,"Carteira D":1200, 'Secretário(a)': 380000}
mercado = {"Carro": 10000,"Caminhão": 52000, "Guitarra": 400, "Moto": 5000, "Casa Pequena": 12000, "Casa Média": 40000, "Mansão": 190000, "Helicóptero": 80000, "Telefone": 1200, "Bicicleta": 300,
                "Barco de pesca": 23000, "Barco grande": 120000, "Iate": 400000, "Picareta": 120,"PC p/ servidor": 40000 ,"GLOBO TERRESTRE": 10000000000,}
default_zerar = 0
carteira = carregar_dados("carteira", default_carteira)
licenças = carregar_dados("licencas", default_licenças)
for chave, valor in default_licenças.items():
    if chave not in licenças:
        licenças[chave] = valor
Garagem = carregar_dados("garagem", default_Garagem)
placa_caminhao = carregar_dados("placa_caminhão", "SEM-PLACA")
default_bandeira = {"imposto": False,"empresa":False}
bandeira = carregar_dados("bandeira",default_bandeira)
for chave, valor in default_bandeira.items():
    if chave not in bandeira:
        bandeira[chave] = valor
default_estudos = {"Administração": 0,"Gestão de finanças": 0,"Contabilidade": 0}
estudos = carregar_dados("estudos",default_estudos)
default_estudos_pag_inicial = {"Administração": False, "Gestão de finanças": False, "Contabilidade": False}
estudos_pag_inicial = carregar_dados("estudos_pag_inicial",default_estudos_pag_inicial)
default_nome_empresa = "DIVIDENDOS ANÔNIMOS"
nome_empresa = carregar_dados("nome_empresa",default_nome_empresa)
default_empresa = {
    "Nível":0,
    "Nível_propaganda": 0,
    "Faturamento": 0,
    "custo_upgrade": 150000,
    "custo_propaganda": 100000
}
empresa = carregar_dados("empresa",default_empresa)
t = threading.Thread(target=render, daemon=True)
t.start()

def imposto():
    while True:
        sleep(298)
        global carteira
        # Calcula o adicional da garagem
        adicional = len(Garagem) / 18
        if 'Carro' in Garagem:
            adicional += 0.07
        if bandeira['empresa'] == True:
            adicional += 0.20
        
        try:
            valor_atual = carteira["Banco"]
            
            # Taxas reduzidas para não falir o jogador
            if valor_atual >= 450000:
                taxa_imposto = 0.05 + adicional  # 5% de imposto
            elif valor_atual >= 200000:
                taxa_imposto = 0.04 + adicional  # 4% de imposto
            elif valor_atual >= 140000:
                taxa_imposto = 0.03 + adicional  # 3% de imposto
            elif valor_atual >= 25000:
                taxa_imposto = 0.01 + adicional  # 1% de imposto
            else:
                taxa_imposto = 0
                
            if taxa_imposto > 0:
                carteira["Banco"] -= valor_atual * taxa_imposto
                salvar_dados("carteira", carteira)
                atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar, bandeira['empresa'], nome_empresa)
                
        except Exception:
            sleep(20)
def pagamento_da_empresa():
    while True:
        sleep(71)
        carteira['Banco'] += empresa['Faturamento']
        try:
            salvar_dados("carteira", carteira)
        except:
            pass

def organizar_janelas_lado_a_lado():
    # 1. Define o título da janela do jogo atual e joga para a ESQUERDA
    os.system("title A Arte do Capitalismo")
    
    # Comando PowerShell para mover o Jogo (Posição X=0, Y=0, Largura=900, Altura=600)
    cmd_jogo = (
        'powershell -command "'
        '$w = Get-Process -Name cmd, powershell | Where-Object {$_.MainWindowTitle -eq \'A Arte do Capitalismo\'}; '
        'if ($w) { '
        '  $b = Add-Type -Name W -Namespace N -Method \'[DllImport(\\"user32.dll\\")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int h, bool r);\' -PassThru; '
        '  $b::MoveWindow($w.MainWindowHandle, 0, 0, 900, 600, $true) '
        '}"'
    )
    os.system(cmd_jogo)
    if getattr(sys, 'frozen', False):
        pasta_base = os.path.dirname(sys.executable)
    else:
        pasta_base = os.path.dirname(os.path.abspath(__file__))

    # Caminho do Rodolfo
    rodolfo = os.path.join(pasta_base, "Rodolfo.exe")

    # Tenta abrir o Rodolfo em JANELA SEPARADA (próprio CMD)
    try:
        if os.path.exists(rodolfo):
            # CREATE_NEW_CONSOLE = abre um CMD NOVO exclusivo para o Rodolfo
            # CREATE_NEW_PROCESS_GROUP = não morre junto com o jogo
            DETACHED = 0x00000010          # CREATE_NEW_CONSOLE
            NOVO_GRUPO  = 0x00000200        # CREATE_NEW_PROCESS_GROUP
            subprocess.Popen(
                [rodolfo],
                cwd=pasta_base,
                creationflags=DETACHED | NOVO_GRUPO
            )
            sleep(3)  # Espera a nova janela abrir e o title() rodar

            # Move a janela do Rodolfo (agora com título garantido)
            cmd_rodolfo = (
                'powershell -command "'
                'Start-Sleep -Milliseconds 800; '
                '$w = Get-Process | Where-Object { $_.MainWindowTitle -like \'*RODOLFO*\' -or $_.MainWindowTitle -like \'*MENTOR*\' -or $_.ProcessName -eq \'Rodolfo\' }; '
                'if ($w -is [array]) { $w = $w[0] }; '
                'if ($w -and $w.MainWindowHandle -ne 0) { '
                '  $b = Add-Type -Name W -Namespace N -Method \'[DllImport(\\"user32.dll\\")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int h, bool r);\' -PassThru; '
                '  $null = $b::MoveWindow($w.MainWindowHandle, 900, 0, 500, 680, $true); '
                '  $b2 = Add-Type -Name W2 -Namespace N2 -Method \'[DllImport(\\"user32.dll\\")] public static extern bool SetForegroundWindow(IntPtr h);\' -PassThru; '
                '  $null = $b2::SetForegroundWindow($w.MainWindowHandle) '
                '}"'
            )
            subprocess.Popen(["powershell", "-NoProfile", "-Command", cmd_rodolfo],
                             creationflags=0x08000000)  # CREATE_NO_WINDOW no powershell helper

        else:
            print("Rodolfo.exe não encontrado. O jogo continuará sem o assistente.")

    except Exception as e:
        print(f"Erro ao iniciar o Rodolfo: {e}")

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

def registrar_acao_jogador(chave_contador, texto_historico):
    '''Salva log da acao do jogador para o Rodolfo ler.'''
    global default_acoes_jogador
    dados = carregar_dados("acoes_jogador", default_acoes_jogador.copy())
    if "contadores" not in dados:
        dados["contadores"] = default_acoes_jogador["contadores"].copy()
    if "historico" not in dados:
        dados["historico"] = []
    for kk, vv in default_acoes_jogador["contadores"].items():
        if kk not in dados["contadores"]:
            dados["contadores"][kk] = vv
    if chave_contador and chave_contador in dados["contadores"]:
        dados["contadores"][chave_contador] += 1
    if texto_historico:
        dados["historico"].append(texto_historico)
        while len(dados["historico"]) > 5:
            del dados["historico"][0]
        dados["ultima_acao"] = texto_historico
    salvar_dados("acoes_jogador", dados)

config_pc = {}
carteiraKRYPTO = {}
def mineracao_background():
    while True:
        global config_pc, carteiraKRYPTO, carteira
        if os.path.exists("config_pc.json"):
        # Tabela de referência de poder (coloquei os nomes base)
            
            poder_referencia = { "GT720 *velha*":1,
                    "GT720": 5, "GTX1050": 10, "GTX1090": 25, 
                    "RTX2060": 60, "RTX3090": 150
                }
            while True:
                sleep(20) # Ciclo de mineração (ajuste o tempo se quiser)
                        # 1. CALCULA POTÊNCIA TOTAL
                config_pc = carregar_dados("config_pc", config_pc)
                    

                    
                if config_pc:
                    potencia_total = 0
                    try:
                        for item in list(config_pc.keys()):
                                # Limpa o nome (ex: "RTX3090 #1" vira "RTX3090")
                            nome_base = item.split(" #")[0].split(" *")[0]
                            potencia_total += poder_referencia.get(nome_base, 0)

                            # 2. SORTEIO E FRAGMENTOS (Só se tiver placa)
                            if potencia_total > 0:
                                sorte = randint(1, 100)
                                        
                                        # Lógica de raridade
                                if sorte <= 5:    moeda = "DOGECOIN"
                                elif sorte <= 15: moeda = "Bitinho coin"
                                elif sorte <= 25: moeda = "Kryptonita"
                                elif sorte <= 60: moeda = "Lixo kripto"
                                else:             moeda = "Lixo do Lixo Krypto"
                                        # Ganho baseado na potência (ajuste o divisor 1000 para balancear)
                                quantidade = (potencia_total / 25000) * uniform(0.5, 1.5)    
                                    # 3. SALVA NA CARTEIRA KRIPTO
                                carteiraKRYPTO[moeda] = carteiraKRYPTO.get(moeda, 0) + quantidade
                                salvar_dados("Carteira Krypto", carteiraKRYPTO)
                    except Exception:
                        pass
        else:
            sleep(2)
            continue
def barra_viagem(segundos):
    print(f"\nIniciando viagem... ({segundos}s)")
    tamanho_barra = 20 # Quantos quadradinhos a barra terá
    
    for i in range(tamanho_barra + 1):
        # Calcula a porcentagem
        percent = int((i / tamanho_barra) * 100)
        
        # Cria a string da barra: [##########----------]
        preenchido = "█" * i
        vazio = "-" * (tamanho_barra - i)
        
        # \r faz o print sobrescrever a linha atual
        sys.stdout.write(f"\rProgresso: [{preenchido}{vazio}] {percent}%")
        sys.stdout.flush() # Força o terminal a mostrar o texto na hora
        
        # Divide o tempo total pelo tamanho da barra
        sleep(segundos / tamanho_barra)

riscos = {
    "Petroleo": 0.08,  # Muito instável
    "Minerio": 0.08,   # Instável
    "Soja": 0.06,      # Estável
    "Algodao": 0.03,   # Bem estável
    "Feno": 0.04       # Quase não muda
}
evento_atual = "Mercado Estável"
# Dicionário de eventos: Item afetado e o multiplicador (ex: 1.5 = sobe 50%, 0.5 = cai 50%)
eventos_possiveis = [
    ("Estreito de ormuz está comprometido", "Petroleo", 1.8),
    ("Praga na Lavoura", "Soja", 2),
    ("Seca no Sertão", "Feno", 2.0),
    ("Inovação Têxtil", "Algodao", 1.5),
    ("Crise na Construção", "Minerio", 2),
    ("Clima Perfeito", "Soja", 0.5),
    ("Descoberta de novo templo", "Minerio", 0.6),
    ("Animais da Lavoura estão sadios", "Feno", 0.5),
    ("Milhares de barrís de petróleo foram ilegalmente vendidos para todos os continentes!!", "Petroleo", 0.4)
]
precos = {"Petroleo": 1500.0, "Minerio": 800.0, "Soja": 350.0, "Algodao": 120.0, "Feno": 40.0}
def oscilar_mercado():
    global precos, evento_atual
    while True:
        if randint(1,100) < 45: 
            nome_ev, item_ev, impacto = choice(eventos_possiveis)
            evento_atual = f"ALERTA: {nome_ev}!"
            precos[item_ev] = round(precos[item_ev] * impacto, 2)
        else:
            evento_atual = "Mercado Estável"
        for item in precos:
            # Petróleo/Minério oscilam até 7%, o resto até 3%
            volatilidade =  riscos[item] 
            fator = uniform(-volatilidade, volatilidade)
            
            # Aplica a oscilação
            precos[item] = round(precos[item] * (1 + fator), 2)
            
            # Trava para o preço não ficar negativo ou zero
            if precos[item] < 0.5: precos[item] = 0.5
        salvar_dados("mercado_ao_vivo", {"precos": precos, "noticia": evento_atual})
        sleep(30)

def digitar(texto, velocidade=0.05):
    for caractere in texto:
        sys.stdout.write(caractere)
        sys.stdout.flush()
        sleep(velocidade)
    print()

#MONGO MONGO MONGO MONGO MONGO MONGO
LINK_MONGO =  "mongodb+srv://superartitude_db_user:123Mongo@cluster0.tbesz68.mongodb.net/?appName=Cluster0"
client = pymongo.MongoClient(LINK_MONGO, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000, socketTimeoutMS=10000)
db = client.get_database('jogo_vida')
ranking_col = db.ranking
leilao_invest_col = db["leilao_investimentos"]
#MONGO MONGO MONGO MONGO MONGO MONGO

def ver_ranking(seu_nome_atual):
    try:
        print("\n" + "—" * 40)
        print(" TOP 10 JOGADORES TOTAIS ".center(40,"$"))
        print("—" * 40)
        titulos = [
            (1000000000000, "SOBERANO DA ECONOMIA"),
            (500000000000,  "LENDARIO DOS NEGOCIOS"),
            (100000000000,  "TITÃ FINANCEIRO"),
            (50000000000,   "BARÃO DO MERCADO"),
            (10000000000,   "MULTIBILIONARIO"),
            (1000000000,    "BILIONARIO"),
            (500000000,     "MAGNATA"),
            (100000000,     "GRANDE INVESTIDOR"),
            (50000000,      "INVESTIDOR SENIOR"),
            (10000000,      "MILIONARIO"),
            (5000000,       "EMPREENDEDOR DE SUCESSO"),
            (1000000,       "CONSOLIDADO"),
            (500000,        "ACUMULADOR"),
            (100000,        "BEM SUCEDIDO"),
            (50000,         "EM ASCENSÃO"),
            (10000,         "ESTAVEL"),
            (5000,          "AUTONOMO"),
            (2500,          "TRABALHADOR"),
            (2000,          "ESFORÇADO"),
            (1500,          "APRENDIZ"),
            (1000,          "ESTAGIARIO"),
            (500,           "SOBREVIVENTE"),
            (0,             "INICIANTE")
        ]
        # Busca os 10 mais ricos
        jogadores = ranking_col.find().sort("total", -1).limit(10)
        
        for i, j in enumerate(jogadores, 1):
            # 🌟 CORREÇÃO 1: O status padrão precisa ser resetado para CADA jogador
            status = "INICIANTE"
            
            nome_player = j.get('nome', 'Desconhecido')
            bolso = j.get('bolso', 0)
            banco = j.get('banco', 0)
            total = j.get('total', 0)
            zerou = j.get('zerar', 0)
            
            # Ajuste caso garagem venha como dicionário ou lista
            garagem_crua = j.get('garagem', [])
            if isinstance(garagem_crua, dict):
                itens = ", ".join(garagem_crua.keys())
            else:
                itens = ", ".join(garagem_crua)
                
            possui_empresa = j.get('Empresa')

            # Mostra o Nome e o Total em destaque
            for valor_minimo, nome_titulo in titulos:
                if total >= valor_minimo:
                    status = nome_titulo                    
                    break   # 🌟 CORREÇÃO 2: O break impede o Python de continuar descendo para títulos menores!
            
            if nome_player == seu_nome_atual:
                print(f"{i}º| {status:<25} | {nome_player} <--- (EU)")
            else:
                print(f"{i}º| {status:<25} | {nome_player}")
            print(f"    TOTAL: R$ {total:,.2f} (Bolso: R$ {bolso:,.2f} | Banco: R$ {banco:,.2f})")
            print(f"    Zerou: {zerou} vezes")
            print(f"    Itens: {itens if itens else 'Nenhum'}")
            print(f"    Empresa: {possui_empresa if possui_empresa else 'Não possui empresa'}")
            print("—" * 40)

        input("\nPressione Enter para voltar ao menu...")
    except Exception as e:
        print(f"Falha na rede ou Nuvem!\n{e}")
        sleep(2)
#VER RANKING PARA ESTE JOGO

#VER RANKING PARA A IA ASSISTENTE
def puxar_ranking_para_rodolfo(seu_nome_atual):
    try:
        titulos = [
            (1000000000000, "SOBERANO DA ECONOMIA"),
            (500000000000,  "LENDARIO DOS NEGOCIOS"),
            (100000000000,  "TITÃ FINANCEIRO"),
            (50000000000,   "BARÃO DO MERCADO"),
            (10000000000,   "MULTIBILIONARIO"),
            (1000000000,    "BILIONARIO"),
            (500000000,     "MAGNATA"),
            (100000000,     "GRANDE INVESTIDOR"),
            (50000000,      "INVESTIDOR SENIOR"),
            (10000000,      "MILIONARIO"),
            (5000000,       "EMPREENDEDOR DE SUCESSO"),
            (1000000,       "CONSOLIDADO"),
            (500000,        "ACUMULADOR"),
            (100000,        "BEM SUCEDIDO"),
            (50000,         "EM ASCENSÃO"),
            (10000,         "ESTAVEL"),
            (5000,          "AUTONOMO"),
            (2500,          "TRABALHADOR"),
            (2000,          "ESFORÇADO"),
            (1500,          "APRENDIZ"),
            (1000,          "ESTAGIARIO"),
            (500,           "SOBREVIVENTE"),
            (0,             "INICIANTE")
        ]
        # Busca os 10 mais ricos (Exatamente igual ao seu)
        jogadores = ranking_col.find().sort("total", -1).limit(10)

        linhas_ranking = []
        for i, j in enumerate(jogadores, 1):
            nome_player = j.get('nome', 'Desconhecido')
            bolso = j.get('bolso', 0)
            banco = j.get('banco', 0)
            total = j.get('total', 0)
            zerou = j.get('zerar', 0)
            itens = ", ".join(j.get('garagem', []))

            status = "INICIANTE"
            for valor_minimo, nome_titulo in titulos:
                if total >= valor_minimo:
                    status = nome_titulo
                    break   
            
            # Monta o texto no mesmo formato do seu print, mas salvando na lista
            if nome_player == seu_nome_atual:
                linhas_ranking.append(f"{i}º| {status} | {nome_player} <--- (VOCÊ, O JOGADOR)")
            else:
                linhas_ranking.append(f"{i}º| {status} | {nome_player}")
            
            linhas_ranking.append(f"    TOTAL: R$ {total:,.2f} (Bolso: R$ {bolso:,.2f} | Banco: R$ {banco:,.2f})")
            linhas_ranking.append(f"    Zerou: {zerou} vezes")
            linhas_ranking.append(f"    Itens: {itens if itens else 'Nenhum'}")

        # Retorna o placar completo como um bloco único de texto limpo
        return "\n".join(linhas_ranking)
    except Exception:
        return "Falha na rede ou Nuvem ao tentar ler o ranking de competidores!"

class car:
    
    def __init__(self, dados):
        if isinstance(dados, tuple):
            # Se for a tupla padrão:
            self.modelo_carro = dados[0]
            self.potencia_carro = dados[1]
            self.cor_carro = dados[2]
            self.limite_tuning = dados[3]
            self.tem_nitro = False
        else:
            # Se for o dicionário carregado do JSON:
            self.modelo_carro = dados["modelo_carro"]
            self.potencia_carro = dados["potencia_carro"]
            self.cor_carro = dados["cor_carro"]
            self.limite_tuning = dados["limite_tuning"]
            self.tem_nitro = dados["tem_nitro"]
        self.distancia = 0

    def comprarNITRO(self,dinheiro):
        if self.tem_nitro == True:
            print('Você já possui Nitro!')
            return {'C':False,'$': 0}
        else:
            Y_N = input('O nitro custa R$9.000,00 conto, vai comprar?\nS/N:>>> ').strip().upper()
            if Y_N == 'S':
                if dinheiro >= 9000:
                    print('aproveite seu nitro!')
                    sleep(1)
                    limpar()
                    verificar = self.potencia_carro + 120
                    if verificar > self.limite_tuning:
                        self.potencia_carro = self.limite_tuning + 20
                        self.limite_tuning += 20
                    else:
                        self.tem_nitro = True
                        self.potencia_carro += 120
                        self.limite_tuning += 20
                    return {'C':True,'$': 9000}
                else:
                    print('Valor insuficiente!')
                    sleep(1)
                    limpar()
                    return {'C':False,'$': 0}
            else:
                return {'C':False,'$': 0}
                

    def acelerar(self,distancia=60):
        movimento = 0
        tempo_KM = 100
        velocidade = self.potencia_carro
        tempo_KM = tempo_KM // velocidade
        for _ in range(distancia):
            print(f'KM ATUAL: {movimento}',end='',flush=True)
            sleep(tempo_KM)
            movimento += 1
            limpar()
        
        print(f'CHEGOU AO FINAL DOS {distancia} KM')

    def corrida(self, oponente, distancia_pista=30):
        # Os dois começam no quilômetro zero
        self.distancia = 0
        oponente.distancia = 0

        # Define um tamanho fixo visual para a pista na tela (40 caracteres)
        largura_pista_tela = 40

        # O loop roda enquanto NENHUM dos dois cruzou a linha de chegada
        while self.distancia < distancia_pista and oponente.distancia < distancia_pista:
            
            # Sua maracutaia de ritmo original continua igual!
            avanco_meu = randint(1, max(2, int(self.potencia_carro * 0.1)))
            avanco_oponente = randint(1, max(2, int(oponente.potencia_carro * 0.1)))
            
            self.distancia += avanco_meu
            oponente.distancia += avanco_oponente

            # Garante que nenhum carro passe do limite da pista no texto
            if self.distancia > distancia_pista: self.distancia = distancia_pista
            if oponente.distancia > distancia_pista: oponente.distancia = distancia_pista

            # CONVERSÃO VISUAL: Transforma a distância real em fatias da pista da tela
            fatias_minhas = int((self.distancia / distancia_pista) * largura_pista_tela)
            fatias_oponente = int((oponente.distancia / distancia_pista) * largura_pista_tela)

            # Monta as duas pistas com os carrinhos andando (pode trocar os símbolos se quiser)
            pista_minha = "." * fatias_minhas + ">" + "." * (largura_pista_tela - fatias_minhas)
            pista_oponente = "." * fatias_oponente + "X" + "." * (largura_pista_tela - fatias_oponente)

            # EXIBIÇÃO FORMATADA: Alinha os nomes em 20 espaços para a pista começar igual
            limpar()
            print(" DISPUTA DE RUA ".center(70, "="))
            print(f" {self.modelo_carro:<20} |{pista_minha}| {self.distancia}/{distancia_pista} KM")
            print(f" {oponente.modelo_carro:<20} |{pista_oponente}| {oponente.distancia}/{distancia_pista} KM")
            print("=" * 70)
            
            sleep(0.4) # Dá uma pausinha rápida para o jogador conseguir assistir
            limpar()

        # FIM DA CORRIDA: Quem acumulou mais distância ganhou!
        if self.distancia > oponente.distancia:
            print(f" {self.modelo_carro} VENCEU A CORRIDA!")
            return 'V'
        elif oponente.distancia > self.distancia:
            print(f" {oponente.modelo_carro} VENCEU A CORRIDA!")
            return 'D'
        else:
            print(" EMPATE EM CIMA DA LINHA DE CHEGADA!")
            return 'E'

    def tunar(self,dinheiro):
        print('Você quer tunar seu carro?')
        S_Y = input('S/N:>>> ').strip().upper()
        limpar()
        if S_Y == 'S':
            while True:
                limpar()
                try:
                    if self.potencia_carro >= self.limite_tuning:
                        print('Você não pode mais Tunar este carro')
                    else:
                        print('Qual o tamanho dessa Tunagem? (Quantidade de cavalos 1 = 100)')
                        tamanho_tuning = float(input(':>>> ').strip())
                        preço = 5000
                        cavalo = 100
                        preço += tamanho_tuning * cavalo
                        limite_atual = self.limite_tuning - self.potencia_carro
                        if (tamanho_tuning * cavalo) > limite_atual:
                            print(f'Seu carro não suporta essa modificação!\nVocê tem {self.potencia_carro} cavalos, o limite é de {self.limite_tuning} cavalos')
                            sleep(2)
                            continue
                        print(f'Vai custar R${preço:,.2f}. Para + {tamanho_tuning*cavalo} Cavalos à potência. Você tem R${dinheiro:,.2f}')
                        s_y = input('PAGAR TUNING? [x-sair] S/N:>>> ').strip().upper()
                        if s_y == 'S':
                            if dinheiro >= preço:
                                self.potencia_carro += tamanho_tuning*cavalo
                                print('Tunagem Feita!')
                                return {'C':True,'$':preço}
                            else:
                                print('saldo insuficiente.')
                                return {'C':False,'$':0}
                        elif s_y == 'X':
                            
                            return {'C':False,'$':0}
                        else:
                            
                            continue
                except ValueError:
                    print('VALOR INVÁLIDO')
                else:            
                    return {'C':False,'$':0}


def doar_dinheiro(seu_nome):
    limpar()
    print("\n" + "—" * 40)
    print(" ENVIAR TRANSFERENCIA / DOAÇÃO ".center(40, "$"))
    print("—" * 40)
    
    nome_destino = input("Digite o nome do jogador que vai receber: ").strip()
    
    if nome_destino == seu_nome:
        print("Erro: Voce nao pode doar para voce mesmo!")
        return

    # 1. Procura o jogador que vai receber na nuvem
    jogador_destino = ranking_col.find_one({"nome": nome_destino})
    if not jogador_destino:
        print("Erro: Jogador nao encontrado no ranking da nuvem!")
        return
        
    try:
        valor = float(input(f"Quanto deseja doar? (Saldo atual: R$ {carteira['Banco']:,.2f}): "))
        
        if valor <= 0 or valor > carteira["Banco"]:
            print("Erro: Saldo insuficiente ou valor invalido!")
            return
            
        # 2. Atualiza os saldos na Nuvem para os DOIS jogadores ao mesmo tempo
        ranking_col.update_one({"nome": seu_nome}, {"$inc": {"banco": -valor, "total": -valor}})
        ranking_col.update_one({"nome": nome_destino}, {"$inc": {"banco": valor, "total": valor}})
        
        # 3. Envia o aviso para a lista de notificacoes do jogador destino na nuvem
        ranking_col.update_one(
            {"nome": nome_destino},
            {"$push": {"notificacoes": f"Voce recebeu uma doacao de R$ {valor:,.2f} de {seu_nome}!"}}
        )
        
        # 4. Atualiza o SEU jogo local na mesma hora
        carteira["Banco"] -= valor
        salvar_dados("carteira", carteira)
        
        print(f"\nSucesso! R$ {valor:,.2f} enviados para {nome_destino}!")
        sleep(2)
        
    except ValueError:
        print("Erro: Digite um numero valido.")
    sleep(2)
    limpar()

def verificar_notificacoes(seu_nome):
    try:
        # 1. Busca os dados do jogador na nuvem
        jogador = ranking_col.find_one({"nome": seu_nome})
        
        if jogador:
            # 2. Atualiza o saldo local com o banco da nuvem (onde as doacoes caem)
            global carteira
            carteira["Banco"] = jogador.get("banco", carteira["Banco"])
            salvar_dados("carteira", carteira)
            
            # 3. Pega as mensagens pendentes
            mensagens = jogador.get("notificacoes", [])
            
            if mensagens:
                limpar()
                print("\n" + "—" * 40)
                print(" NOVAS NOTIFICACOES ".center(40))
                print("—" * 40)
                if mensagens:
                # 🌟 AQUI acontece a mágica! O seu banco local recebe o valor 
                # que já foi somado pelo seu amigo lá na nuvem:
                    carteira["Banco"] = jogador.get("banco", carteira["Banco"])
                    
                    # Salva localmente sem disparar o gatilho que limpa a nuvem
                    with open("carteira.json", "w", encoding="utf-8") as f:
                        texto_puro = json.dumps(carteira, ensure_ascii=False)
                        f.write(decodificar(texto_puro))

                for msg in mensagens:
                    print(f"* {msg}")
                print("—" * 40 + "\n")
                
                # 4. Limpa as notificacoes na nuvem para o aviso nao repetir
                ranking_col.update_one({"nome": seu_nome}, {"$set": {"notificacoes": []}})
                
                input("Pressione Enter para continuar...")
                limpar()
    except Exception as e:
        pass

def Jogo_principal():
    global nome, carteira, Garagem, zerar, bandeira, nome_empresa, primeira_intro, estudos_pag_inicial,estudos,licenças,placa_caminhao
    zerar = carregar_dados("zerar", default_zerar)
    nome_empresa = carregar_dados("nome_empresa",default_nome_empresa)
    primeira_intro = carregar_dados("intro", default_primeira_intro)
    estudos_pag_inicial = carregar_dados("estudos_pag_inicial",default_estudos_pag_inicial)
    bandeira = carregar_dados("bandeira",default_bandeira)
    estudos = carregar_dados("estudos",default_estudos)
    carteira = carregar_dados("carteira", default_carteira)
    licenças = carregar_dados("licencas", default_licenças)
    Garagem = carregar_dados("garagem", default_Garagem)
    placa_caminhao = carregar_dados("placa_caminhão", "SEM-PLACA")
    nome = carregar_dados("nome",default_nome)
    primeira_intro = carregar_dados("intro", default_primeira_intro)
    

    atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar, bandeira['empresa'], nome_empresa)
    
    if "GLOBO TERRESTRE" in Garagem: #efeito zerar
        limpar()
        print(f"Você comprou o mundo, tudo é seu. Parabéns por zerar o game {nome}")
        DECISAO = input("Você quer reiniciar o jogo?\n N/S: ")
        if DECISAO.strip().upper() == "S":            
            arquivos_para_deletar = [
                "config_pc.json", "Carteira Krypto.json", "carteira_motorista.json",
                "placa_caminhão.json", "estoque agro.json", "Historico preços.json",
                "fadiga.json", "Historico km.json", "aviso.json","empresa.json",
                "estudos.json","estudos_pag_inicial.json","mercado_ao_vivo.json","nome_empresa.json",
                "acoes_jogador.json","licencas.json","garagem.json","carteira.json","aviso.json","bandeira.json","NFS.json",
                "fama.json","carro_atual.json"
            ]

            for arquivo in arquivos_para_deletar:
                if os.path.exists(arquivo):
                    os.remove(arquivo)


            zerar += 1
            salvar_dados("zerar", zerar)
            primeira_intro +=1
            salvar_dados("intro",primeira_intro)
            atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
            exit()
        else:
            print("OBRIGADO POR JOGAR| FECHE O PROGRAMA (1 hora para fechar automaticamente)")
            atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
            sleep(3600)
            exit()

    ##########################################
    if primeira_intro > 0:
        if os.path.exists("Carteira Krypto.json"):
            os.remove("Carteira Krypto.json")
        limpar()
        if zerar == 0:
            digitar("PARABÉNS! Você é um empresário fracassado...")
        else:
            digitar("PARABÉNS! Você é um empresário fracassado... (DE NOVO)")
        sleep(1.5)
        digitar("Tentou seguir a vida que todos DIZIAM ser a chave para o sucesso.") 
        sleep(3)
        digitar("E olha você agora... com diploma, sem dinheiro, com dívidas e pensando: ")
        sleep(2)
        digitar(f"{AMARELO}'porque não trabalhei na mecânica do meu avô?'{RESET}",velocidade=0.08)
        sleep(2)
        digitar("Mas você descobriu uma coisa.")
        sleep(1)
        digitar("Dinheiro não aparece só porque você trabalhou duro.")
        digitar(f"Ele aparece quando você sabe onde colocar o seu{VERMELHO} esforço{RESET}.")
        digitar("Uma carga pode valer uma fortuna")
        sleep(0.4)
        digitar("Uma mina pode esconder milhões")
        digitar("Mas um tanque cheio pode transformar lucro em prejuízo.")
        sleep(3)
        digitar(f"E uma decisão ruim... ...pode fazer você começar tudo{VERMELHO} de novo.{RESET}",velocidade=0.08)
        sleep(3)
        digitar("Existe vários empregos")
        digitar("Se um não dá conta, pegue dois")
        digitar("Se nem dois dá conta, PEGUE TODOS!")
        sleep(1.8)
        digitar("Agora dê seu jeito... Porque está prestes a entrar no..")
        sleep(2.5)
        limpar()
        digitar(rf"""{VERDE}
                 _      _   __         ____               _                           
                | |    (_) / _|  ___  | __ )  _   _  ___ (_) _ __    ___  ___  ___    
                | |    | || |_  / _ \ |  _ \ | | | |/ __|| || '_ \  / _ \/ __|/ __|   
                | |___ | ||  _||  __/ | |_) || |_| |\__ \| || | | ||  __/\__ \\__ \   
                |_____||_||_|   \___| |____/  \__,_||___/|_||_| |_| \___||___/|___/   
                _____  _____  _____  _____  _____  _____  _____  _____  _____  _____ 
                |_____||_____||_____||_____||_____||_____||_____||_____||_____||_____|{RESET}{AMARELO}
                 ____          _      _  _____       _         _                      
                / ___|   ___  | |  __| ||_   _|_ __ (_)  __ _ | |                     
                | |  _  / _ \ | | / _` |  | | | '__|| | / _` || |                    
                | |_| || (_) || || (_| |  | | | |   | || (_| || |                     
                 \____| \___/ |_| \__,_|  |_| |_|   |_| \__,_||_|                     
                _____  _____  _____  _____  _____  _____  _____                      
                |_____||_____||_____||_____||_____||_____||_____|       {RESET} 
""",velocidade=0.002)
        sleep(6.5)
        limpar()
        if not os.path.exists("nome.json"):
            nome = input("SEU NOME: ")
            salvar_dados("nome",nome)
        primeira_intro -= 1
        salvar_dados("intro",primeira_intro)
    else:
        limpar()
        digitar(desenho_intro, velocidade=0.001) 
        sleep(4)
    ###########################################
    limpar()

    
    
    
    c = threading.Thread(target=mineracao_background, daemon=True)
    c.start()
    threading.Thread(target=oscilar_mercado, daemon=True).start()


    if bandeira.get("imposto",False) is True: #PARA INICIAR IMPOSTO
        threading.Thread(target=imposto, daemon= True).start()
    if bandeira.get("empresa",False) is True: #PARA INICIAR GANHOS DA EMPRESA
        threading.Thread(target=pagamento_da_empresa,daemon=True).start()
    organizar_janelas_lado_a_lado()
    #INICIO DO WHILE PARA JOGO PRINCIPAL
    while True:
        #DIVIDA
        if carteira["Bolso"] <0:
            carteira["Banco"] += carteira["Bolso"]
            carteira["Bolso"] = 0
            salvar_dados('carteira',carteira)
        else:   
            pass
        #DIVIDA
        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
        limpar()
        print("JOGO DA VIDA".center(40,"="))
        print(f"USUÁRIO: {nome}")
        #MENSAGENS COSTUMIZADAS PARA QUEM ZEROU O GAME
        if zerar == 1:
            print(f"!Você zerou o jogo {zerar} vez! :)")
        elif 1 < zerar < 3:
            print(f"!Você zerou o jogo {zerar} vezes! :)")
        elif zerar >= 3:
            print(f"Caramba, Você zerou o jogo {zerar} vezes! Cansou não?\n")
        #MENSAGENS COSTUMIZADAS PARA QUEM ZEROU O GAME
        zero = 0
        zerozero = carregar_dados("aviso",zero)
        um = 1
        um_um = carregar_dados("aviso",um)
        if "Barco de pesca" in Garagem:print("[10] Ir pescar") 
        if "Moto" in Garagem:print("[11] Moto boy")
        if "Picareta" in Garagem:print("[12] Minerar") 
        if "PC p/ servidor" in Garagem:print("[13] BITINHO COIN") 
        if "Caminhão" in Garagem:print("[14] Frete") 
        if "Telefone" in Garagem: print("[15] Bolsa de Valores")
        if "Bicicleta" in Garagem: print("[16] Bike boy")
        if 'Carro' in Garagem: print('[17] Corrida de Rua')

        if carteira["Banco"] > 25000:
            if zerozero <= 0:
                limpar()
                print("Você tem um valor alto na conta, a receita federal ira cobrar uma taxa a cada cinco minutos!!!\nPense aonde vai deixar seu dinheiro.")
                zero += 1
                sleep(5)
                limpar()
                salvar_dados("aviso",zero)
                bandeira["imposto"] = True
                salvar_dados("bandeira",bandeira)
                threading.Thread(target=imposto, daemon= True).start()
                continue

        if all(valor == 100 for valor in estudos.values()):
            escolha = input("OPÇÕES|ONLINE| [R] Ver ranking           EDUCAÇÃO| [E] Ensino Superior           EMPRESA| [C] Comércio\n\n[1] Trabalhos Fáceis\n[2] Trabalhos Médios\n[3] Trabalhos Difíceis\n[4] Desafio do tesouro\n[5] LOJA DE DESBLOQUEIO DE TRABALHOS\n[6] Visualizar carteira\n[7] Banco do Brasil\n[8] Ver garagem\n[9] Mercado\n--> ").upper()
        else:    
            escolha = input("OPÇÕES|ONLINE| [R] Ver ranking           EDUCAÇÃO| [E] Ensino Superior\n\n[1] Trabalhos Fáceis\n[2] Trabalhos Médios\n[3] Trabalhos Difíceis\n[4] Desafio do tesouro\n[5] LOJA DE DESBLOQUEIO DE TRABALHOS\n[6] Visualizar carteira\n[7] Banco do Brasil\n[8] Ver garagem\n[9] Mercado\n--> ").upper()
        #TODO O RESTO
        if escolha == "5": #Venda licença
            registrar_acao_jogador("passou_por_loja", "Entrou na Loja de Licencas de Trabalho")
            if carteira["Banco"] < 0:
                print("Pague suas dívidas antes de efetuar qualquer compra!")
                input("ENTER PARA CONTINUAR")
            else:
                loja_clt = True
                while loja_clt:
                    try:
                        limpar()
                        print("LICENÇAS CLT".center(40,"="))
                        print(f"[x]Trabalhos fáceis: {clt_shop['Trabalho1']}")
                        if licenças["Trabalho2"] is False:
                            print(f"[1]Trabalhos Médios: R${clt_shop['Trabalho2']:,.2f}")
                        else:
                            print(f"[1]Trabalhos Médios: COMPRADO")
                        if licenças["Trabalho3"] is False:
                            print(f"[2]Trabalhos Difíceis: R${clt_shop['Trabalho3']:,.2f}")
                        else:
                            print(f"[2]Trabalhos Difíceis: COMPRADO")
                        if licenças["Trabalho4"] is False:
                            print(f"[3]Desafio do tesouro: R${clt_shop['Trabalho4']:,.2f}")
                        else:
                            print(f"[3]Desafio do tesouro: COMPRADO")
                        if licenças["Carteira D"] is False:
                            print(f"[4]Carteira D: R${clt_shop['Carteira D']:,.2f}")
                        else:
                            print(f"[4]Carteira D: COMPRADO")
                        if licenças['View_conts'] is False:
                            print(f"[5]Secretário(a) - Ajuda em contas: R${clt_shop['Secretário(a)']:,.2f}")
                        else:
                            print(f"[5]Secretário(a) - Ajuda em contas:: COMPRADO")

                        opcao = input("ESCOLHA UMA LICENÇA PARA COMPRAR(ENTER PARA SAIR)\n--> ")
                        if opcao == "1":
                            if licenças["Trabalho2"] is False:
                                if carteira["Bolso"] >= clt_shop["Trabalho2"]:
                                    carteira["Bolso"] -= clt_shop["Trabalho2"]
                                    licenças["Trabalho2"] = True
                                    salvar_dados("licencas", licenças)
                                    salvar_dados("carteira", carteira)
                                    input("Você comprou a licença! (ENTER)")
                                    continue
                                else:
                                    limpar()
                                    print("Você não tem dinheiro!")
                                    input("Enter para continuar")
                                    continue
                            else:
                                print("Você já comprou esta licença!")
                                input("\n(pressione ENTER para continuar)")
                                continue
                        if opcao == "2":
                            if licenças["Trabalho3"] is False:
                                if carteira["Bolso"] >= clt_shop["Trabalho3"]:
                                    carteira["Bolso"] -= clt_shop["Trabalho3"]
                                    licenças["Trabalho3"] = True
                                    salvar_dados("licencas", licenças)
                                    salvar_dados("carteira", carteira)
                                    input("Você comprou a licença! (ENTER)")
                                    continue
                                else:
                                    limpar()
                                    print("Você não tem dinheiro!")
                                    input("Enter para continuar")
                                    continue
                            else:
                                print("Você já comprou esta licença!")
                                input("\n(pressione ENTER para continuar)")
                                continue
                        if opcao == "3":
                            if licenças["Trabalho4"] is False:
                                if carteira["Bolso"] >= clt_shop["Trabalho4"]:
                                    carteira["Bolso"] -= clt_shop["Trabalho4"]
                                    licenças["Trabalho4"] = True
                                    salvar_dados("licencas", licenças)
                                    salvar_dados("carteira", carteira)
                                    input("Você comprou a licença! (ENTER)")
                                    continue
                                else:
                                    limpar()
                                    print("Você não tem dinheiro!")
                                    input("Enter para continuar")
                                    continue
                            else:
                                print("Você já comprou esta licença!")
                                input("\n(pressione ENTER para continuar)")
                                continue
                        if opcao == "4":
                            if licenças["Carteira D"] is False:
                                if carteira["Bolso"] >= clt_shop["Carteira D"]:
                                    carteira["Bolso"] -= clt_shop["Carteira D"]
                                    licenças["Carteira D"] = True
                                    salvar_dados("licencas", licenças)
                                    salvar_dados("carteira", carteira)
                                    input("Você comprou a licença! (ENTER)")
                                    continue
                                else:
                                    limpar()
                                    print("Você não tem dinheiro!")
                                    input("Enter para continuar")
                                    continue
                            else:
                                print("Você já comprou esta licença!")
                                input("\n(pressione ENTER para continuar)")
                                continue
                        if opcao == "5":
                            if licenças["View_conts"] is False:
                                if carteira["Bolso"] >= clt_shop["Secretário(a)"]:
                                    carteira["Bolso"] -= clt_shop["Secretário(a)"]
                                    licenças["View_conts"] = True
                                    salvar_dados("licencas", licenças)
                                    salvar_dados("carteira", carteira)
                                    input("Você comprou a licença! (ENTER)")
                                    continue
                                else:
                                    limpar()
                                    print("Você não tem dinheiro!")
                                    input("Enter para continuar")
                                    continue
                            else:
                                print("Você já comprou esta licença!")
                                input("\n(pressione ENTER para continuar)")
                                continue
                        
                        
                        
                        
                        else:
                            loja_clt = False
                            break
                    except (ValueError, TypeError) :
                        print("DIGITE UM NÙMERO|VOCÊ JA COMPROU ESTA LICENÇA!")
                        input("ENTER PARA CONTINUAR")
                        continue
        if escolha == "6": #Ver Carteira/Conta Banco
            ambiente = True
            while ambiente:
                if carteira["Banco"] >=0:
                    print(f"NO BANCO: R${carteira["Banco"]:,.2f}")
                else:
                    print(f"NO BANCO: R${carteira["Banco"]:,.2f} DE DÍVIDAS!")
                print(f"NA CARTEIRA: R${carteira["Bolso"]:,.2f}")
                sair = input("ENTER PARA VOLTAR")
                if sair.strip() == "":
                    ambiente = False
                    break
                sleep(2)
                limpar()
        if escolha == "1": #TRABALHOS FÁCEIS
            registrar_acao_jogador("passou_por_Trabalho1", "Acessou Trabalhos Faceis")
            trabalho = True
            while trabalho is True:
                limpar()
                A = randint(1,20)
                B = randint(1,30)
                soma = A + B
                try:
                    if not licenças['View_conts']:
                        resposta = int(input(f"Quanto é {A}+{B}?\nRESPOSTA: "))
                    else:
                        resposta = int(input(f"Quanto é {A}+{B}?\nRESPOSTA [Senhor(a), coloque {soma}]: "))
                    if resposta == soma:
                        limpar()
                        ganho = round(uniform(5.40,50.30), 2)
                        carteira["Bolso"] += ganho
                        print(f"Parabéns, você ganhou R${ganho:,.2f} em dinheiro vivo!")
                        salvar_dados("carteira", carteira)
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                        reinicio = input("Continuar? S/N:  ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break  
                    else:
                        limpar()
                        if not licenças['View_conts']:
                            print("Você errou, infelizmente.")
                        else:
                            print('Como que você errou?!')
                        reinicio = input("Continuar? S/N: ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break
                except ValueError:
                    print("digite apenas números aqui!")
        if escolha == "2": #TRABALHOS MÉDIOS
            registrar_acao_jogador("passou_por_Trabalho2", "Acessou Trabalhos Medios")
            if licenças["Trabalho2"] is True:
                pass
            else:
                print("Você não possui licença para este emprego!")
                input("ENTER PARA VOLTAR")
                continue
            trabalho = True
            while trabalho is True:
                limpar()
                A = randint(1,100)
                B = randint(1,30)
                soma = A * B
                try:
                    if not licenças['View_conts']:
                        resposta = int(input(f"Quanto é {A}X{B}?\nRESPOSTA: ").strip().replace(",","").replace(".",""))
                    else:
                        resposta = int(input(f"Quanto é {A}X{B}?\nRESPOSTA [Senhor(a) coloque {soma}]: ").strip().replace(",","").replace(".",""))
                    if resposta == soma:
                        limpar()
                        ganho = round(uniform(60.40,130.99), 2)
                        carteira["Bolso"] += ganho
                        salvar_dados("carteira", carteira)
                        print(f"Parabéns, você ganhou R${ganho:,.2f} em dinheiro vivo!")
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                        reinicio = input("Continuar? S/N:  ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break  
                    else:
                        limpar()
                        if not licenças['View_conts']:
                            print("Você errou, infelizmente.")
                        else:
                            print('Como você errou?!')
                        reinicio = input("Continuar? S/N: ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break
                except ValueError:
                    print("digite apenas números aqui!")
        if escolha == "3": #TRABALHOS DIFÍCEIS
            registrar_acao_jogador("passou_por_Trabalho3", "Acessou Trabalhos Dificeis")
            if licenças["Trabalho3"] is True:
                pass
            else:
                print("Você não possui licença para este emprego!")
                input("ENTER PARA VOLTAR")
                continue
            trabalho = True
            while trabalho is True:
                limpar()
                contas_divisao = [(100,2),(50,5),(30,2),(6,2),(9,3),
                                    (144, 12), (168, 14), (225, 15), (390, 13), (112, 7), 
                                    (135, 9), (182, 14), (252, 12), (324, 18), (448, 14), 
                                    (729, 27), (840, 24), (936, 12), (1024, 32), (625, 25)
                                ]
                conta_definida = choice(contas_divisao)
                soma = conta_definida[0]//conta_definida[1]
                try:
                    if not licenças['View_conts']:
                        resposta = int(input(f"Quanto é {conta_definida[0]} dividido por {conta_definida[1]}?\nRESPOSTA: ").strip().replace(",","").replace(".",""))
                    else:
                        resposta = int(input(f"Quanto é {conta_definida[0]} dividido por {conta_definida[1]}?\nRESPOSTA [Senhor(a) coloque {soma}]: ").strip().replace(",","").replace(".",""))
                    if resposta == soma:
                        limpar()
                        ganho = round(uniform(300.40,540.99), 2)
                        carteira["Bolso"] += ganho
                        salvar_dados("carteira", carteira)
                        print(f"Parabéns, você ganhou R${ganho:,.2f} em dinheiro vivo!")
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                        reinicio = input("Continuar? S/N:  ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break  
                    else:
                        limpar()
                        if not licenças['View_conts']:
                            print("Você errou, infelizmente.")
                        else:
                            print('Será possível?!')
                        reinicio = input("Continuar? S/N: ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break
                except ValueError:
                    print("digite apenas números aqui!")
        if escolha == "4": #Desafio do tesouro
            registrar_acao_jogador("passou_por_Trabalho4", "Acessou Desafio do Tesouro")
            if licenças["Trabalho4"] is True:
                pass
            else:
                print("Você não possui licença para este emprego!")
                input("ENTER PARA VOLTAR")
                continue
            trabalho = True
            rodada = 3
            if not rodada > 0:
                for tempo in range(50, 0, -1):
                    print(f"\rEspere até o próximo desafio começar em {tempo} segundos...", end="")
                    sys.stdout.flush()
                    sleep(1)
                    rodada = 3
                    pass
            else:
                while trabalho is True:
                    limpar()
                    bolsa = 0
                    erro = 0 
                    A = randint(1,90)
                    B = randint(1,80)
                    C = randint(1,300)
                    D = randint(1,200)
                    contas_divisao = [(100,2),(50,5),(30,2),(6,2),(9,3),
                                        (144, 12), (168, 14), (225, 15), (390, 13), (112, 7), 
                                        (135, 9), (182, 14), (252, 12), (324, 18), (448, 14), 
                                        (729, 27), (840, 24), (936, 12), (1024, 32), (625, 25)
                                    ]
                    conta_definida = choice(contas_divisao)
                    soma1 = A+B
                    soma2 = C*D
                    soma3 = conta_definida[0]//conta_definida[1]
                    print(f"RESOLVA ESTE DESAFIO EM 30 SEGUNDOS:")
                    try:
                        tempo_on = time()
                        if not licenças['View_conts']:
                            resposta_1 = int(float(input(f"Quanto é {A}+{B}?\n: ").strip().replace(",","").replace(".","")))
                        else:
                            resposta_1 = int(float(input(f"Quanto é {A}+{B}?\n[Rápido! coloque {soma1}]: ").strip().replace(",","").replace(".","")))
                        if resposta_1 == soma1:
                            ganho = round(uniform(1000.40,4000.99), 2)
                            bolsa += ganho
                            limpar()
                        else:
                            limpar()
                            erro += 1
                            input("ERRADO! (PRESSIONE ENTER)")
                            limpar()
                        if not licenças['View_conts']:
                            resposta_2 = int(input(f"Quanto é {C}X{D}?\n: ").strip().replace(",","").replace(".",""))
                        else:
                            resposta_2 = int(input(f"Quanto é {C}X{D}?\n[Rápido! coloque {soma2}]: ").strip().replace(",","").replace(".",""))
                        if resposta_2 == soma2:
                            ganho = round(uniform(2500.40,5000.99), 2)
                            bolsa += ganho
                            limpar()
                        else:
                            limpar()
                            erro += 1
                            input("ERRADO! (PRESSIONE ENTER)")
                            limpar()

                        if not licenças['View_conts']:  
                            resposta_3 = int(input(f"Quanto é {conta_definida[0]} dividido por {conta_definida[1]}?\n: ").strip().replace(",","").replace(".",""))
                        else:
                            resposta_3 = int(input(f"Quanto é {conta_definida[0]} dividido por {conta_definida[1]}?\n[Rápido! coloque {soma3}]: ").strip().replace(",","").replace(".",""))

                        if resposta_3 == soma3:
                            ganho = round(uniform(2500.40,5000.99), 2)
                            bolsa += ganho
                        else:
                            limpar()
                            erro += 1
                            input("ERRADO! (PRESSIONE ENTER)")
                        tempo_off = time()
                        tempo_total = tempo_off - tempo_on
                        if tempo_total > 30:
                                limpar()
                                print(f"TEMPO ESGOTADO! Você levou {tempo_total:.1f} segundos. Não há recompensa")
                                bolsa = 0 # Zera o ganho porque demorou demais
                                reinicio = input("Continuar? S/N: ")
                                if reinicio.strip().upper() == "S" or "":
                                    rodada -= 1
                                    continue
                                elif reinicio.strip().upper() == "N":
                                    rodada -= 1
                                    trabalho = False
                                    break
                        else:
                                print("RESULTADO")
                                if erro == 0:
                                    print("Você errou nenhuma vez!")
                                elif erro <= 2:
                                    print(f"Você errou {erro} vezes")
                                elif erro == 3:
                                    if not licenças['View_conts']:
                                        print("Você errou tudo!")
                                    else:
                                        print('É falta de atenção ou incopetência mesmo?')
                                carteira["Bolso"] += bolsa
                                salvar_dados("carteira", carteira)
                                atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                                print(f"Você ganhou R${bolsa:,.2f} em dinheiro vivo!")

                                reinicio = input("Continuar? S/N: ")
                                limpar()
                                if reinicio.strip().upper() == "S" or "":
                                    rodada -= 1
                                    continue
                                elif reinicio.strip().upper() == "N":
                                    rodada -= 1
                                    trabalho = False
                                    break
                    except ValueError:
                        print("DIGITE APENAS NÚMEROS!")
                        input("ENTER PARA CONTINUAR")             
        if escolha == "7": #Banco
            registrar_acao_jogador(None, "Acessou o Banco")
            banco = True
            while banco is True:
                try:
                    limpar()
                    verificar_notificacoes(nome)
                    print("BANDO DO BRASIL".center(40,"/"))
                    print("*Seu dinheiro rende mais, dependendo do valor guardado| Experimente nossa campanha de doação! [R]*\n[1]Depositar dinheiro               [3]Depositar Tudo \n[2]Retirar dinheiro                 [4]Retirar tudo\n[G] Investimentos Globais!")
                    if carteira["Banco"] < 0:
                        print(f"\n{VERMELHO}[Sua conta está no vermelho! Você deve R${carteira["Banco"]:,.2f} para o banco]\n[Todo valor colocado será descontado pela dívida.]{RESET}\n")
                    banco_escolha = input("Escolha uma opção| ENTER PARA SAIR\n: ").strip().upper()
                    if banco_escolha == "0408": #DEBUG
                        print("DEBUG acessado")
                        carteira["Bolso"] += 10000000000
                        input("ENTER")
                    if banco_escolha == "1": #depositar
                        print(f"Você tem R${carteira['Bolso']:,.2f} em dinheiro")
                        quantia = float(input("Quanto para colocar na conta?\n: ").replace(",", "."))
                        if round(quantia,2) <= float(carteira["Bolso"]) and quantia >=0:
                            carteira["Bolso"] = round(float(carteira["Bolso"]) - quantia, 2)
                            carteira["Banco"] = round(float(carteira["Banco"]) + quantia, 2)
                            print(f"R${quantia:,.2f} foi depositado na conta!")
                            salvar_dados("carteira", carteira)
                            input("ENTER PARA COTINUAR")
                        else:
                            limpar()
                            print(f"Você não tem esse valor: R${quantia:,.2f}")
                            input("Enter para continuar")
                    if banco_escolha == "2": #sacar
                        if carteira["Banco"] > 0:
                            print(f"Você tem R${carteira['Banco']:,.2f} na conta")
                            quantia = float(input("Quanto para retirar da conta?\n: ").replace(",", "."))
                            if round(quantia,2) <= float(carteira["Banco"]) and  quantia >0:
                                carteira["Banco"] -= round(float(quantia))
                                carteira['Bolso'] += round(float(quantia))
                                print(f"R${quantia:,.2f} foi retirado da sua conta!")
                                salvar_dados("carteira", carteira)
                                input("ENTER PARA COTINUAR")
                            else:
                                limpar()
                                print(f"Você não tem esse valor: R${quantia:,.2f}, você tem R${carteira['Banco']:,.2f}")
                                input("Enter para continuar")
                        else:
                            limpar()
                            print(f"Você não tem fundos na conta")
                            input("Enter para continuar")
                    if banco_escolha == "3": #Depositar tudo
                        valor_depositado = carteira["Bolso"]

                        carteira["Banco"] = round(carteira["Banco"] + valor_depositado, 2)
                        print(f"R${carteira["Bolso"]:,.2f} foi depositado à sua conta!")
                        
                        carteira["Bolso"] = 0
                        salvar_dados("carteira",carteira)
                        
                        sleep(1)
                        limpar()
                    if banco_escolha == "4": #Sacar tudo
                        if not carteira["Banco"] <0:
                            valor_sacado = carteira["Banco"]
                            
                            carteira["Bolso"] = round(carteira["Bolso"] + valor_sacado, 2)
                            carteira["Banco"] = 0.0
                            
                            salvar_dados("carteira", carteira)
                            
                            # Força a nuvem a registrar o saque na hora
                            
                            
                            print(f"Você sacou todo o valor de R$ {valor_sacado:,.2f}!")
                            sleep(1)
                            limpar()
                        else:
                            print("Não é possível fazer esta ação")
                            sleep(1)
                            limpar()
                    if banco_escolha == "": #SAIR
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                        banco = False
                        break
                    if banco_escolha == 'R':
                        limpar()
                        doar_dinheiro(nome)
                    if banco_escolha == 'G':
                        limpar()
                        menu_leilao_investimento(nome)


                except ValueError:
                    limpar()
                    print("Digite um valor válido")
                    sleep(2)
                    limpar()
        if escolha == "8": #Ver garagem
            registrar_acao_jogador("passou_por_garagem", "Ver a Garagem")
            ambiente = True
            while ambiente:
                print("SUA GARAGEM".center(40,"="))
                if not Garagem:
                    print("[Vazio]")
                else:
                    for p in Garagem:
                        print(f"-> {p}")    
                print("-"*40)
                saida = input("ENTER PARA SAIR")
                if saida.strip() == "":
                    break
        if escolha == "9": #ver Loja
            registrar_acao_jogador("loja_comprou_algo", "Entrou no Mercado / Loja de Itens")
            if carteira["Banco"] < 0:
                print("Pague suas dívidas antes de efetuar qualquer compra!")
                input("ENTER PARA CONTINUAR")
            else:
                ambiente = True
                while ambiente:
                    limpar()
                    print("AMERICANAS".center(40,"-"))
                    for i,(mercadoria,valor) in enumerate(mercado.items(),start = 1):
                        status = f"R${valor:,.2f}" if mercadoria not in Garagem else "[ESGOTADO]"
                        print(f"[{i}] {mercadoria}: {status}")
                    item = input("ESCOLHA UM ITEM| ENTER PARA SAIR\n-> ")
                    if item == "":
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                        ambiente = False
                        break
                    else:
                        try:    
                            indice = int(item) - 1
                            lista_mercadoria = list(mercado)
                            nome_item = lista_mercadoria[indice]
                            if 0 <= indice < len(lista_mercadoria):
                                nome_item = lista_mercadoria[indice]
                                preco = mercado[nome_item] # Pega o valor direto
                            
                                print(f"Você selecionou {nome_item} - Preço: R${preco:,.2f}")
                                confirmar = input(f"Confirmar compra de {nome_item}? S/N: ").upper()
                                if confirmar == "S":
                                    if carteira["Bolso"] >= preco:
                                        if nome_item in Garagem:
                                            print(f"Você já possui o item {nome_item}! Escolha outro.")
                                            input("ENTER PARA CONTINUAR")
                                            limpar()
                                        else:
                                            carteira["Bolso"] -= preco
                                            Garagem[nome_item] = preco
                                            salvar_dados("carteira", carteira)
                                            salvar_dados("garagem", Garagem)
                                            print("Compra realizada com sucesso!")
                                            if nome_item == "Caminhão" and licenças["Carteira D"] is False:
                                                print("Compre a licença D, na loja de licenças para poder trabalhar!!!")
                                                sleep(2)
                                            if nome_item == "Caminhão":
                                                letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                                numeros = "0123456789"
                                                default_placa_caminhao = f"{choice(letras)}{choice(letras)}{choice(letras)}-{choice(numeros)}{choice(numeros)}{choice(numeros)}{choice(numeros)}"
                                                placa_caminhao = carregar_dados("placa_caminhão", default_placa_caminhao)
                                                salvar_dados("placa_caminhão",placa_caminhao)
                                            sleep(2)
                                            limpar()
                                    else:
                                        print("Saldo insuficiente")
                                        sleep(2)
                                        limpar()
                                else:
                                    print("Compra cancelada")
                                    sleep(2)
                                    limpar()
                                    
                            else:
                                print("Número inválido! Escolha um item da lista.")
                        except (ValueError,TypeError):
                            print("VALOR INVÁLIDO")
                            sleep(2)
                            continue
        if escolha == "0": #SAIR#
            break
        if escolha == "10":#Pesca
            registrar_acao_jogador("passou_por_pesca", "Foi pescar com Barco")
            if not "Barco de pesca" in Garagem:
                print("selecione um valor válido")
                input("ENTER PARA CONTINUAR")
                continue
            else:
                if carteira["Bolso"] > 100:
                    carteira["Bolso"] -= 100
                    print("Foi descontado R$100.00 para a legalização de pesca")
                    sleep(2.6)
                    pass
                else:
                    input("Melhor trabalhar com no mínimo R$100 na conta nesta área.")
                    continue
            trabalho = True
            while trabalho:
                limpar()
                print("PESQUE PEIXES PARA VENDER|QUANTO MAIOR O PEIXE, MAIS DIFÍCIL")
                tamanhos = ("GRANDE","PEQUENO","MÉDIO","MUITO PEQUENO","ENORME")
                peixe_da_vez = []
                for a in range(3):
                    tamanhos_ok = choice(tamanhos)
                    peixe_da_vez.append(tamanhos_ok)
                    print(f"[{a + 1}] Um peixe {tamanhos_ok} apareceu!")
                a = input("ESCOLHA O PEIXE|ENTER PARA SAIR\n: ")
                if a == "":
                    atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                    trabalho = False
                    break
                idx = int(a) - 1
                alvo = peixe_da_vez[idx]
                if alvo == "ENORME":
                    chance = randint(1,5)
                    if chance == 3:
                        print("PARABÉNS VOCÊ PESCOU O PEIXE ENORME!")
                        ganho = round(uniform(600.30,1400.30), 2)
                        carteira["Bolso"] += ganho
                        salvar_dados("carteira", carteira)
                        print(f"Você ganhou R${ganho} em dinheiro vivo com essa pesca!")
                        v = input("Continuar a pesca?\nS/N: ")
                        limpar()
                        if v.strip().upper() in ["S",""]:
                            continue
                        else:
                            trabalho = False
                            break
                    else:
                        print("ESSA NÃO! ele quebrou a varinha e fugiu!")
                        perda = round(uniform(200.40,400.20),2)
                        print(f"Você teve R${perda} de perda")
                        if carteira["Bolso"] > 200.40:
                            carteira["Bolso"] -= perda
                        else:
                            print(f"Você não tem dinheiro na mão, Foi descontado de sua conta os R${perda:,.2f}.")
                            carteira["Banco"] -= perda
                        salvar_dados("carteira", carteira)
                        v = input("Continuar a pesca?\nS/N: ")
                        if v.strip().upper() in ["S",""]:
                            continue
                        else:
                            trabalho = False
                            break
                if alvo == "GRANDE":
                    chance = randint(10,30)
                    if chance >13:
                        print("PARABÉNS VOCÊ PESCOU O PEIXE GRANDE!")
                        ganho = round(uniform(250.30,400.30), 2)
                        carteira["Bolso"] += ganho
                        salvar_dados("carteira", carteira)
                        print(f"Você ganhou R${ganho} em dinheiro vivo com essa pesca!")
                        v = input("Continuar a pesca?\nS/N: ")
                        limpar()
                        if v.strip().upper() in ["S",""]:
                            continue
                        else:
                            trabalho = False
                            break
                    else:
                        print("ESSA NÃO! ele arrebentou a linha e fugiu!")
                        perda = round(uniform(150.40,300.20),2)
                        print(f"Você teve R${perda} de perda")
                        if carteira["Bolso"] > 150.40:
                            carteira["Bolso"] -= perda
                        else:
                            print(f"Você não tem dinheiro na mão, Foi descontado de sua conta os R${perda:,.2f}.")
                            carteira["Banco"] -= perda
                        salvar_dados("carteira", carteira)
                        v = input("Continuar a pesca?\nS/N: ")
                        if v.strip().upper() in ["S",""]:
                            continue
                        else:
                            trabalho = False
                            break
                if alvo == "MÉDIO":
                    chance = randint(3,35)
                    if chance >10:
                        print("PARABÉNS VOCÊ PESCOU O PEIXE MÉDIO!")
                        ganho = round(uniform(100.40,210.90), 2)
                        carteira["Bolso"] += ganho
                        salvar_dados("carteira", carteira)
                        print(f"Você ganhou R${ganho} em dinheiro vivo com essa pesca!")
                        v = input("Continuar a pesca?\nS/N: ")
                        limpar()
                        if v.strip().upper() in ["S",""]:
                            continue
                        else:
                            trabalho = False
                            break
                    else:
                        print("ESSA NÃO! ele comeu a isca e fugiu!")
                        perda = round(uniform(10.40,50.20),2)
                        print(f"Você teve R${perda}")
                        if carteira["Bolso"] > 10.40:
                            carteira["Bolso"] -= perda
                        else:
                            print(f"Você não tem dinheiro na mão, Foi descontado de sua conta os R${perda:,.2f}.")
                            carteira["Banco"] -= perda
                        salvar_dados("carteira", carteira)
                        v = input("Continuar a pesca?\nS/N: ")
                        if v.strip().upper() in["S",""]:
                            continue
                        else:
                            trabalho = False
                            break
                if alvo == "PEQUENO":
                    chance = randint(1,100)
                    if chance >20:
                        print("PARABÉNS VOCÊ PESCOU O PEIXE PEQUENO!")
                        ganho = round(uniform(60.40,110.90), 2)
                        carteira["Bolso"] += ganho
                        salvar_dados("carteira", carteira)
                        print(f"Você ganhou R${ganho} em dinheiro vivo com essa pesca!")
                        v = input("Continuar a pesca?\nS/N: ")
                        limpar()
                        if v.strip().upper() in["S",""]:
                            continue
                        else:
                            trabalho = False
                            break
                    else:
                        print("ESSA NÃO! ele comeu a isca e fugiu!")
                        perda = round(uniform(10.40,50.20),2)
                        print(f"Você teve R${perda} de perda")
                        if carteira["Bolso"] > 10.40:
                            carteira["Bolso"] -= perda
                        else:
                            print(f"Você não tem dinheiro na mão, Foi descontado de sua conta os R${perda:,.2f}.")
                            carteira["Banco"] -= perda
                        salvar_dados("carteira", carteira)
                        v = input("Continuar a pesca?\nS/N: ")
                        if v.strip().upper() in ["S",""]:
                            continue
                        else:
                            trabalho = False
                            break
                if alvo == "MUITO PEQUENO":
                    chance = randint(1,100)
                    if chance >20:
                        print("Bem.. Você consegiu pegar o peixe pequeno.. na verdade muito pequeno")
                        ganho = round(uniform(10.40,50.90), 2)
                        carteira["Bolso"] += ganho
                        salvar_dados("carteira", carteira)
                        
                        print(f"Você ganhou R${ganho} em dinheiro vivo com essa pesca!")
                        v = input("Continuar a pesca?\nS/N: ")
                        limpar()
                        if v.strip().upper() in ["S",""]:
                            continue
                        else:
                            trabalho = False
                            break
                    else:
                        print("Como ele fugiu?")
                        v = input("Continuar a pesca?\nS/N: ")
                        if v.strip().upper() in["S",""]:
                            continue
                        else:
                            trabalho = False
                            break
        if escolha == "11":#Moto
            registrar_acao_jogador("passou_por_moto_boy", "Foi fazer Moto Boy")
            if not "Moto" in Garagem:

                print("selecione um valor válido")
                input("ENTER PARA CONTINUAR")
                continue
            else:
                if carteira["Bolso"] >= 100 or carteira["Banco"] >= 100:
                    pass
                else:
                    input("Melhor trabalhar com no mínimo R$100 na conta nesta área.")
                    sleep(2)
                    continue

            trabalho = True
            while trabalho:
                limpar()
                print("TRABALHE COMO ENTREGADOR!\nVocê precisa calcular as despesas e o ganho\nMáximo 5 viagens!")
                posto = round(uniform(40.30,100.30), 2)
                situacao_mercado = []
                lucro = 0
                print("\nSituação do mercado\n")
                for _ in range(3):
                    valor = round(uniform(30.30,100.30), 2)
                    valor1 = round(uniform(30.30,100.30), 2)
                    valor2 = round(uniform(30.30,100.30), 2)
                    valor3 = round(uniform(30.30,100.30), 2)
                    valor_raro = round(uniform(80.30,120.30), 2)
                    pacote = (valor,valor1,valor2,valor3,valor_raro)
                    escolhavalor = choice(pacote)
                    situacao_mercado.append(escolhavalor)
                    print(f"Valor da entrega R${escolhavalor:,.2f}")
                print(f"\nGASOLINA POR VIAGEM R${posto:,.2f}\n")
                
                x = input("Quantas vezes gostaria de fazer a viagem?|ENTER PARA SAIR\n: ")
                if x == "":
                    atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                    trabalho = False
                    break
                else:
                    pass
                if x.isdigit():
                    x = int(x)
                else:
                    print("DIGITE NÚMEROS!")
                    input("ENTER PARA CONTINUAR")
                    limpar()
                    continue
                if not x < 6:
                    print("Você só pode fazer 5 viagens!")
                    input("ENTER PARA CONTINUAR")
                    limpar()
                else:
                    for a in range(x):
                        lucro += choice(situacao_mercado) - posto
                    carteira["Bolso"] += lucro
                    if lucro > 0:
                        print(f"Você obteve R${lucro:,.2f} de lucro!")
                        print(f"SALDO ATUAL: R${carteira["Bolso"]:,.2f}")
                        sleep(3)
                        limpar()
                        salvar_dados("carteira", carteira)
                        
                    else:
                        print(f"Você obteve R${lucro:,.2f} de PREJUÍZO!")
                        print(f"SALDO ATUAL: R${carteira["Bolso"]:,.2f}")
                        sleep(3)
                        limpar()
                        salvar_dados("carteira", carteira)
                        
                        saldo = carteira["Bolso"]
                        if saldo <=0:
                            carteira["Banco"] += lucro
                            print(f"você não possui dinheiro, foram descontados os R${lucro:,.2f} de sua conta\nSeus fundos contam: R${carteira["Banco"]:,.2f} ATUALMENTE")
                            sleep(3)
                            limpar()
                            salvar_dados("carteira", carteira)
                            
                            
                    v = input("\nContinuar a rota?\nS/N: ")
                    limpar()
                    if v.strip().upper() == "S":
                        continue
                    else:
                        trabalho = False
                        break
        if escolha == "12":#Mineração
            registrar_acao_jogador("passou_por_mineracao_picareta", "Minerou com Picareta")
            if not "Picareta" in Garagem:
                print("selecione um valor válido")
                input("ENTER PARA CONTINUAR")
                continue
            else:
                trabalho = True
                limpar()
                digitar("Você está entrando em uma caverna...")
                sleep(2)
                digitar("Cuidado")
                sleep(3)
                default_caixa = []
                caixa = carregar_dados("caixa",default_caixa)
                tentativas = 0
                while trabalho:
                    
                    tipos_D = {"Diamante pequeno": 800,"Diamante Médio": 2300,"Diamante Grande": 8900,"Diamante Negro":10000}
                    limpar()
                    print("MINERAÇÃO".center(30,"="))
                    chance_D = randint(1,100)
                    Decisao = input("ENTER para MINERAR| 0 PARA SAIR | Ver caixa [1]\n: ")
                    if Decisao == "1":
                        total = 0
                        for d in caixa:
                            D = tipos_D[d]
                            print(f"{d}: R${D:,.2f}")
                            total +=D
                        print("_"*40)
                        menu_mine = input(f"| Total: R${total:,.2f} | ENTER PARA SAIR| [1] Vender tudo |")
                        print("_"*40)
                        if menu_mine == "1":
                            if not caixa:
                                print("Não tem nada aqui,ta querendo vender o que, doido?")
                                sleep(3)
                            else:
                                carteira["Bolso"] += total
                                print(f"Você recebeu R${total:,.2f}.")
                                caixa = []
                                salvar_dados("caixa",caixa)
                                sleep(1.9)
                        else:
                            limpar()
                    else:
                        if Decisao == "0":
                            atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                            trabalho = False
                            break
                        else:
                            if tentativas < 3:
                                tentativas += 1
                                if chance_D == 5:
                                    print("Você achou um diamante Negro!")
                                    sleep(2)
                                    caixa.append("Diamante Negro")
                                    salvar_dados("caixa",caixa)
                                    limpar()
                                elif chance_D == 10:
                                    print("Você achou um diamante grande!")
                                    sleep(2)
                                    caixa.append("Diamante Grande")
                                    salvar_dados("caixa",caixa)
                                    limpar()
                                elif chance_D == 15:
                                    print("Você achou um diamante médio!")
                                    sleep(2)
                                    caixa.append("Diamante Médio")
                                    salvar_dados("caixa",caixa)
                                    limpar()                            
                                elif chance_D == 40:
                                    print("Você achou um diamante pequeno!")
                                    sleep(2)
                                    caixa.append("Diamante pequeno")
                                    salvar_dados("caixa",caixa)
                                    limpar()
                                else:
                                    print("Você achou nada aqui! Bata de novo.")
                                    sleep(2)
                                    limpar()
                            else:
                                for tempo in range(20, 0, -1):
                                    print(f"\rDescanse um pouco... Espere {tempo} segundos para recuperar o fôlego", end="")
                                    sys.stdout.flush()
                                    sleep(1)
                                tentativas = 0
                                limpar()
        if escolha == "13":#Mineração bit coin
            registrar_acao_jogador("passou_por_cripto", "Acessou Mineracao de Cripto (PC Servidor)")
            if not "PC p/ servidor" in Garagem and nome != "727":
                print("selecione um valor válido")
                input("ENTER PARA CONTINUAR")
                continue
            else:
                trabalho = True
                loja_hardware = {"GT720":900,"GTX1050":4000,"GTX1090":8000,"RTX2060":21000,"RTX3090":100000}
                default_config_pc = {"GT720 *velha*":700}
                campo_miner = {"DOGECOIN":40000,"Bitinho coin":21000,"Kryptonita":12000,"Lixo kripto":1000,"Lixo do Lixo krypto":500}
                default_carteiraKRYPTO = {"Moedas":0}
                
                config_pc = carregar_dados("config_pc",default_config_pc)
                carteiraKRYPTO = carregar_dados("Carteira Krypto",default_carteiraKRYPTO)
                salvar_dados("config_pc",config_pc)
                salvar_dados("Carteira Krypto",carteiraKRYPTO)  
                while trabalho:
                    limpar()
                    print("CRIPTO HUB".center(40,'='))

                    print("[1] CONFIGURAÇÕES DO MEU PC\n[2] LOJA DE HARDWARE\n[3] Carteira kripto")

                    pc_indx = input("ENTER PARA SAIR| ESCOLHA UMA OPÇÃO: ")
                    if pc_indx == "1":
                        ambiente = True
                        while ambiente:
                            
                            limpar()
                            print("SEU PC".center(30,"-"))
                            if not config_pc: #SE PC ESTIVER VAZIO
                                print("|NENHUM COMPONENTE|")
                                input("ENTER PARA SAIR")
                                ambiente = False
                                limpar()
                                break
                            else:
                                for i, (placa,preço) in enumerate(list(config_pc.items()),start = 1): #MOSTRAR COMPONENTES
                                    print(f"[{i}] {placa}: R${preço - 500}")
                            
                                idx = input("ENTER PARA SAIR| ESCOLHA UM COMPONENTE PRA VENDER: ")
                            if not idx.strip(): #SAIR DO CONFIG USER PC
                                ambiente = False
                                limpar()
                                break
                            try:
                                indice = int(idx) - 1
                                lista_mercadoria = list(config_pc.keys())
                                nome_item = lista_mercadoria[indice]
                                if 0 <= indice < len(lista_mercadoria):
                                    nome_item = lista_mercadoria[indice]
                                    preco = config_pc[nome_item] - 500 # Pega o valor direto
                                    
                                    print(f"Você selecionou {nome_item} - Preço: R${preco:,.2f}")
                                    confirmar = input(f"Confirmar Venda de {nome_item}? S/N: ").upper()
                                    if confirmar == "S":
                                        carteira["Bolso"] += preco
                                        salvar_dados("carteira",carteira)
                                        
                                        print(f"Você recebeu R${preco:,.2f}")
                                        sleep(2)
                                        
                                        del config_pc[nome_item]
                                        salvar_dados("config_pc",config_pc)
                                        limpar()

                                    else:
                                        print("compra cancelada.")
                                        sleep(2)
                                        limpar()
                                limpar()
                            except ValueError:
                                print("VALOR INVÁLIDO")
                                sleep(2)
                                limpar()
                                continue
                            except IndexError:
                                print("Esse Item não está mais no seu pc")
                                sleep(2)
                                limpar()
                                continue
                    if pc_indx == "2":
                        ambiente = True
                        while ambiente:
                            limpar()
                            print("PICHAU".center(40,"_"))
                            for i , (placa,valor) in enumerate(loja_hardware.items(),start=1):
                                print(f"[{i}] {placa}: R${valor:,.2f}")
                            idx = input("ENTER PARA SAIR| SELECIONE UM PRODUTO: ")
                            if not idx.strip(): #SAIR DA LOJA HARDWARE
                                ambiente = False
                                limpar()
                                break
                            try:
                                indice = int(idx) - 1
                                lista_mercadoria = list(loja_hardware.keys())
                                nome_item = lista_mercadoria[indice]
                                if 0 <= indice < len(lista_mercadoria):
                                    nome_item = lista_mercadoria[indice]
                                    preco = loja_hardware[nome_item]                   
                                    print(f"Você selecionou {nome_item} - Preço: R${preco:,.2f}")
                                    confirmar = input(f"Confirmar Compra de {nome_item}? S/N: ").upper()             
                                    if confirmar == "S":
                                        if carteira["Bolso"] >= preco:
                                            if len(config_pc) == 10:
                                                print("Você já atingiu o limite máximo de 10 placas.")
                                                print("Venda alguma placa antiga para instalar uma nova.")
                                                input("\n[ENTER] VOLTAR")
                                            else:
                                                carteira["Bolso"] -= preco
                                                contador = 1
                                                envio = f"{nome_item} #{contador}"
                                                while envio in config_pc:
                                                    contador +=1
                                                    envio = f"{nome_item} #{contador}"
                                                salvar_dados("carteira",carteira)
                                                
                                                print(f"Você colocou a {nome_item} no seu pc")
                                                config_pc[envio] = preco 
                                                salvar_dados("config_pc",config_pc)
                                                sleep(2)
                                                limpar()
                                        else:
                                            print("saldo insuficiente")
                                            sleep(2)
                                            limpar()
                                    else:
                                        print("compra cancelada")
                                        sleep(2)
                                        limpar()       
                            except ValueError:
                                print("VALOR INVÁLIDO")
                                sleep(2)
                                limpar()
                                continue
                    if pc_indx == "3":
                        while True:
                            try:
                                limpar()
                                print(" CARTEIRA KRIPTO ".center(30, "="))
                                
                                # 1. Verifica se a carteira está vazia
                                # (Soma todos os valores para ver se tem pelo menos um pouquinho de algo)
                                if sum(carteiraKRYPTO.values()) == 0:
                                    print("\nVocê ainda não possui moedas.")
                                    
                                else:
                                    # 2. Lista cada moeda e seu saldo formatado
                                    for moeda, saldo in carteiraKRYPTO.items():
                                        if saldo > 0: # Só mostra as que ele tem
                                            val = saldo * campo_miner.get(moeda, 0)
                                            print(f"• {moeda}: {saldo:.6f}| R$ {val:,.2f}") # 6 casas decimais para os fragmentos

                                print("\n" + "-"*30)
                                iv = input("\n[ENTER] Atualizar Saldo | [V] Vender Tudo | [S] Sair\n>> ").upper().strip()
                                
                                if not iv:
                                    carteiraKRYPTO = carregar_dados("Carteira Krypto", carteiraKRYPTO)
                                    continue
                                    
                                # 3. Lógica para transformar Krypto em Dinheiro (opcional)
                                if iv == "V":
                                    total_venda = 0
                                    for moeda, saldo in carteiraKRYPTO.items():
                                        valor_unidade = campo_miner.get(moeda, 0)
                                        total_venda += saldo * valor_unidade
                                    carteiraKRYPTO.clear() # Zera a carteira
                                    
                                    carteira["Bolso"] += total_venda
                                    salvar_dados("Carteira Krypto", carteiraKRYPTO)
                                    salvar_dados("carteira", carteira)
                                    
                                    
                                    print(f"\nVocê recebeu R${total_venda:,.2f}")
                                    sleep(2)
                                    limpar()
                                elif iv == "S":
                                    break
                                else:
                                    print("VALOR INVÁLIDO")
                                    sleep(2)
                                    limpar()  
                            except ValueError:
                                print("VALOR INVÁLIDO")
                                sleep(2)
                                limpar()                    
                    if pc_indx.strip() == "": #SAIR
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                        trabalho = False
                        break
        if escolha == "14":#Frete com Caminhão
            registrar_acao_jogador("passou_por_frete", "Acessou Fretes de Caminhao")
            if not "Caminhão" in Garagem and nome != "727":
                print("selecione um valor válido")
                input("ENTER PARA CONTINUAR")
                continue
            if not licenças["Carteira D"] is True:
                print("Você não possui a licença de motorista!")
                input("ENTER PARA CONTINUAR")
                continue

            else:
                if carteira["Bolso"] >= 1000 or carteira["Banco"] >= 1000:
                    pass
                else:
                    input("Melhor trabalhar com no mínimo R$1.000 na conta nesta área.")
                    sleep(2)
                    continue
                trabalho = True
                while trabalho:     
                    limpar()
                    print("SEDEX".center(30,"="))
                    distancia = ("Longa","Intermediária","Curta")
                    cargas = ("Sucata","Leite","Adubo","Garrafas vazias","Gado","Alimento","Combustível","Líquido","Lenha","Eletrodomésticos","Entregas (correios)","Veículos","Cavalos","Frutas","Trator","Turbina eólica (peça)","Produtos químicos","Laboratório móvel","Animal selvagem","Produto radioativo","Guindaste","Casa","Foguete NASA","Equipamento médico","Boing 747")
                    default_carteira_motorista = {"D":True,"F":False,"S":False,"S+":False,"S++":False,"Z":False}
                    Loja_caminhão = {"F":7000,"S":9000,"S+":14000,"S++":32000,"Z":80000}
                    carteira_motorista = carregar_dados("carteira_motorista",default_carteira_motorista)
                    default_historico_km = 0
                    historico_km = carregar_dados("Historico km",default_historico_km)
                    print(fr"""
--------------------------------------
-[1] Ver Cargas                      -        
-[2] Loja De licenças Especiais      -
-[3] Documentação                    -
-[Enter] Sair                        -
--------------------------------------""")
                    hub_caminhao = input(">>>: ")
                    if hub_caminhao == "": #Sair
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                        trabalho = False
                        break
                    if hub_caminhao == "1":
                        limpar()
                        ambiente = True
                        while ambiente:
                            multiplicadores = {"D": 1.0, "F": 2, "S": 3, "S+": 5, "S++": 8, "Z": 14.0}
                            valor_base = 500 
                            cargas_D = ("Gado","Alimento","Lenha","Entregas (correios)","Sucata","Leite","Adubo","Garrafas vazias",)
                            cargas_F = ("Combustível","Líquido","Eletrodomésticos","Frutas")
                            cargas_S = ("Veículos","Cavalos",)
                            cargas_S_plus = ("Trator","Produtos químicos","Produto radioativo","Guindaste","Casa",)
                            cargas_S_plus_plus = ("Turbina eólica (peça)","Equipamento médico","Laboratório móvel","Animal selvagem",)
                            cargas_Z = ("Boing 747","Foguete NASA")
                            perigo_licenca = {"D": 0, "F": 5, "S": 10, "S+": 15, "S++": 20, "Z": 30}
                            multiplicador_prejuizo = {"D": 1.0, "F": 2, "S": 2.5, "Z": 5.0,'S+':3.5,'S++':4.7}
                            todas_as_categorias = [
                                (cargas_D, "D"),
                                (cargas_F, "F"),
                                (cargas_S, "S"),
                                (cargas_S_plus, "S+"),
                                (cargas_S_plus_plus, "S++"),
                                (cargas_Z, "Z")
                            ]
                            fretes_possiveis = []
                            print("CARGAS".center(30,"="))

                            for tupla_cargas, letra in todas_as_categorias:
                                if carteira_motorista.get(letra) == True:
                                    for item in tupla_cargas:
                                        dist_sorteada = choice(distancia) 
                                        margem = valor_base * multiplicadores[letra]
                                        if dist_sorteada == "Longa":
                                            margem*= 3
                                        elif dist_sorteada == "Intermediária":
                                            margem *= 1.8
                                        fretes_possiveis.append((f"{item} | Rota {dist_sorteada}", margem, letra)) 
                            opcoes_disponiveis = sample(fretes_possiveis, k=min(5, len(fretes_possiveis)))

                            
                            for i, (carga,valor, letra) in enumerate(opcoes_disponiveis, start=1):
                                print(f"[{i}] {carga} | R${valor:,.2f} |categoria: {letra} ")
                            try:
                                viagem_op = input("ENTER PARA SAIR\n>>> ")
                                if viagem_op.strip() == "":
                                    ambiente = False
                                    break

                                if viagem_op.isdigit():
                                    index = int(viagem_op) - 1
                                    if 0 <= index < len(opcoes_disponiveis):
                                        carga_escolhida, pagamento_final, letra_cargo = opcoes_disponiveis[index]
                                        bonus_risco = perigo_licenca.get(letra_cargo, 0) 
                                        fator = multiplicador_prejuizo.get(letra_cargo, 1.0)
                                        print(f"Carga selecionada: {carga_escolhida}")
                                        sleep(2)
                                        limpar()
                                        prejuízo = 0
                                        if "Longa" in carga_escolhida:
                                            tempo_viagem = 60
                                            km_aleatorio = randint(30,250)
                                            historico_km += km_aleatorio
                                            salvar_dados("Historico km",historico_km)
                                        elif "Intermediária" in carga_escolhida:
                                            km_aleatorio = randint(12,50)
                                            historico_km += km_aleatorio
                                            salvar_dados("Historico km",historico_km)
                                            tempo_viagem = 30
                                        else:
                                            km_aleatorio = randint(4,10)
                                            historico_km += km_aleatorio
                                            salvar_dados("Historico km",historico_km)
                                            tempo_viagem = 20
                                        print("Direção".center(30,"-"))
                                        
                                        print("Como irá conduzir?\n[1] Normal - risco moderado e pagamento normal\n[2] Rápido - Alto risco e Bônus no pagamento (caso dê certo)\n[3] Lento - baixo risco e desconto de 10% no pagamento\nENTER para cancelar")
                                        velocidade = input(">>> ").strip().upper()
                                        if velocidade == "1":
                                            risco = randint(1,100)
                                            barra_viagem(tempo_viagem)
                                            sleep(1)
                                            if risco >(52 - bonus_risco):
                                                prejuízo = round(uniform(600.40,900.99)* fator, 2)
                                                pagamento_final -= prejuízo
                                                print(f"\n[Houve dano na carga, isso será descontado no seu pagamento no valor de R${prejuízo:,.2f}]")
                                                
                                                sleep(5)
                                                limpar()
                                            else:
                                                pass
                                        elif velocidade == "2":
                                            risco = randint(1,100)
                                            barra_viagem(tempo_viagem/2)
                                            sleep(1)
                                            if risco >(33 - bonus_risco):
                                                prejuízo = round(uniform(1900.40,2900.99)* fator, 2)
                                                pagamento_final -= prejuízo
                                                print(f"\n[Houve choque da carga com um obstáculo, isso será descontado no seu pagamento no valor de R${prejuízo:,.2f}]")
                                                
                                                sleep(5)
                                                limpar()
                                            else:
                                                bonus = pagamento_final * 0.6
                                                pagamento_final += bonus
                                                print(f"\n[Você chegou rápido e inteiro, o bonûs foi de R${bonus:,.2f}]")
                                                sleep(3)
                                                limpar()
                                                pass
                                        elif velocidade == "3":
                                            risco = randint(1,100)
                                            barra_viagem(tempo_viagem*2)
                                            sleep(1)
                                            desconto_no_pagamento = (pagamento_final * 0.1 )
                                            pagamento_final *= 0.9 
                                            limpar()
                                            print(f"\nVocê decidiu ir mais lento, o desconto dos 10% foram de R${desconto_no_pagamento:,.2f}")
                                            sleep(4)
                                            limpar()
                                            if risco >(92-bonus_risco):
                                                prejuízo = round(uniform(440.40,1100.99)* fator, 2)
                                                pagamento_final -= prejuízo
                                                print(f"\n[Houve um arranhão na carga, isso será descontado no seu pagamento no valor de R${prejuízo:,.2f}]")
                                                
                                                sleep(5)
                                                limpar()
                                                
                                            else:
                                                pass
                                        elif velocidade == "":
                                            limpar()
                                            continue
                                        else:
                                            raise ValueError
                                        sleep(2)
                                        limpar()
                                        print("GANHOS".center(30,"-"))
                                        if pagamento_final > 0:
                                            if not prejuízo > 0:
                                                print(f"Entrega feita com sucesso, você recebeu R${pagamento_final:,.2f}")

                                            else:
                                                print(f"Entrega feita com turbulência, você recebeu R${pagamento_final:,.2f}, mas com R${prejuízo:,.2f} de prejuízo...")
                                            carteira["Bolso"] += pagamento_final
                                            salvar_dados("carteira",carteira)
                                            
                                        else:
                                            print(f"Entrega fracassada, houve apenas R${pagamento_final:,.2f} de PREJUÍZO")
                                            if carteira["Bolso"] >= pagamento_final:
                                                carteira["Bolso"] += pagamento_final
                                                salvar_dados("carteira",carteira)
                                                
                                            else:
                                                print("Você não tem saldo na carteira para ser tirado\nEntão o prejuízo foi descontado da sua conta bancária!")
                                                carteira["Banco"] += pagamento_final
                                                salvar_dados("carteira",carteira)
                                                
                                        final = input("\nS-para sair|ENTER-voltar ao menu de cargas\n>>> ")
                                        if final.strip().upper() == "S":
                                            ambiente = False
                                            break
                                        else:
                                            limpar()
                                            continue
                                    else:
                                        print("selecione um valor válido")
                                        sleep(2)
                                        limpar()    
                                else:
                                    print("selecione um valor válido")
                                    sleep(2)
                                    limpar()
                                    continue        
                            except (ValueError,IndexError,UnicodeDecodeError,Exception):
                                print("Erro de escolha")
                                sleep(2)
                                limpar()
                                continue

                    if hub_caminhao == "2":
                        ambiente = True
                        while ambiente:
                            limpar()
                            print("CARTEIRAS ESPECIAS".center(30,"_"))
                            for i , (licença,valor) in enumerate(Loja_caminhão.items(),start=1):
                                status = f"R${valor:,.2f}" if carteira_motorista.get(licença) != True else "[COMPRADO]"
                                print(f"[{i}] |{licença}: {status}")
                            compra = input("ENTER PARA SAIR\n>>> ")
                            if compra == "": #SAIR
                                ambiente = False
                                break
                            if compra.isdigit():
                                opcoes = list(Loja_caminhão.keys())
                                index = int(compra) - 1
                                if 0 <= index < len(opcoes):
                                    licenca_escolhida = opcoes[index]
                                    preco = Loja_caminhão[licenca_escolhida]
                                    if carteira_motorista[licenca_escolhida] == True:
                                        print("Você já possui está licença.")
                                        sleep(2)
                                        limpar()
                                    elif carteira["Bolso"] >= preco:
                                        carteira["Bolso"] -= preco
                                        carteira_motorista[licenca_escolhida] = True
                                        print("Compra realizada!")
                                        salvar_dados("carteira",carteira)
                                        
                                        salvar_dados("carteira_motorista",carteira_motorista)

                    if hub_caminhao == "3":
                        ambiente = True
                        
                        licencas_atuais = " ".join([f"[{letra}]" for letra, possui in carteira_motorista.items() if possui])
                        while ambiente:
                            limpar()
                            if historico_km >= 99999999:
                                historico_km = 0
                                salvar_dados("Historico km",historico_km)
# Largura total de 45 caracteres internos + 2 barras = 47
                            print(" _______________________________________________ ")
                            print("|                                               |")
                            print(f"| Motorista: {nome:<34.34} |")
                            print(f"| Placa do veículo: {placa_caminhao:<27} |")
                            print(f"| Licenças: {licencas_atuais:<34}  |")
                            print(f"| Quilômetros rodados : KM {historico_km:<20} |")
                            print("|                                               |")
                            print(f"|                © BRASIL RODOVIÁRIO            |") 
                            print("|                                               |")
                            print(" ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯  ")
                            sair_doc = input("ENTER PARA SAIR")
                            if sair_doc.strip() == "":
                                ambiente = False
                                limpar()
                                break
        if escolha == "15":# Telefone commodit
            registrar_acao_jogador("passou_por_bolsa", "Acessou Bolsa de Commodities (Telefone)")
            if not "Telefone" in Garagem and nome != "727":
                print("selecione um valor válido")
                input("ENTER PARA CONTINUAR")
                continue
            else:


                default_estoque_agro = {"Petroleo": 0, "Minerio": 0, "Soja": 0, "Algodao": 0, "Feno": 0}
                estoque_agro = carregar_dados("estoque agro",default_estoque_agro)
                default_historico_precos = {"Petroleo": 0.0, "Minerio": 0.0, "Soja": 0.0, "Algodao": 0.0, "Feno": 0.0}
                historico_precos = carregar_dados("Historico preços", default_historico_precos)



                trabalho = True
                while trabalho:
                    limpar()
                    print(f"{'--- BOLSA DE COMMODITIES ---':^40}")
                    print(f"NOTÍCIA: {evento_atual}".center(40,"="))
                    print()
                    print(f"{'PRODUTO':<15} | {'PREÇO':<10} | {'ESTOQUE':<10}")
                    print("-" * 30)
                    for i , (item,valor) in enumerate(precos.items(), start=1):
                        qtd = estoque_agro.get(item, 0)
                        p_pago = historico_precos.get(item, 0)
                        p_exibir = f"R$ {p_pago:,.2f}" if qtd > 0 else "---"
                        print(f"[{i}] {item:<15} | R$ {valor:<10.2f} | {qtd:<5} un (Pago: R${p_exibir})")
                    print("-" * 50)
                    print("DICA: aperte/segure [ENTER] para atualizar ou manter atualizado a info. dos preços.\n")
                    tel = input("S - Sair | C - Comprar | V/VT - Vender/Vender Tudo: ").lower()
                    if tel == "s":
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                        trabalho = False
                        break
                    if tel == "c":
                        try:
                            num = int(input("Digite o número do produto: "))
                            limpar()
                            # Transforma o número de volta no nome da commodity
                            lista_nomes = list(precos.keys())
                            alvo = lista_nomes[num - 1] 
                            
                            qtd = int(input(f"Quanto de {alvo} deseja comprar?\n>>>  "))
                            if qtd <= 0: raise ValueError
                            custo_total = qtd * precos[alvo]
                            telbuy = input(f"O valor é R${custo_total:,.2f}, deseja comprar?\nS/N >>> ").upper()
                            if telbuy == "S":
                                if carteira["Bolso"] >= custo_total:
                                    carteira["Bolso"] -= custo_total
                                    estoque_agro[alvo] += qtd
                                    historico_precos[alvo] = precos[alvo]
                                    salvar_dados("carteira",carteira)
                                    
                                    
                                    salvar_dados("estoque agro",estoque_agro)
                                    salvar_dados("Historico preços", historico_precos)
                                    print(f"Você comprou {qtd} de {alvo}")
                                    sleep(2)
                                    limpar()
                                else:
                                    print("Você não tem dinheiro")
                                    sleep(2)
                                    limpar()
                            else:
                                limpar()
                                continue
                        except (ValueError,IndexError):
                            print("VALOR INVÁLIDO")
                            sleep(2)
                            limpar()
                            continue
                    if tel == "v":
                        try:
                            num = int(input("Digite o número do produto para vender: "))
                            limpar()
                            lista_nomes = list(precos.keys())
                            alvo = lista_nomes[num - 1]

                            qtd_venda = int(input(f"Quanto de {alvo} deseja vender? (Você tem {estoque_agro[alvo]} un)\n>>> "))
                            
                            if qtd_venda <= 0: raise ValueError
                            
                            if estoque_agro[alvo] >= qtd_venda:
                                valor_venda = qtd_venda * precos[alvo]
                                
                                # Processando a venda
                                carteira["Bolso"] += valor_venda
                                estoque_agro[alvo] -= qtd_venda
                                if estoque_agro[alvo] == 0 : historico_precos[alvo] = 0
                                # Salvando os dados (usando suas funções)
                                salvar_dados("Historico preços", historico_precos)
                                salvar_dados("carteira", carteira)
                                
                                salvar_dados("estoque agro", estoque_agro)
                                
                                print(f"Você vendeu {qtd_venda} de {alvo} por R$ {valor_venda:,.2f}")
                                sleep(2)
                                limpar()
                            else:
                                print("Você não tem estoque suficiente!")
                                sleep(2)
                                limpar()
                        except (ValueError, IndexError):
                            print("VALOR INVÁLIDO")
                            sleep(2)
                            limpar()
                            continue
                    if tel == "vt":
                        limpar()
                        print("🚨 LIQUIDANDO TODO O ESTOQUE... 🚨\n")
                        total_geral_venda = 0
                        
                        # O 'for' percorre cada item que o jogador tem no estoque
                        for item, qtd in estoque_agro.items():
                            if qtd > 0:
                                valor_item = qtd * precos[item]
                                total_geral_venda += valor_item
                                estoque_agro[item] = 0 # Zera o item no estoque
                                historico_precos[item] = 0
                                # Salvando os dados (usando suas funções)
                                
                        if total_geral_venda > 0:
                            carteira["Bolso"] += total_geral_venda
                            
                            # Salva a nova realidade
                            salvar_dados("carteira", carteira)
                            
                            salvar_dados("estoque agro", estoque_agro)
                            salvar_dados("Historico preços", historico_precos)
                            print(f"💰 SUCESSO! Tudo foi vendido.")
                            print(f"Total recebido: R$ {total_geral_venda:,.2f}")
                        else:
                            print("Você não tem nada em estoque para vender!")
                            
                        sleep(3)
                        limpar()
        if escolha == "16":# Bike boy
            registrar_acao_jogador("passou_por_bike_boy", "Foi fazer Bike Boy")
            if not "Bicicleta" in Garagem and nome != 727:

                print("selecione um valor válido")
                input("ENTER PARA CONTINUAR")
                continue
            else:
                trabalho = True
                while trabalho:
                    limpar()
                    print("TRABALHE COMO ENTREGADOR!\nEvite a fadiga")
                    default_fadiga = 100
                    fadiga = carregar_dados("fadiga",default_fadiga)
                    situacao_mercado = []
                    lucro = 0
                    print(f"\nSituação do mercado                               fadiga: {fadiga}\n")
                    for _ in range(1,6):
                        distanciaB = (80,30,20,15,4,3,2,1)
                        valor = round(uniform(10.30,40.30), 2)
                        valor1 = round(uniform(10.30,40.30), 2)
                        valor2 = round(uniform(10.30,40.30), 2)
                        valor3 = round(uniform(10.30,40.30), 2)
                        valor_raro = round(uniform(40.30,100.30), 2)
                        pacote = (valor,valor1,valor2,valor3,valor_raro)
                        escolhavalor = choice(pacote)
                        escolhadistancia = choice(distanciaB)
                        situacao_mercado.append((escolhavalor, escolhadistancia))
                        print(f"[{_}] Valor da entrega R${escolhavalor:,.2f} KM:{escolhadistancia}")
                    
                    
                    x = input("Qual viagem gostaria de fazer?|ENTER PARA SAIR| D para descansar\n>>>: ").strip().upper()
                    if x == "": #SAIR
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar,bandeira['empresa'],nome_empresa)
                        trabalho = False
                        break
                    else: #SAIR COMP    
                        pass
                    if x == "D":
                        try:
                            limpar()
                            descanso = int(input(f"Quanto quer descansar?| fadiga atual: {fadiga}\n>>> "))
                            fadiga += descanso
                            tempo_espera = descanso * 1.5
                            if descanso >= 70:
                                tempo_espera = descanso * 0.5
                            
                            barra_viagem(tempo_espera)
                            limpar()
                            if fadiga > 100:
                                fadiga = 100
                                print("Você está totalmente descansado!")
                                sleep(2)
                                continue

                            salvar_dados("fadiga", fadiga)
                            print(f"Fadiga atualizada para: {fadiga}")
                            truto =input("\n[ENTER PARA VOLTAR]")
                            if truto:
                                limpar()
                                continue
                        except ValueError:
                            limpar()
                            print("Digite um número inteiro válido!")  
                            sleep(2)
                            limpar()   
                    if x.isdigit():
                        x = int(x)
                        if 1 <= x <= len(situacao_mercado):
                            escolha = situacao_mercado[x - 1]
                            valor_final = escolha[0]
                            km_final = escolha[1]
                            custo_fadiga = km_final * 1
                            passagem = input(f"Você selecionou a corrida {x}\nValor R${valor_final:,.2f} | {km_final} KM\n Continuar S/N >>> ").upper().strip()
                            if passagem == "N":
                                continue
                            else:
                                limpar()
                                tempo_viagem = km_final * 1.5
                                barra_viagem(tempo_viagem)
                                if fadiga >= custo_fadiga:
                                    # Caso tenha fadiga suficiente
                                    fadiga -= custo_fadiga
                                    
                                    carteira["Bolso"] += valor_final
                                    print(f"\nViagem tranquila! Fadiga restante: {fadiga}\nR${valor_final:,.2f} Ganho!")
                                else:
                                    deficit = custo_fadiga - fadiga
                                    fadiga = 0
                                    multa = valor_final * 0.7 
                                    valor_ganho = valor_final - multa
                                    valor_ganho_falso_positivo = abs(valor_ganho)
                                    if valor_ganho_falso_positivo > carteira["Bolso"]:
                                        print(f"\nVocê não possui dinheiro para multa, aplicamos ela em sua conta. No valor de R${valor_ganho:,.2f}")
                                        carteira["Banco"] -= valor_ganho
                                    else:
                                        carteira["Bolso"] -= valor_ganho
                                    print(f"\nVOCÊ EXAUSTOU! Faltou {deficit} de energia.")
                                    print(f"Multa por cansaço: R${multa:,.2f} - Valor da entrega: R${valor_final:,.2f} = R${valor_ganho:,.2f}")
                                    salvar_dados("carteira",carteira)
                                    
                                
                                salvar_dados("fadiga", fadiga)
                                v = input("\nContinuar a rota?\nS/N: ").upper().strip()
                                limpar()
                                if v.strip().upper() == "S" or "":
                                        continue
                                else:
                                        trabalho = False
                                        break
                        else:
                            print("OPÇÃO INVÁLIDA!")
                            continue
                    else:
                        print("DIGITE NÚMEROS!")
                        input("ENTER PARA CONTINUAR")
                        limpar()
                        continue
        if escolha == '17':#corrida de rua
            registrar_acao_jogador("passou_por_Corrida_de_rua", "Foi Correr com carro na rua")
            if not "Carro" in Garagem and nome != 727:
                print("selecione um valor válido")
                input("ENTER PARA CONTINUAR")
                continue
            else:
                car_rua = True
                while car_rua:
                    limpar()
                    fama_default = 0
                    fama = carregar_dados('fama', fama_default)
                    carro_atual = carregar_dados('carro_atual', 'Carro comum')
                    
                    # Converte o dicionário do save em objeto da classe car automaticamente
                    if isinstance(carro_atual, dict):
                        carro_atual = car(carro_atual)
                        nome_exibir_carro = carro_atual.modelo_carro
                        potencia_exibir = carro_atual.potencia_carro
                        limite_carro = carro_atual.limite_tuning
                        nitro = carro_atual.tem_nitro
                    else:
                        nome_exibir_carro = "Carro comum"
                        potencia_exibir = 0 
                        limite_carro = 0 
                        nitro = False

                        
                    limpar()
                    print('Necessidade de velocidade'.center(90, ':'))
                    print(f''' 
                [1] Fazer Corridas                  Carro atual: {nome_exibir_carro}
                [2] Oficina                         Potência: {potencia_exibir:.0f} / {limite_carro} 
                [3] Acelerar na pista               Fama: {fama if fama < 1000 else "1000 MAX"}
                [4] Garagem de Carros de rua
                [5] Comprar Carros de rua''')
                    if carteira['Bolso'] < 0 or carteira['Banco'] < 0:
                        print('\nSuas perdas se tornaram dívidas pense em parar de correr.')
                    NFS = input('>>>: ').strip().upper()
                    if NFS == '':
                        car_rua = False
                        limpar()
                        break
                    if NFS == '1': #fazer corrida
                        if nome_exibir_carro == 'Carro comum':
                            print('A plateia e os corredores riram da sua cara quando viram você chegando\ncom seu carrinho de empresário...')
                            sleep(2)
                            limpar()
                        else:
                            limpar()
                            base_distancia = 20
                            corrida_da_vez = [] 
                            
                            oponentes_faceis = [('Fiat Uno Mile', 75, 'Vermelho', 150), ('VW Gol Quadrado', 85, 'Vermelho', 160), ('Chevrolet Celta', 70, 'Vermelho', 140), ('Ford Ka Barata', 65, 'Vermelho', 130), ('Renault Clio', 72, 'Vermelho', 145), ('Fiat Palio 1.0', 73, 'Vermelho', 145), ('Peugeot 206', 78, 'Vermelho', 155), ('Chevrolet Corsa', 71, 'Vermelho', 140), ('VW Fox Idoso', 80, 'Vermelho', 150), ('Ford Fiesta', 74, 'Vermelho', 148), ('Fiat Mob', 72, 'Vermelho', 140), ('Renault Kwid', 68, 'Vermelho', 135), ('VW Up!', 82, 'Vermelho', 165), ('Chevrolet Prisma', 80, 'Vermelho', 155), ('Hyundai HB20 1.0', 80, 'Vermelho', 160), ('Toyota Etios', 84, 'Vermelho', 165), ('Nissan March', 77, 'Vermelho', 155), ('Fiat Siena', 75, 'Vermelho', 150), ('Chevrolet Kadett', 90, 'Vermelho', 170), ('Ford Escort', 86, 'Vermelho', 165)]
                            oponentes_medios = [('VW Gol G5 1.6', 104, 'Vermelho', 220), ('Fiat Uno Turbo', 118, 'Vermelho', 240), ('Chevrolet Astra', 121, 'Vermelho', 230), ('Ford Focus 1.6', 115, 'Vermelho', 225), ('Honda Civic 2000', 106, 'Vermelho', 210), ('Toyota Corolla Vovô', 110, 'Vermelho', 215), ('VW Santana', 114, 'Vermelho', 220), ('Chevrolet Vectra', 130, 'Vermelho', 250), ('Fiat Stilo', 122, 'Vermelho', 240), ('Renault Sandero RS', 150, 'Vermelho', 260), ('Suzuki Swift', 102, 'Vermelho', 200), ('Hyundai i30', 145, 'Vermelho', 255), ('Kia Cerato', 126, 'Vermelho', 235), ('Ford EcoSport', 110, 'Vermelho', 210), ('VW Polo 1.6', 104, 'Vermelho', 220), ('Chevrolet Onix Turbo', 116, 'Vermelho', 230), ('Fiat Cronos 1.8', 139, 'Vermelho', 250), ('Nissan Versa', 114, 'Vermelho', 220), ('Peugeot 208 Turbo', 130, 'Vermelho', 245), ('Citroen C3 Tendance', 115, 'Vermelho', 225)]
                            oponentes_dificeis = [('VW Golf GTI', 230, 'Vermelho', 400), ('Honda Civic Si', 192, 'Vermelho', 360), ('Chevrolet Cruze Turbo', 153, 'Vermelho', 300), ('Audi A3 Sportback', 180, 'Vermelho', 350), ('BMW 320i', 184, 'Vermelho', 360), ('Mercedes A200', 163, 'Vermelho', 320), ('Ford Fusion Ecoboost', 248, 'Vermelho', 420), ('Hyundai Azera', 265, 'Vermelho', 440), ('VW Jetta TSI', 211, 'Vermelho', 390), ('Volvo V40 T5', 254, 'Vermelho', 450), ('Mini Cooper S', 192, 'Vermelho', 350), ('Subaru Impreza WRX', 270, 'Vermelho', 480), ('Mitsubishi Lancer GT', 160, 'Vermelho', 310), ('Chevrolet Omega Fittipaldi', 292, 'Vermelho', 500), ('VW Passat TSI', 220, 'Vermelho', 400), ('Fiat Marea Turbo', 182, 'Vermelho', 380), ('Ford Maverick V8', 197, 'Vermelho', 350), ('Chevrolet Opala 6cc', 171, 'Vermelho', 340), ('Audi Q3 Turbo', 150, 'Vermelho', 300), ('Peugeot 308 THP', 165, 'Vermelho', 320)]
                            oponentes_chefes = [('Chevrolet Camaro SS', 461, 'Vermelho', 700), ('Ford Mustang GT', 466, 'Vermelho', 710), ('Porsche 911 Carrera', 385, 'Vermelho', 650), ('Nissan GT-R Godzilla', 572, 'Vermelho', 900), ('Toyota Supra MK4', 326, 'Vermelho', 800), ('Mazda RX-7', 276, 'Vermelho', 600), ('Audi R8 V10', 610, 'Vermelho', 950), ('Ferrari 488 GTB', 670, 'Vermelho', 990), ('Lamborghini Huracan', 610, 'Vermelho', 950), ('Dodge Challenger SRT', 717, 'Vermelho', 999), ('BMW M5', 600, 'Vermelho', 920), ('Mercedes-AMG C63', 510, 'Vermelho', 850), ('Chevrolet Corvette C8', 502, 'Vermelho', 820), ('Aston Martin Vantage', 510, 'Vermelho', 830), ('Jaguar F-Type R', 575, 'Vermelho', 890), ('McLaren 720S', 720, 'Vermelho', 999), ('Honda NSX', 581, 'Vermelho', 880), ('Subaru WRX STI', 310, 'Vermelho', 550), ('Mitsubishi Lancer Evo X', 295, 'Vermelho', 540), ('Tesla Model S Plaid', 1020, 'Vermelho', 1500)]

                            if fama < 30:
                                oponente = oponentes_faceis
                            elif fama < 60:
                                oponente = oponentes_medios
                            elif fama < 150:
                                oponente = oponentes_dificeis
                            else:
                                oponente = oponentes_chefes

                            q = 100
                            for _ in range(5):
                                op = choice(oponente)
                                rival = car(op)

                                x = randint(1,8)
                                base_premio = q + (rival.potencia_carro * 5)
                                valor_corridas = randint(base_premio, base_premio + (fama * x * 10))
                                
                                distancia_corrida = max(5, (base_distancia * fama) - randint(1, max(2, 4 * fama)))
                                
                                
                                print(f'[{_ + 1}] Oponente| {rival.modelo_carro}| {rival.potencia_carro} cv | Distância: {distancia_corrida} KM | Prêmio: R${valor_corridas:,.2f}')
                                valores_corriadas = [rival, distancia_corrida, valor_corridas]
                                corrida_da_vez.append(valores_corriadas)
                                
                            run = input('[ENTER PARA SAIR]\n>>>: ').strip().upper()
                            if run == '':
                                limpar()
                            elif run.isdigit():
                                idx = int(run) - 1
                                if 0 <= idx < len(corrida_da_vez):
                                    CARRO_INIMIGO, KM, DINHEIRO = corrida_da_vez[idx]
                                    CHEGADA = carro_atual.corrida(CARRO_INIMIGO, KM)
                                    if CHEGADA == 'V':
                                        print(f'Você ganhou R${DINHEIRO:,.2f} na conta')
                                        carteira['Bolso'] += DINHEIRO
                                        fama += int(5  + (CARRO_INIMIGO.potencia_carro // 10))
                                        salvar_dados('carteira', carteira)
                                        
                                        salvar_dados('fama', fama)
                                        sleep(2)
                                        limpar()
                                    elif CHEGADA == 'D':
                                        print(f'Você perdeu R${DINHEIRO:,.2f} da sua conta')
                                        carteira['Banco'] -= DINHEIRO
                                        fama -= int(5  + (CARRO_INIMIGO.potencia_carro // 10))
                                        salvar_dados('carteira', carteira)
                                        
                                        salvar_dados('fama', fama)
                                        sleep(2)
                                        limpar()
                                    else:
                                        bobice = DINHEIRO // 2
                                        print(f'Deu empate, você ganha metade do valor\nseus ganhos foram de R${bobice:,.2f}')
                                        carteira['Bolso'] += bobice
                                        fama += int(5  + (CARRO_INIMIGO.potencia_carro // 20))
                                        salvar_dados('carteira', carteira)
                                        
                                        salvar_dados('fama', fama)
                                        sleep(2)
                                        limpar()                                      
                    if NFS == '2':
                        if nome_exibir_carro == 'Carro comum':
                            print('Você não pode Tunar um carro de empresário!')
                            sleep(2)
                            continue
                        else:
                            limpar()
                            print(f'''
                [1] Melhorar motor  Carro atual: {carro_atual.modelo_carro} | {carro_atual.potencia_carro:.0f}/{carro_atual.limite_tuning} cavalos
                [2] Comprar Nitro   Nitro: {'Nitro Instalado' if carro_atual.tem_nitro else 'Sem Nitro'}
                ''')
                            Of = input('>>>: ').strip()
                            if Of == '1':
                                tun = carro_atual.tunar(carteira['Bolso'])
                                if tun['C'] == True:
                                    carteira['Bolso'] -= tun['$']
                                    salvar_dados('carteira', carteira)
                                    

                                    salvar_dados('carro_atual', carro_atual.__dict__)
                                    Sua_Garagem = carregar_dados('NFS', {})
                                    Sua_Garagem[carro_atual.modelo_carro] = carro_atual.__dict__
                                    salvar_dados('NFS', Sua_Garagem)
                                    sleep(2)
                                    continue
                                else:
                                    sleep(2)
                                    continue
                            if Of == '2':
                                tun = carro_atual.comprarNITRO(carteira['Bolso'])
                                if tun['C'] == True:
                                    carteira['Bolso'] -= tun['$']
                                    salvar_dados('carteira', carteira)
                                    

                                    salvar_dados('carro_atual', carro_atual.__dict__)
                                    Sua_Garagem = carregar_dados('NFS', {})
                                    Sua_Garagem[carro_atual.modelo_carro] = carro_atual.__dict__
                                    salvar_dados('NFS', Sua_Garagem)
                                    sleep(2)
                                    continue
                                else:
                                    sleep(2)
                                    continue
                    if NFS == '3':
                        if nome_exibir_carro == 'Carro comum':
                            print('Você não pode utilizar um carro de empresário')
                            sleep(2)
                            continue
                        else:
                            try:
                                dist = int(input('Quantos KM irá correr?\n>>>:'))
                                carro_atual.acelerar(dist)
                                input('[ENTER]')
                                continue
                            except ValueError:
                                print('Valor inválido')
                                sleep(2)
                                continue
                    if NFS == '4':
                        limpar()
                        print('GARAGEM'.center(90, '-'))
                        Garagem_carros = carregar_dados('NFS', 'Nenhum carro na garagem')
                        if Garagem_carros == 'Nenhum carro na garagem' or not Garagem_carros:
                            print('Nenhum carro na garagem')
                            input('\n[ENTER PARA VOLTAR]')
                        else:
                            for i, (carro_nome, dados) in enumerate(Garagem_carros.items(), start=1):
                                print(f"[{i}] {carro_nome} | {dados['potencia_carro']:.0f}/{dados['limite_tuning']} cavalos | {dados['cor_carro']}")
                            esc_car = input('>>>: ')
                            if esc_car == '':
                                continue
                            if esc_car.isdigit():
                                try:
                                    idx = int(esc_car) - 1
                                    lista_nomes_garagem = list(Garagem_carros.keys())
                                    if 0 <= idx < len(lista_nomes_garagem):
                                        nome_do_escolhido = lista_nomes_garagem[idx]
                                        carro_atual_dit = Garagem_carros[nome_do_escolhido]
                                        carro_atual = car(carro_atual_dit)
                                        salvar_dados('carro_atual', carro_atual.__dict__)
                                        print(f"Agora você está pilotando | {carro_atual.modelo_carro}!")
                                        sleep(1.5)
                                    else:
                                        print('Opção inválida')
                                        sleep(2)
                                except (ValueError, TypeError, IndexError):
                                    print('Valor inválido')
                                    sleep(2)
                                    continue
                    if NFS == '5':
                        limpar()
                        print('Concessionária das ruas'.center(90, '='))
                        concessionaria = [
                            ('VW GOL QUADRADO', 85, 'Preto', 160),
                            ('FIAT UNO TURBO', 93, 'Preto', 240),
                            ('RENAULT SANDERO RS', 150, 'Preto', 260),
                            ('HONDA CIVIC SI', 192, 'Preto', 360),
                            ('VW JETTA TSI', 211, 'Preto', 390),
                            ('FORD MUSTANG GT', 466, 'Preto', 710),
                            ('NISSAN GT-R GODZILLA', 572, 'Preto', 900),
                            ('LAMBORGHINI VENENO', 700, 'Preto', 1400),
                            ('MCLAREN SENNA', 799, 'Preto', 1800)]
                        precos_concessionaria = [
                            45000,
                            95000,
                            180000,
                            320000,
                            550000,
                            1200000,
                            3500000,
                            8500000,
                            15000000]
                        
                        Sua_Garagem_Carros = carregar_dados('NFS', {})
                        # Garante que a garagem seja um dicionário limpo caso venha como texto/tupla default
                        if isinstance(Sua_Garagem_Carros, (tuple, str)):
                            Sua_Garagem_Carros = {}

                        for i, (carro_loja, potencia, cor, limite) in enumerate(concessionaria, start=1):
                            if carro_loja in Sua_Garagem_Carros:
                                status_preco = "[COMPRADO]"
                            else:
                                preço_exibir = precos_concessionaria[i - 1]
                                status_preco = f"R${preço_exibir:,.2f}"
                            
                            # Mostra o status correto de preço ou se já está comprado
                            print(f'[{i}] {carro_loja} | {potencia}/{limite} cavalos | {status_preco}')

                        print('\n[ENTER PARA VOLTAR]')
                        loja_escolha = input('Escolha o número do carro para comprar >>>: ').strip()
                        if loja_escolha == '':
                            limpar()
                            continue
                        elif loja_escolha.isdigit():
                            idx_loja = int(loja_escolha) - 1
                            if 0 <= idx_loja < len(concessionaria):
                                tupla_carro_escolhido = concessionaria[idx_loja]
                                preco_carro_escolhido = precos_concessionaria[idx_loja]
                                
                                # Define a variável pegando o nome direto da primeira vaga da tupla
                                nome_carro_escolhido = tupla_carro_escolhido[0]
                                
                                if nome_carro_escolhido in Sua_Garagem_Carros:
                                    print(f'\nVocê já possui o {nome_carro_escolhido} na sua garagem!')
                                    sleep(2)
                                    limpar()
                                    continue
                                    
                                if carteira['Bolso'] >= preco_carro_escolhido:
                                    limpar()
                                    print(f'Personalização do seu novo {nome_carro_escolhido}')
                                    cor_customizada = input('Digite a cor que deseja para o veículo >>>: ').strip()
                                    if cor_customizada == "":
                                        cor_customizada = "Preto"

                                    carteira['Bolso'] -= preco_carro_escolhido
                                    salvar_dados('carteira', carteira)
                                    

                                    novo_carro = car(tupla_carro_escolhido)
                                    novo_carro.cor_carro = cor_customizada


                                    Sua_Garagem_Carros = carregar_dados('NFS', {})
                                    if isinstance(Sua_Garagem_Carros, (tuple, str)):
                                        Sua_Garagem_Carros = {}
                                        
                                    Sua_Garagem_Carros[novo_carro.modelo_carro] = novo_carro.__dict__
                                    
                                    salvar_dados('NFS', Sua_Garagem_Carros)
                                    salvar_dados('carro_atual', novo_carro.__dict__)
                                    print(f'\nVocê comprou o {novo_carro.modelo_carro} por R${preco_carro_escolhido:,.2f}!')
                                    sleep(2)
                                    limpar()
                                else:
                                    print('\n Saldo insuficiente no Bolso!')
                                    sleep(2)
                                    limpar()
                            else:
                                print('\n Opção inválida!')
                                sleep(1.5)
                                limpar()
        if escolha == "R": #ver ranking
            registrar_acao_jogador(None, "Verificou o Ranking Global")
            limpar()
            ver_ranking(nome)
        if escolha == "E": #ver faculdade
            if carteira["Banco"] < 0 and nome != "727":
                print("Pague sua dívida primeiro.")
                sleep(2)
                limpar()
            else:
                if not "Carro" in Garagem:
                    print("A faculdade fica muito longe, Você não consegue ir lá...\nTalvez seria melhor comprar um carro")
                    sleep(4)
                    limpar()
                else:
                    barra_viagem(5)
                    facul = True
                    while facul:
                        limpar()
                        print("ENSINO SUPERIOR".center(30,"="))
                        for i , (nome_faculdade , progresso) in enumerate(estudos.items(),start= 1):
                            for nome_taxa_pag , condição in estudos_pag_inicial.items():
                                if nome_faculdade == nome_taxa_pag:
                                    if condição == False:
                                        print(f"[{i}] {nome_faculdade}- VALOR INICIAL: R$130.000,00 ")
                                    else:
                                        if progresso < 100:
                                            print(f"[{i}] {nome_faculdade}: Progresso {progresso}% [R$10.000,00 PARA PROSSEGUIR]")
                                        else:
                                            print(f"[{i}] {nome_faculdade}: CONCLUÍDO")
                        opc_facul = input("ENTER PARA SAIR| ESCOLHA ALGUM ITEM\n: ").strip()
                        if opc_facul == "":
                            facul = False
                            barra_viagem(5)
                            limpar()
                            break
                        else:
                            try:
                                indice = int(opc_facul) - 1
                                lista_facul = list(estudos)
                                if not 0 <= indice < len(lista_facul):
                                    raise ValueError
                                else:
                                    nome_facul = lista_facul[indice]
                                    if estudos_pag_inicial[nome_facul] == False:
                                        compra = input(f"Você gostaria de pagar o valor inicial da faculdade de {nome_facul}\n pelo valor de R$130.000,00?\nS/N: ").upper().strip()
                                        if compra == "S":
                                            if carteira['Bolso'] >= 130000:
                                                print("Pagamento concluído")
                                                estudos_pag_inicial[nome_facul] = True
                                                salvar_dados("estudos_pag_inicial",estudos_pag_inicial)
                                                carteira["Bolso"] -= 130000
                                                salvar_dados("carteira",carteira)
                                                
                                                sleep(2)
                                                limpar()
                                            else:
                                                print("Dinheiro insuficiente")
                                                sleep(2)
                                                limpar()
                                        else:
                                            print("Pagamento cancelado")
                                            sleep(2)
                                            limpar()
                                    elif estudos_pag_inicial[nome_facul] == True:
                                        if estudos[nome_facul] == 100:
                                            print("Você já concluiu este ensino.")
                                            sleep(2)
                                            limpar()
                                        else: 
                                            compra = input(f"Você gostaria de continuar seu progresso de {estudos[nome_facul]}% para {estudos[nome_facul] + 10}%\nPor R$10.000,00 ?\nS/N: ").upper().strip()
                                            if compra == "S":
                                                if carteira['Bolso'] >= 10000:
                                                    print("Pagamento concluído")
                                                    estudos[nome_facul] += 10 
                                                    salvar_dados("estudos",estudos)
                                                    carteira["Bolso"] -= 10000
                                                    salvar_dados("carteira",carteira)
                                                    
                                                    sleep(2)
                                                    limpar()
                                                else:
                                                    print("Dinheiro insuficiente")
                                                    sleep(2)
                                                    limpar()
                                            else:
                                                print("Pagamento cancelado")
                                                sleep(2)
                                                limpar()
                            except (TypeError, ValueError):
                                print("VALOR INVÁLIDO")
                                sleep(2)
                                continue
        if escolha == "C": #ver Empresa
            if not all(valor == 100 for valor in estudos.values()):
                continue
            else:
                hub_empresa = True
                limpar()
                if not os.path.exists("nome_empresa.json"):
                    nome_escolhido = input("Qual será o nome de sua empresa?\n: ").strip()
                    nome_empresa = nome_escolhido
                    salvar_dados("nome_empresa", nome_escolhido)
                while hub_empresa:
                    limpar()
                    print(f"{nome_empresa}".center(len(nome_empresa)+30,"="))
                    # 1. Calcula o texto do Upgrade antes do print
                    if empresa['Nível'] < 5:
                        txt_upgrade = f"R${empresa['custo_upgrade']:,.2f}"
                    else:
                        txt_upgrade = "MÁXIMO"

                    # 2. Calcula o texto do Marketing antes do print
                    if empresa['Nível_propaganda'] < 5:
                        txt_marketing = f"R${empresa['custo_propaganda']:,.2f}"
                    else:
                        txt_marketing = "MÁXIMO"

                    # 3. Agora o print fica ridículo de limpo, sem nenhum if/else interno para dar erro!
                    print(f"GERENCIE SEU NEGÓCIO\nCEO:{nome}\n"
                        f"Nível da empresa: {empresa['Nível'] if empresa['Nível'] < 5 else 'MÁXIMO'}\n"
                        f"Nível do Marketing: {empresa['Nível_propaganda'] if empresa['Nível_propaganda'] < 5 else 'MÁXIMO'}\n"
                        f"Faturamento: R${empresa['Faturamento']:,.2f}\n\n"
                        f" [1] UPGRADE: {txt_upgrade}      [2] MARKETING: {txt_marketing}")


                    gerent_op = input("ENTER PARA SAIR| >>> ").strip()
                    if gerent_op == "":
                        hub_empresa = False
                        limpar()
                        break
                    if gerent_op == "1":
                        if empresa['Nível'] == 5:
                            print("Você atingiu o Nível máximo da infraestrutura")
                            sleep(2)
                            limpar()
                        else:
                            compra = input(f"Você gostaria de comprar um Upgrade para a infraestrutura da empresa por R${empresa['custo_upgrade']:,.2f} ?\nS/N: ").strip().upper()
                            if compra == "S":
                                if carteira["Bolso"] >= empresa["custo_upgrade"]:
                                    empresa['Nível'] += 1
                                    carteira['Bolso'] -= empresa["custo_upgrade"]
                                    if um_um == 1:
                                        um_um += 1
                                        salvar_dados("aviso",um)
                                        bandeira["empresa"] = True
                                        salvar_dados("bandeira",bandeira)
                                        threading.Thread(target=pagamento_da_empresa,daemon=True).start()

                                    if empresa['custo_upgrade'] < 6431250:
                                        empresa["custo_upgrade"] *= 3.5
                                    else:
                                        empresa["custo_upgrade"] *= 2
                                    empresa['Faturamento'] = (empresa['Nível'] * 1000000) * (1 + empresa['Nível_propaganda'] * 3.76) + (empresa['Nível_propaganda'] * 200000)
                                    print("Compra realizada com sucesso")

                                    salvar_dados("carteira",carteira)
                                    
                                    salvar_dados("empresa",empresa)
                                    sleep(2)
                                    limpar()
                                else:
                                    print("Saldo insuficiente")
                                    sleep(2)
                                    limpar()
                            else:
                                limpar()
                    if gerent_op == "2":
                        if empresa['Nível_propaganda'] == 5:
                            print("Você atingiu o Nível máximo do Marketing")
                            sleep(2)
                            limpar()
                        else:
                            if empresa['Nível'] == 0:
                                print("Primeiro tem de haver uma empresa para poder publicar sobre ela!")
                                sleep(2)
                                limpar()
                            else:
                                compra = input(f"Você gostaria de comprar um Upgrade para o Marketing da empresa por R${empresa['custo_propaganda']:,.2f} ?\nS/N: ").strip().upper()
                                if compra == "S":
                                    if carteira["Bolso"] >= empresa['custo_propaganda']:
                                        empresa['Nível_propaganda'] += 1
                                        carteira['Bolso'] -= empresa['custo_propaganda']
                                        if empresa['custo_propaganda'] < 1225000:
                                            empresa['custo_propaganda'] *= 3.5
                                        else:
                                            empresa['custo_propaganda'] *= 2
                                        print("Compra realizada com sucesso")
                                        empresa['Faturamento'] = (empresa['Nível'] * 1000000) * (1 + empresa['Nível_propaganda'] * 3.76) + (empresa['Nível_propaganda'] * 200000)
                                        salvar_dados("carteira",carteira)
                                        
                                        salvar_dados("empresa",empresa)
                                        sleep(2)
                                        limpar()
                                    else:
                                        print("Saldo insuficiente")
                                        sleep(2)
                                        limpar()
                                else:
                                    limpar()

def enviar_nota_jogo(nota,comentario="Sem comentário",jogador="Anônimo"):
    # Cole aqui a URL do seu webhook do Discord
    url_webhook = DEScodificar('S:HFSxtxtqpSMGCLN//DKNbiSMGcpUIORVPDKNPNTcpUIOtm/ATRqpbi/mwELEibHFSUIOUIOjkSMG/WVDJTSYHMJTSZXLRFGJTSBDWRFGBDWWVDMXZQPLJTSVCFYHMWVDWVDZXL/ZXLZXLQPLE_TENiu_ONTRSMGF_THIRTY_trlSMGkjYHMkjH_KEYD_FIVEL_ZEROMXZWVDHFSJTSwnHFSBDWVCFF_THIRTYkjH_KEYBDWZXLP_QPtrlvltB_INjkF_THIRTYN_MINUSVCFpqYHMA_NINEzlnwncpQ_PQL_ZEROpqSMGD_FIVExtzlnX_PERvltUIOcpR_BARSMGY_ANDJ_KJZXLZXLF_THIRTYkjmwQPLSMGtmVCF')
    
    # Formata a mensagem de um jeito visualmente legal (Rich Embed)
    payload = {
        "embeds": [
            {
                "title": "🎮 Nova Avaliação do Jogo!",
                "color": 3066993,  # Cor verde em formato decimal
                "fields": [
                    {"name": "⭐ Nota", "value": f"**{nota}/10**", "inline": True},
                    {"name": "💬 Feedback", "value": comentario, "inline": False},
                    {"name": "🤖 Jogador", "value": jogador, "inline": False}
                ],
                "footer": {"text": "Sistema de Feedback Automático"}
            }
        ]
    }
    
    # Envia os dados para o Discord
    resposta = requests.post(url_webhook, json=payload)
    
    if resposta.status_code == 204:
        print("Avaliação enviada com sucesso para o Discord!")
    else:
        print(f"Erro ao enviar: {resposta.status_code}")


def menu_hub():
    while True:
        limpar()
        print("MENU".center(50,"-"))
        escolha = input("[1]PRINCIPAL|Life Business-Gold Trial\n[2]Versão do jogo\n[3]Avalie o Jogo!\n>>> ")
        if escolha == "1":
            Jogo_principal()
        if escolha == "2":
            limpar()
            print("Versão: 15.5V | SOLUÇÃO DE BUGS")
            input("ENTER")
            continue
        if escolha == "3":
            try:
                limpar()
                print("De 0 a 10, Qual a nota você daria para o Jogo? Fique a vontade para enviar uma mensagem|DEIXE VAZIO PARA NÃO RESPONDER|")
                nota = input("[PRIMEIRO ESCOLHA DE 0 à 10 *respeite o limite]: ").strip()
                comentario = input("[AGORA SEU COMENTÁRIO]: ")
                user = input("[SE QUISER DÊ SEU NOME/NICK NAME]: ").strip()
                if nota != "" and nota.isdigit():
                    notaverifica = int(nota)
                    if notaverifica <= 10 and notaverifica >= 0:
                        if user == "":
                            user = "Anônimo"
                        enviar_nota_jogo(nota,comentario,user)
                    else:
                        print("\nVALOR DA NOTA INVÁLIDO")
                        sleep(2)
                        limpar()
                else:
                    print("\nAVALIAÇÃO CANCELADA")
                    sleep(2)
                    limpar()
            except ValueError:
                print('Eu sou você amanhã  - Zacarias')
                sleep(2)
                limpar()
        else:
            limpar()
            print("Dê uma alternativa válida.")
            sleep(2)

if __name__ == "__main__":
    menu_hub()