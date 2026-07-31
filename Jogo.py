from time import sleep, time
import webbrowser as w
from random import choice, randint, uniform, random,sample
import os
import threading
import json
import sys
import base64
import pymongo
import subprocess
zerar = 0
VERDE = '\033[32m'
AMARELO = '\033[33m'
AZUL = '\033[34m'
VERMELHO = '\033[31m'
RESET = '\033[0m'
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
def salvar_dados(nome_arquivo, dados):
        with open(f"{nome_arquivo}.json", "w") as f:
            texto_json = json.dumps(dados,indent=4)
            texto_codificado = base64.b64encode(texto_json.encode()).decode()
            f.write(texto_codificado)
def carregar_dados(nome_arquivo, valor_padrao):

        try:
            with open(f"{nome_arquivo}.json", "r") as f:
                texto_protegido = f.read()
                texto_limpo = base64.b64decode(texto_protegido).decode()
                return json.loads(texto_limpo)
        except (FileNotFoundError, Exception):
            return valor_padrao
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
def limpar(): #o os.sla oque
    os.system('cls' if os.name == 'nt' else 'clear')
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
        if random() < 0.10: 
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
        sleep(15)
def imposto():
    while True:
        sleep(300)
        try:
            if carteira["Banco"] >= 200000:
                
                if carteira["Banco"] >= 200000:
                    carteira["Banco"]  -= carteira["Banco"] * 0.29
                    salvar_dados("carteira",carteira)
            elif carteira["Banco"] >= 140000:
                if carteira["Banco"] >= 140000:
                    carteira["Banco"]  -= carteira["Banco"] * 0.18
                    salvar_dados("carteira",carteira)
            elif carteira["Banco"] >= 25000:
                if carteira["Banco"] >= 25000:
                    carteira["Banco"]  -= carteira["Banco"] * 0.14
                    salvar_dados("carteira",carteira)
                else:
                    pass
        except Exception:
            sleep(20)
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
            # Pega os dados do banco (se não existirem, o .get coloca 0 ou "Nenhum")
            nome_player = j.get('nome', 'Desconhecido')
            bolso = j.get('bolso', 0)
            banco = j.get('banco', 0)
            total = j.get('total', 0)
            zerou = j.get('zerar', 0)
            itens = ", ".join(j.get('garagem', []))

            # Mostra o Nome e o Total em destaque
            for valor_minimo, nome_titulo in titulos:
                if total >= valor_minimo:
                    status = nome_titulo
                    break   
            if nome_player == seu_nome_atual:
                print(f"{i}º| {status:<15} | {nome_player} <--- (EU)")
            else:
                print(f"{i}º| {status:<15} | {nome_player}")
            print(f"    TOTAL: R$ {total:,.2f} (Bolso: R$ {bolso:,.2f} | Banco: R$ {banco:,.2f})")
            print(f"    Zerou: {zerar} vezes")
            print(f"    Itens: {itens if itens else 'Nenhum'}")
            print("—" * 40)

        input("\nPressione Enter para voltar ao menu...")
    except Exception:
        print("Falha na rede ou Nuvem!")
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
def Jogo_principal():
    global Garagem, carteira, nome



    def render():
        while True:
            sleep(150)
            valor_atual = carteira["Banco"]
                
            if valor_atual > 10000:
                taxa = 0.04  # 4% 
            elif valor_atual > 5000:
                taxa = 0.03  # 3%
            elif valor_atual > 500:
                    taxa = 0.01  # 1%
            else:
                taxa = 0.008 # 0.8%

            rendimento = valor_atual * taxa
                
            if rendimento > 0:
                carteira["Banco"] = round(valor_atual + rendimento, 2)
                try:
                    salvar_dados("carteira", carteira)
                except:
                    pass
    desenho_intro = rf"""{VERDE}
    ░░▒█ █▀▀▀█ █▀▀█ █▀▀▀█   █▀▀▄ █▀▀█   █░░▒█ ▀█▀ █▀▀▄ █▀▀█
    ▄░▒█ █░░▒█ █░▄▄ █░░▒█   █░▒█ █▄▄█   ▒█▒█░ ░█░ █░▒█ █▄▄█            
    █▄▄█ █▄▄▄█ █▄▄█ █▄▄▄█   █▄▄▀ █░▒█   ░▀▄▀░ ▄█▄ █▄▄▀ █░▒█ *v11V*

    █▀▀█       █▀▀█ █▀▀█ ▀▀█▀▀ █▀▀   █▀▀▄ █▀▀█     █▀▀ █▀▀█ █▀▀█ ░▀░ ▀▀█▀▀ █▀▀█ █░░ ░▀░ █▀▀ █▀▄▀█ █▀▀█
    █▄▄█       █▄▄█ █▄▄▀ ░░█░░ █▀▀   █░░█ █░░█     █░░ █▄▄█ █░░█ ▀█▀ ░░█░░ █▄▄█ █░░ ▀█▀ ▀▀█ █░▀░█ █░░█
    █░▒█       ▀░░▀ ▀░▀▀ ░░▀░░ ▀▀▀   ▀▀▀░ ▀▀▀▀     ▀▀▀ ▀░░▀ █▀▀▀ ▀▀▀ ░░▀░░ ▀░░▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀░░░▀ ▀▀▀▀ by rogerin {RESET}
"""
    sleep(4)
    default_primeira_intro = 1
    default_nome = "user"
    nome = carregar_dados("nome",default_nome)
    primeira_intro = carregar_dados("intro", default_primeira_intro)

#INTRO LEGAL

    #jogo#
    limpar()
    digitar(desenho_intro, velocidade=0.02)#intro pre jogo
    sleep(4)
    default_carteira = {"Bolso": 0.0, "Banco": -1400.0}
    default_Garagem = {}
    default_licenças = {"Trabalho1":True, "Trabalho2":False,"Trabalho3":False,"Trabalho4":False,"Carteira D":False}
    clt_shop = {"Trabalho1": "GRATUITO", "Trabalho2": 800,"Trabalho3": 3000,"Trabalho4":10000,"Carteira D":1200}
    mercado = {"Carro": 10000,"Caminhão": 52000, "Guitarra": 400, "Moto": 5000, "Casa Pequena": 12000, "Casa Média": 40000, "Mansão": 190000, "Helicóptero": 80000, "Telefone": 1200, "Bicicleta": 300,
                   "Barco de pesca": 23000, "Barco grande": 120000, "Iate": 400000, "Picareta": 120,"PC p/ servidor": 40000 ,"GLOBO TERRESTRE": 10000000000,}
    default_zerar = 0
    zerar = carregar_dados("zerar", default_zerar)
    carteira = carregar_dados("carteira", default_carteira)
    licenças = carregar_dados("licencas", default_licenças)
    Garagem = carregar_dados("garagem", default_Garagem)
    placa_caminhao = carregar_dados("placa_caminhão", "SEM-PLACA")
    default_bandeira = {"imposto": False}
    bandeira = carregar_dados("bandeira",default_bandeira)
    t = threading.Thread(target=render, daemon=True)
    t.start()

    def atualizar_nuvem(nome_usuario, bolso, banco, lista_garagem,zerar):
        try:
            total = bolso + banco
            ranking_col.update_one(
                {"nome": nome_usuario},
                {"$set": {
                    "total": total,
                    "bolso": bolso,
                    "banco": banco,
                    "garagem": lista_garagem, 
                    "zerar": zerar# Salva a lista direto!
                }},
                upsert=True # Se não existir o nome, ele cria um novo
            )
        except Exception as e:
            print(f"Erro ao conectar com o ranking: {e}")
    
    
    
    if "GLOBO TERRESTRE" in Garagem: #efeito zerar
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Você comprou o mundo, tudo é seu. Parabéns por zerar o game {nome}")
        DECISAO = input("Você quer reiniciar o jogo?\n N/S: ")
        if DECISAO.strip().upper() == "S":
            carteira =  salvar_dados("carteira", default_carteira)
            carteira = carregar_dados("carteira", default_carteira)
            licenças = salvar_dados("licencas",default_licenças)
            licenças = carregar_dados("licencas",default_licenças)
            Garagem = salvar_dados("garagem",default_Garagem)
            Garagem = carregar_dados("garagem",default_Garagem)
            bandeira = salvar_dados("bandeira",default_bandeira)
            bandeira = carregar_dados("bandeira",default_bandeira)
            
            arquivos_para_deletar = [
                "config_pc.json", "Carteira Krypto.json", "carteira_motorista.json",
                "placa_caminhão.json", "estoque agro.json", "Historico preços.json",
                "fadiga.json", "Historico km.json", "aviso.json"
            ]

            for arquivo in arquivos_para_deletar:
                if os.path.exists(arquivo):
                    os.remove(arquivo)


            zerar += 1
            salvar_dados("zerar", zerar)
            primeira_intro +=1
            salvar_dados("intro",primeira_intro)
            atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
        else:
            print("OBRIGADO POR JOGAR| FECHE O PROGRAMA (1 hora para fechar automaticamente)")
            atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
            sleep(3600)
            exit()

    
    if primeira_intro > 0:
        if os.path.exists("Carteira Krypto.json"):
            os.remove("Carteira Krypto.json")
        os.system('cls' if os.name == 'nt' else 'clear')
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
        digitar("Mas você teve um estalo: Se o mundo é cheio de gente preguiçosa, resolver problemas bobos é uma mina de ouro.")
        digitar("O mercado é um oceano de preguiça. Aprenda a pescar onde ninguém quer olhar.")
        sleep(3)
        digitar("Então começe a fazer o que sabe de melhor...")
        sleep(3)
        digitar(rf"""{AMARELO}

    █▀▀▀ ▀▄ ▄▀ █▀▀█ █    █▀▀▀█ ▀▀█▀▀ █▀▀█ █▀▀█   █▀▀█   █▀▀█ █▀▀█ █▀▀▀ █▀▀█ █  █ ▀█▀ █▀▀█ █▀▀█      
    █▀▀▀   █   █▄▄█ █    █░░▒█   █   █▄▄█ █▄▄▀   █▄▄█   █▄▄█ █▄▄▀ █▀▀▀ █░▄▄ █░▒█ ░█░ █░░░ █▄▄█      
    █▄▄▄ ▄▀ ▀▄ █    █▄▄█ █▄▄▄█ ░▒█░░ █ ▒█ █ ▒█   █ ▒█   █░░░ █░▒█ █▄▄▄ █▄▄█ ▀▄▄▀ ▄█▄ █▄▄█ █░▒█....       
                                                                                      █░░       {RESET}
                                                                                                ou algo desse tipo""",velocidade=0.01)
        
        
        
        
        sleep(6.5)
        limpar()
        
        if not os.path.exists("nome.json"):
            nome = input("SEU NOME: ")
            salvar_dados("nome",nome)
        primeira_intro -= 1
        salvar_dados("intro",primeira_intro)
    c = threading.Thread(target=mineracao_background, daemon=True)
    c.start()
    threading.Thread(target=oscilar_mercado, daemon=True).start()


    if bandeira["imposto"] is True:
        threading.Thread(target=imposto, daemon= True).start()

    organizar_janelas_lado_a_lado()
    while True:
        #DIVIDA
        if carteira["Bolso"] <0:
            carteira["Banco"] += carteira["Bolso"]
            carteira["Bolso"] = 0
        else:   
            pass
        #DIVIDA

        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
        limpar()
        print("JOGO DA VIDA".center(10,"-"))
        print(f"USUÁRIO: {nome}")
        
        if zerar == 1:
            print(f"!Você zerou o jogo {zerar} vez! :)")
        elif 1 < zerar < 3:
            print(f"!Você zerou o jogo {zerar} vezes! :)")
        elif zerar >= 3:
            print(f"Caramba, Você zerou o jogo {zerar} vezes! Cansou não?\n")

        zero = 0
        zerozero = carregar_dados("aviso",zero)

        if "Barco de pesca" in Garagem:print("[10] Ir pescar") 
        if "Moto" in Garagem:print("[11] Moto boy")
        if "Picareta" in Garagem:print("[12] Minerar") 
        if "PC p/ servidor" in Garagem:print("[13] BITINHO COIN") 
        if "Caminhão" in Garagem:print("[14] Frete") 
        if "Telefone" in Garagem: print("[15] Bolsa de Valores")
        if "Bicicleta" in Garagem: print("[16] Bike boy")
        if carteira["Banco"] > 25000:
            if zerozero <= 0:
                print("Você tem um valor alto na conta, a receita federal ira cobrar uma taxa a cada cinco minutos!!!")
                zero += 1
                sleep(5)
                salvar_dados("aviso",zero)
                bandeira["imposto"] = True
                salvar_dados("bandeira",bandeira)
                threading.Thread(target=imposto, daemon= True).start()
                continue
        
        
        escolha = input("OPÇÕES    -------------------> [R] Ver ranking \n[1] Trabalhos Fáceis\n[2] Trabalhos Médios\n[3] Trabalhos Difíceis\n[4] Desafio do tesouro\n[5] LOJA DE DESBLOQUEIO DE TRABALHOS\n[6] Visualizar carteira\n[7] Banco do Brasil\n[8] Ver garagem\n[9] Mercado\n--> ").upper()
        #TODO O RESTO
        if escolha == "5": #Venda licença
                if carteira["Banco"] < 0:
                    print("Pague suas dívidas antes de efetuar qualquer compra!")
                    input("ENTER PARA CONTINUAR")
                else:
                    loja_clt = True
                    while loja_clt:
                        try:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print("LICENÇAS CLT".center(40,"="))
                            print(f"[]Trabalhos fáceis: {clt_shop['Trabalho1']}")
                            if licenças["Trabalho2"] is False:
                                print(f"[1]Trabalhos Médios: R${clt_shop['Trabalho2']:.2f}")
                            else:
                                print(f"[1]Trabalhos Médios: COMPRADO")
                            if licenças["Trabalho3"] is False:
                                print(f"[2]Trabalhos Difíceis: R${clt_shop['Trabalho3']:.2f}")
                            else:
                                print(f"[2]Trabalhos Difíceis: COMPRADO")
                            if licenças["Trabalho4"] is False:
                                print(f"[3]Desafio do tesouro: R${clt_shop['Trabalho4']:.2f}")
                            else:
                                print(f"[3]Desafio do tesouro: COMPRADO")
                            if licenças["Carteira D"] is False:
                                print(f"[4]Carteira D: R${clt_shop['Carteira D']:.2f}")
                            else:
                                print(f"[4]Carteira D: COMPRADO")


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
                                        os.system('cls' if os.name == 'nt' else 'clear')
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
                                        os.system('cls' if os.name == 'nt' else 'clear')
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
                                        os.system('cls' if os.name == 'nt' else 'clear')
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
                                        os.system('cls' if os.name == 'nt' else 'clear')
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
                    print(f"NO BANCO: R${carteira["Banco"]:.2f}")
                else:
                    print(f"NO BANCO: R${carteira["Banco"]:.2f} DE DÍVIDAS!")
                print(f"NA CARTEIRA: R${carteira["Bolso"]:.2f}")
                sair = input("ENTER PARA VOLTAR")
                if sair.strip() == "":
                    ambiente = False
                    break
                sleep(2)
                limpar()
        if escolha == "1": #TRABALHOS FÁCEIS
            trabalho = True
            while trabalho is True:
                os.system('cls' if os.name == 'nt' else 'clear')
                A = randint(1,20)
                B = randint(1,30)
                soma = A + B
                try:
                    resposta = int(input(f"Quanto é {A}+{B}?\nRESPOSTA: "))
                    if resposta == soma:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        ganho = round(uniform(5.40,50.30), 2)
                        carteira["Bolso"] += ganho
                        print(f"Parabéns, você ganhou R${ganho:.2f} em dinheiro vivo!")
                        salvar_dados("carteira", carteira)
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
                        reinicio = input("Continuar? S/N:  ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break  
                    else:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Você errou, infelizmente.")
                        reinicio = input("Continuar? S/N: ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break
                except ValueError:
                    print("digite apenas números aqui!")
        if escolha == "2": #TRABALHOS MÉDIOS
            if licenças["Trabalho2"] is True:
                pass
            else:
                print("Você não possui licença para este emprego!")
                input("ENTER PARA VOLTAR")
                continue
            trabalho = True
            while trabalho is True:
                os.system('cls' if os.name == 'nt' else 'clear')
                A = randint(1,100)
                B = randint(1,30)
                soma = A * B
                try:
                    resposta = int(input(f"Quanto é {A}X{B}?\nRESPOSTA: ").strip().replace(",","").replace(".",""))
                    if resposta == soma:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        ganho = round(uniform(60.40,130.99), 2)
                        carteira["Bolso"] += ganho
                        salvar_dados("carteira", carteira)
                        print(f"Parabéns, você ganhou R${ganho:.2f} em dinheiro vivo!")
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
                        reinicio = input("Continuar? S/N:  ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break  
                    else:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Você errou, infelizmente.")
                        reinicio = input("Continuar? S/N: ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break
                except ValueError:
                    print("digite apenas números aqui!")
        if escolha == "3": #TRABALHOS DIFÍCEIS
            if licenças["Trabalho3"] is True:
                pass
            else:
                print("Você não possui licença para este emprego!")
                input("ENTER PARA VOLTAR")
                continue
            trabalho = True
            while trabalho is True:
                os.system('cls' if os.name == 'nt' else 'clear')
                contas_divisao = [(100,2),(50,5),(30,2),(6,2),(9,3),
                                    (144, 12), (168, 14), (225, 15), (390, 13), (112, 7), 
                                    (135, 9), (182, 14), (252, 12), (324, 18), (448, 14), 
                                    (729, 27), (840, 24), (936, 12), (1024, 32), (625, 25)
                                ]
                conta_definida = choice(contas_divisao)
                soma = conta_definida[0]//conta_definida[1]
                try:
                    resposta = int(input(f"Quanto é {conta_definida[0]} dividido por {conta_definida[1]}?\nRESPOSTA: ").strip().replace(",","").replace(".",""))
                    if resposta == soma:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        ganho = round(uniform(300.40,540.99), 2)
                        carteira["Bolso"] += ganho
                        salvar_dados("carteira", carteira)
                        print(f"Parabéns, você ganhou R${ganho:.2f} em dinheiro vivo!")
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
                        reinicio = input("Continuar? S/N:  ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break  
                    else:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Você errou, infelizmente.")
                        reinicio = input("Continuar? S/N: ")
                        if reinicio.strip().upper() == "S" or "":
                            continue
                        elif reinicio.strip().upper() == "N":
                            trabalho = False
                            break
                except ValueError:
                    print("digite apenas números aqui!")
        if escolha == "4": #Desafio do tesouro
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
                    os.system('cls' if os.name == 'nt' else 'clear')
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
                        resposta_1 = int(float(input(f"Quanto é {A}+{B}?\n: ").strip().replace(",","").replace(".","")))
                        
                        if resposta_1 == soma1:
                            ganho = round(uniform(1000.40,4000.99), 2)
                            bolsa += ganho
                            limpar()
                        else:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            erro += 1
                            input("ERRADO! (PRESSIONE ENTER)")
                            limpar()
                        resposta_2 = int(input(f"Quanto é {C}X{D}?\n: ").strip().replace(",","").replace(".",""))
                        
                        if resposta_2 == soma2:
                            ganho = round(uniform(2500.40,5000.99), 2)
                            bolsa += ganho
                            limpar()
                        else:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            erro += 1
                            input("ERRADO! (PRESSIONE ENTER)")
                            limpar()
                        resposta_3 = int(input(f"Quanto é {conta_definida[0]} dividido por {conta_definida[1]}?\n: ").strip().replace(",","").replace(".",""))
                        if resposta_3 == soma3:
                            ganho = round(uniform(2500.40,5000.99), 2)
                            bolsa += ganho
                        else:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            erro += 1
                            input("ERRADO! (PRESSIONE ENTER)")
                        tempo_off = time()
                        tempo_total = tempo_off - tempo_on
                        if tempo_total > 30:
                                os.system('cls' if os.name == 'nt' else 'clear')
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
                                    print("Você errou tudo!")
                                carteira["Bolso"] += bolsa
                                salvar_dados("carteira", carteira)
                                atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
                                print(f"Você ganhou R${bolsa:.2f} em dinheiro vivo!")

                                reinicio = input("Continuar? S/N: ")
                                os.system('cls' if os.name == 'nt' else 'clear')
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
            banco = True
            while banco is True:
                try:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("BANDO DO BRASIL".center(40,"/"))
                    print("*Seu dinheiro rende mais, dependendo do valor guardado*\n[1]Depositar dinheiro               [3]Depositar Tudo \n[2]Retirar dinheiro                 [4]Retirar tudo")
                    if carteira["Banco"] < 0:
                        print(f"Sua conta está no vermelho! Você deve R${carteira["Banco"]:.2f} para o banco\nTodo valor colocado será descontado pela dívida.\n")
                    banco_escolha = input("Escolha uma opção| ENTER PARA SAIR\n: ")
                    if banco_escolha == "testesenha":
                        print("DEBUG acessado")
                        carteira["Bolso"] += 10000000000
                        input("ENTER")
                    if banco_escolha == "1": #depositar
                        print(f"Você tem R${carteira['Bolso']:.2f} em dinheiro")
                        quantia = float(input("Quanto para colocar na conta?\n: ").replace(",", "."))
                        if round(quantia,2) <= float(carteira["Bolso"]) and quantia >=0:
                            carteira["Bolso"] = round(float(carteira["Bolso"]) - quantia, 2)
                            carteira["Banco"] = round(float(carteira["Banco"]) + quantia, 2)
                            print(f"R${quantia:.2f} foi depositado na conta!")
                            salvar_dados("carteira", carteira)
                            input("ENTER PARA COTINUAR")
                        else:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"Você não tem esse valor: R${quantia:.2f}")
                            input("Enter para continuar")
                    if banco_escolha == "2": #sacar
                        if carteira["Banco"] > 0:
                            print(f"Você tem R${carteira['Banco']:.2f} na conta")
                            quantia = float(input("Quanto para retirar da conta?\n: ").replace(",", "."))
                            if round(quantia,2) <= float(carteira["Banco"]) and  quantia >0:
                                carteira["Banco"] -= round(float( quantia))
                                carteira['Bolso'] += round(float( quantia))
                                print(f"R${quantia:.2f} foi retirado da sua conta!")
                                salvar_dados("carteira", carteira)
                                input("ENTER PARA COTINUAR")
                            else:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                print(f"Você não tem esse valor: R${quantia:.2f}, você tem R${carteira['Banco']:.2f}")
                                input("Enter para continuar")
                        else:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"Você não tem fundos na conta")
                            input("Enter para continuar")
                    if banco_escolha == "3": #Depositar tudo
                        carteira["Banco"] += carteira["Bolso"]
                        print(f"R${carteira["Bolso"]:.2f} foi depositado à sua conta!")
                        carteira["Bolso"] = 0
                        salvar_dados("carteira",carteira)
                        sleep(1)
                        os.system('cls' if os.name == 'nt' else 'clear')
                    if banco_escolha == "4": #Sacar tudo
                        if not carteira["Banco"] <0:
                            carteira["Bolso"]+=carteira["Banco"]
                            print(f"Você sacou todo o valor|R${carteira["Banco"]:.2f}")
                            carteira["Banco"] = 0
                            salvar_dados("carteira",carteira)
                            sleep(1)
                            os.system('cls' if os.name == 'nt' else 'clear')
                        else:
                            print("Não é possível fazer esta ação")
                            sleep(1)
                            os.system('cls' if os.name == 'nt' else 'clear')
                    if banco_escolha == "":
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
                        banco = False
                        break
                except ValueError:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Digite um valor válido")
                    input("ENTER para continuar")
        if escolha == "8": #Ver garagem
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
            if carteira["Banco"] < 0:
                print("Pague suas dívidas antes de efetuar qualquer compra!")
                input("ENTER PARA CONTINUAR")
            else:
                ambiente = True
                while ambiente:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("AMERICANAS".center(40,"-"))
                    for i,(mercadoria,valor) in enumerate(mercado.items(),start = 1):
                        status = f"R${valor:.2f}" if mercadoria not in Garagem else "[ESGOTADO]"
                        print(f"[{i}] {mercadoria}: {status}")
                    item = input("ESCOLHA UM ITEM| ENTER PARA SAIR\n-> ")
                    if item == "":
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
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
                            
                                print(f"Você selecionou {nome_item} - Preço: R${preco:.2f}")
                                confirmar = input(f"Confirmar compra de {nome_item}? S/N: ").upper()
                                if confirmar == "S":
                                    if carteira["Bolso"] >= preco:
                                        if nome_item in Garagem:
                                            print(f"Você já possui o item {nome_item}! Escolha outro.")
                                            input("ENTER PARA CONTINUAR")
                                            os.system('cls' if os.name == 'nt' else 'clear')
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
                os.system('cls' if os.name == 'nt' else 'clear')
                print("PESQUE PEIXES PARA VENDER|QUANTO MAIOR O PEIXE, MAIS DIFÍCIL")
                tamanhos = ("GRANDE","PEQUENO","MÉDIO","MUITO PEQUENO","ENORME")
                peixe_da_vez = []
                for a in range(3):
                    tamanhos_ok = choice(tamanhos)
                    peixe_da_vez.append(tamanhos_ok)
                    print(f"[{a + 1}] Um peixe {tamanhos_ok} apareceu!")
                a = input("ESCOLHA O PEIXE|ENTER PARA SAIR\n: ")
                if a == "":
                    atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
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
                        os.system('cls' if os.name == 'nt' else 'clear')
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
                            print(f"Você não tem dinheiro na mão, Foi descontado de sua conta os R${perda:.2f}.")
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
                        os.system('cls' if os.name == 'nt' else 'clear')
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
                            print(f"Você não tem dinheiro na mão, Foi descontado de sua conta os R${perda:.2f}.")
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
                        os.system('cls' if os.name == 'nt' else 'clear')
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
                            print(f"Você não tem dinheiro na mão, Foi descontado de sua conta os R${perda:.2f}.")
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
                        os.system('cls' if os.name == 'nt' else 'clear')
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
                            print(f"Você não tem dinheiro na mão, Foi descontado de sua conta os R${perda:.2f}.")
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
                        os.system('cls' if os.name == 'nt' else 'clear')
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
                    print(f"Valor da entrega R${escolhavalor:.2f}")
                print(f"\nGASOLINA POR VIAGEM R${posto:.2f}\n")
                
                x = input("Quantas vezes gostaria de fazer a viagem?|ENTER PARA SAIR\n: ")
                if x == "":
                    atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
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
                        print(f"Você obteve R${lucro:.2f} de lucro!")
                        print(f"SALDO ATUAL: R${carteira["Bolso"]:.2f}")
                        sleep(3)
                        limpar()
                        salvar_dados("carteira", carteira)
                    else:
                        print(f"Você obteve R${lucro:.2f} de PREJUÍZO!")
                        print(f"SALDO ATUAL: R${carteira["Bolso"]:.2f}")
                        sleep(3)
                        limpar()
                        salvar_dados("carteira", carteira)
                        saldo = carteira["Bolso"]
                        if saldo <=0:
                            carteira["Banco"] += lucro
                            print(f"você não possui dinheiro, foram descontados os R${lucro:.2f} de sua conta\nSeus fundos contam: R${carteira["Banco"]:.2f} ATUALMENTE")
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
            if not "Picareta" in Garagem:
                print("selecione um valor válido")
                input("ENTER PARA CONTINUAR")
                continue
            else:
                trabalho = True
                os.system('cls' if os.name == 'nt' else 'clear')
                digitar("Você está entrando em uma caverna...")
                sleep(2)
                digitar("Cuidado")
                sleep(3)
                default_caixa = []
                caixa = carregar_dados("caixa",default_caixa)
                tentativas = 0
                while trabalho:
                    
                    tipos_D = {"Diamante pequeno": 800,"Diamante Médio": 2300,"Diamante Grande": 8900,"Diamante Negro":10000}
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("MINERAÇÃO".center(30,"="))
                    chance_D = randint(1,100)
                    Decisao = input("ENTER para MINERAR| 0 PARA SAIR | Ver caixa [1]\n: ")
                    if Decisao == "1":
                        total = 0
                        for d in caixa:
                            D = tipos_D[d]
                            print(f"{d}: R${D:.2f}")
                            total +=D
                        print("_"*40)
                        menu_mine = input(f"| Total: R${total:.2f} | ENTER PARA SAIR| [1] Vender tudo |")
                        print("_"*40)
                        if menu_mine == "1":
                            if not caixa:
                                print("Não tem nada aqui,ta querendo vender o que, doido?")
                                sleep(3)
                            else:
                                carteira["Bolso"] += total
                                print(f"Você recebeu R${total:.2f}.")
                                caixa = []
                                salvar_dados("caixa",caixa)
                                sleep(1.9)
                        else:
                            os.system('cls' if os.name == 'nt' else 'clear')
                    else:
                        if Decisao == "0":
                            atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
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
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                elif chance_D == 10:
                                    print("Você achou um diamante grande!")
                                    sleep(2)
                                    caixa.append("Diamante Grande")
                                    salvar_dados("caixa",caixa)
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                elif chance_D == 15:
                                    print("Você achou um diamante médio!")
                                    sleep(2)
                                    caixa.append("Diamante Médio")
                                    salvar_dados("caixa",caixa)
                                    os.system('cls' if os.name == 'nt' else 'clear')                            
                                elif chance_D == 40:
                                    print("Você achou um diamante pequeno!")
                                    sleep(2)
                                    caixa.append("Diamante pequeno")
                                    salvar_dados("caixa",caixa)
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                else:
                                    print("Você achou nada aqui! Bata de novo.")
                                    sleep(2)
                                    os.system('cls' if os.name == 'nt' else 'clear')
                            else:
                                for tempo in range(20, 0, -1):
                                    print(f"\rDescanse um pouco... Espere {tempo} segundos para recuperar o fôlego", end="")
                                    sys.stdout.flush()
                                    sleep(1)
                                tentativas = 0
                                os.system('cls' if os.name == 'nt' else 'clear')
        if escolha == "13":#Mineração bit coin
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
                                    
                                    print(f"Você selecionou {nome_item} - Preço: R${preco:.2f}")
                                    confirmar = input(f"Confirmar Venda de {nome_item}? S/N: ").upper()
                                    if confirmar == "S":
                                        carteira["Bolso"] += preco
                                        salvar_dados("carteira",carteira)
                                        print(f"Você recebeu R${preco:.2f}")
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
                                print(f"[{i}] {placa}: R${valor:.2f}")
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
                                    print(f"Você selecionou {nome_item} - Preço: R${preco:.2f}")
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
                                            print(f"• {moeda}: {saldo:.6f}| R$ {val:.2f}") # 6 casas decimais para os fragmentos

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
                                    
                                    print(f"\nVocê recebeu R${total_venda:.2f}")
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
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
                        trabalho = False
                        break
        if escolha == "14":#Frete com Caminhão
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
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
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
                            multiplicador_prejuizo = {"D": 1.0, "F": 1.5, "S": 2.5, "Z": 5.0}
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
                                print(f"[{i}] {carga} | R${valor:.2f} |categoria: {letra} ")
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
                                                print(f"\n[Houve dano na carga, isso será descontado no seu pagamento no valor de R${prejuízo:.2f}]")
                                                
                                                sleep(5)
                                                limpar()
                                            else:
                                                pass
                                        elif velocidade == "2":
                                            risco = randint(1,100)
                                            barra_viagem(tempo_viagem/2)
                                            sleep(1)
                                            if risco >(33 - bonus_risco):
                                                prejuízo = round(uniform(900.40,1400.99)* fator, 2)
                                                pagamento_final -= prejuízo
                                                print(f"\n[Houve choque da carga com um obstáculo, isso será descontado no seu pagamento no valor de R${prejuízo:.2f}]")
                                                
                                                sleep(5)
                                                limpar()
                                            else:
                                                bonus = pagamento_final * 0.6
                                                pagamento_final += bonus
                                                print(f"\n[Você chegou rápido e inteiro, o bonûs foi de R${bonus:.2f}]")
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
                                            print(f"\nVocê decidiu ir mais lento, o desconto dos 10% foram de R${desconto_no_pagamento:.2f}")
                                            sleep(4)
                                            limpar()
                                            if risco >(92-bonus_risco):
                                                prejuízo = round(uniform(40.40,100.99)* fator, 2)
                                                pagamento_final -= prejuízo
                                                print(f"\n[Houve um arranhão na carga, isso será descontado no seu pagamento no valor de R${prejuízo:.2f}]")
                                                
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
                                                print(f"Entrega feita com sucesso, você recebeu R${pagamento_final:.2f}")

                                            else:
                                                print(f"Entrega feita com turbulência, você recebeu R${pagamento_final:.2f}, mas com R${prejuízo:.2f} de prejuízo...")
                                            carteira["Bolso"] += pagamento_final
                                            salvar_dados("carteira",carteira)
                                        else:
                                            print(f"Entrega fracassada, houve apenas R${pagamento_final:.2f} de PREJUÍZO")
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
                                status = f"R${valor:.2f}" if carteira_motorista.get(licença) != True else "[COMPRADO]"
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
                        p_exibir = f"R$ {p_pago:.2f}" if qtd > 0 else "---"
                        print(f"[{i}] {item:<15} | R$ {valor:<10.2f} | {qtd:<5} un (Pago: R${p_exibir})")
                    print("-" * 50)
                    print("DICA: aperte/segure [ENTER] para atualizar ou manter atualizado a info. dos preços.\n")
                    tel = input("S - Sair | C - Comprar | V/VT - Vender/Vender Tudo: ").lower()
                    if tel == "s":
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
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
                            telbuy = input(f"O valor é R${custo_total:.2f}, deseja comprar?\nS/N >>> ").upper()
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
                                
                                print(f"Você vendeu {qtd_venda} de {alvo} por R$ {valor_venda:.2f}")
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
                            print(f"Total recebido: R$ {total_geral_venda:.2f}")
                        else:
                            print("Você não tem nada em estoque para vender!")
                            
                        sleep(3)
                        limpar()
        if escolha == "16":# Bike boy
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
                        print(f"[{_}] Valor da entrega R${escolhavalor:.2f} KM:{escolhadistancia}")
                    
                    
                    x = input("Qual viagem gostaria de fazer?|ENTER PARA SAIR| D para descansar\n>>>: ").strip().upper()
                    if x == "": #SAIR
                        atualizar_nuvem(nome, carteira["Bolso"], carteira["Banco"], Garagem, zerar)
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
                            passagem = input(f"Você selecionou a corrida {x}\nValor R${valor_final:.2f} | {km_final} KM\n Continuar S/N >>> ").upper().strip()
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
                                    print(f"\nViagem tranquila! Fadiga restante: {fadiga}\nR${valor_final:.2f} Ganho!")
                                else:
                                    deficit = custo_fadiga - fadiga
                                    fadiga = 0
                                    multa = valor_final * 0.7 
                                    valor_ganho = valor_final - multa
                                    valor_ganho_falso_positivo = abs(valor_ganho)
                                    if valor_ganho_falso_positivo > carteira["Bolso"]:
                                        print(f"\nVocê não possui dinheiro para multa, aplicamos ela em sua conta. No valor de R${valor_ganho:.2f}")
                                        carteira["Banco"] -= valor_ganho
                                    else:
                                        carteira["Bolso"] -= valor_ganho
                                    print(f"\nVOCÊ EXAUSTOU! Faltou {deficit} de energia.")
                                    print(f"Multa por cansaço: R${multa:.2f} - Valor da entrega: R${valor_final:.2f} = R${valor_ganho:.2f}")
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
        if escolha == "R":
            limpar()
            ver_ranking(nome)


def menu_hub():
    while True:
        limpar()
        print("MENU".center(50,"-"))
        escolha = input("[1] PRINCIPAL| JOGO DA VIDA\n[2]Versão do jogo\n>>> ")
        if escolha == "1":
            Jogo_principal()
        if escolha == "2":
            limpar()
            print("Versão: 11V | Paciência de Rodolfo Cavalcanti")
            input("ENTER")
            continue
        else:
            limpar()
            print("Dê uma alternativa válida.")
            sleep(2)
if __name__ == "__main__":
    menu_hub()
