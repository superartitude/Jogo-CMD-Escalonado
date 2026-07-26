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
default_Garagem = {}
Garagem = carregar_dados("garagem", default_Garagem)
default_carteira = {"Bolso": 0.0, "Banco": -1400.0}
carteira = carregar_dados("carteira", default_carteira)
default_nome = "user"
nome = carregar_dados("nome",default_nome)
default_licenças = {"Trabalho1":True, "Trabalho2":False,"Trabalho3":False,"Trabalho4":False,"Carteira D":False}
licenças = carregar_dados("licencas", default_licenças)
ALERTA_COMMODITIES_PRONTO = ""
NOTICIA_ATUAL_BOLSA = "Mercado Estável"
def thread_monitorar_bolsa():
    global ALERTA_COMMODITIES_PRONTO, NOTICIA_ATUAL_BOLSA
    
    # Valores padrão exatos do seu jogo
    default_estoque_agro = {"Petroleo": 0, "Minerio": 0, "Soja": 0, "Algodao": 0, "Feno": 0}
    default_historico_precos = {"Petroleo": 0.0, "Minerio": 0.0, "Soja": 0.0, "Algodao": 0.0, "Feno": 0.0}
    default_mercado = {"precos": {"Petroleo": 1500.0, "Minerio": 800.0, "Soja": 350.0, "Algodao": 120.0, "Feno": 40.0}, "noticia": "Mercado Estável"}

    while True:
        try:
            # 0. Primeiro ele precisa ter o telefone.
            if "Telefone" not in Garagem:
                ALERTA_COMMODITIES_PRONTO = ""
                NOTICIA_ATUAL_BOLSA = "Acesso bloqueado (Sem Telefone)."
                sleep(5)
                continue
            # 1. Puxa os dados ao vivo do mercado e as compras do usuário
            estoque_agro = carregar_dados("estoque agro", default_estoque_agro)
            historico_precos = carregar_dados("Historico preços", default_historico_precos)
            mercado_ao_vivo = carregar_dados("mercado_ao_vivo", default_mercado)
            
            precos_ao_vivo = mercado_ao_vivo["precos"]
            NOTICIA_ATUAL_BOLSA = mercado_ao_vivo["noticia"]

            # 2. Faz a conta matemática em segundo plano (escondido do LLM)
            alertas = []
            for item, qtd in estoque_agro.items():
                if qtd > 0:
                    p_pago = historico_precos.get(item, 0.0)
                    p_atual = precos_ao_vivo.get(item, 0.0)
                    
                    # Se estiver valendo mais do que o usuário pagou, gera o alerta em texto puro
                    if p_atual > p_pago:
                        lucro_total = (p_atual - p_pago) * qtd
                        alertas.append(f"O jogador tem {qtd} un de {item}. Comprou por R${p_pago:.2f} e agora vale R${p_atual:.2f}. Lucro atual de R${lucro_total:.2f} se vender tudo.")

            # 3. Salva o resultado na variável global como texto simples
            if alertas:
                ALERTA_COMMODITIES_PRONTO = "\n".join(alertas)
            else:
                ALERTA_COMMODITIES_PRONTO = "Nenhuma oportunidade de lucro alto no estoque atual."
                
        except Exception:
            pass  # Evita que a thread quebre se ler o arquivo enquanto ele é gravado
            
        sleep(2) # Atualiza a cola a cada 2 segundos
# INICIALIZA A THREAD ASSIM QUE O ARQUIVO DO RODOLFO ABRE
t = threading.Thread(target=thread_monitorar_bolsa, daemon=True)
t.start()
MANUAL_BASE = """
========================
MANUAL DO JOGO
"A ARTE DO CAPITALISMO"
========================

OBJETIVO FINAL
- Comprar o item "Globo Terrestre".
- Valor: R$ 1.000.000.000,00.

====================================
BANCO
====================================

- Saldo bancário negativo = dívida.
- Enquanto houver dívida, o dinheiro guardado NÃO rende.
- Quanto maior o saldo positivo, maior o rendimento.
- Ao atingir R$ 25.000,00 ou mais no banco, passa a existir cobrança de imposto sobre o saldo.

====================================
FORMAS DE GANHAR DINHEIRO
====================================

TRABALHOS FÁCEIS
- Gratuito.
- Não precisa licença.
- Exercício: Soma.
- Pagamento: R$ 5,40 até R$ 50,30.

TRABALHOS MÉDIOS
- Requer licença "Trabalhos Médios".
- Exercício: Multiplicação.
- Pagamento: R$ 60,40 até R$ 130,99.

TRABALHOS DIFÍCEIS
- Requer licença "Trabalhos Difíceis".
- Exercício: Divisão.
- Pagamento: R$ 300,40 até R$ 540,99.

DESAFIO DO TESOURO
- Requer licença "Desafio do Tesouro".
- Tempo limite: 30 segundos.
- Contém:
    • 1 soma
    • 1 multiplicação
    • 1 divisão
- Cada erro reduz os ganhos.
- Errar tudo ou acabar o tempo pode resultar em recompensa zero.
- Pagamento: R$ 1.000,40 até R$ 4.000,99.

====================================
LICENÇAS
====================================

Trabalhos Médios ............ R$ 800
Trabalhos Difíceis .......... R$ 3.000
Desafio do Tesouro .......... R$ 10.000

IMPORTANTE
Sempre que o jogador possuir dinheiro suficiente para comprar a próxima licença, incentive essa compra.
"""
INST_PICARETA = """
PICARETA

- Atividade: Mineração.
- Não possui custo.
- Pode encontrar diamantes de até R$ 10.000.
- Todo o lucro é líquido.
- O jogador pode realizar até 3 tentativas consecutivas de mineração.
- Após a terceira tentativa, a mineração fica indisponível por 10 segundos para descanso.
- Enquanto durar o descanso, nenhuma nova tentativa pode ser realizada.
"""
INST_BARCO = """
BARCO DE PESCA

- Atividade: Pesca.
- Custo inicial: R$ 100.
- Peixes maiores possuem maior valor.
- Quanto maior o peixe, menor a chance de capturá-lo.
- Se falhar, o jogador paga pelos danos da tentativa.
"""
INST_MOTO = """
MOTO

- Atividade: Entregas.
- Gasolina custa entre R$ 40 e R$ 100.
- Cada entrega paga entre R$ 30 e R$ 120.
- Gasolina cara pode gerar prejuízo.
"""
INST_PC = """
PC

- Atividade: Mineração de criptomoedas.
- Permite comprar placas de vídeo.
- Cada placa pode custar até R$ 100.000.
- Mais placas aumentam a velocidade de mineração.
"""
INST_CAMINHAO = """
CAMINHÃO

- Atividade: Fretes.
- Requer Carteira D.
- Carteira D custa R$ 1.200.
- Também exige R$ 1.000 disponíveis para iniciar.
- Carteiras superiores liberam fretes mais valiosos.
- Fretes melhores também aumentam o risco de prejuízo.
"""
INST_TELEFONE = """
TELEFONE

- Atividade: Bolsa de Commodities.
- Permite negociar petróleo, algodão, minério de ferro e outros produtos.
- Sempre avise imediatamente quando surgir uma oportunidade muito lucrativa.
"""
INST_BIKE = """
BICICLETA

- Atividade: Bike Boy (Entregas).
- Entregas comuns pagam até R$ 40,30.
- Entregas raras podem pagar até R$ 100,30.
- Cada quilômetro percorrido consome 1 ponto de Fadiga.
- Se a Fadiga chegar a 0 durante uma entrega, o jogador sofre exaustão.
- Enquanto estiver exausto, será necessário utilizar a opção "Descansar" antes de continuar trabalhando.
"""
DIRETRIZ_FINAL = """
========================
PERSONALIDADE
========================

Você é Rodolfo.

Características:
- Mentor capitalista.
- Velho rabugento.
- Formal.
- Frio.
- Sarcástico.
- Humor seco ocasional.

========================
ESTILO DAS RESPOSTAS
========================

OBRIGATÓRIO

- Responder em apenas UMA linha.
- Máximo de 20 palavras.
- Nunca usar emojis.
- Nunca usar palavrões.
- Nunca usar linguagem técnica.
- Nunca mencionar variáveis ou funcionamento interno do jogo.
- Nunca dizer:
    Trabalho1
    Trabalho2
    Trabalho3
    Trabalho4

========================
REGRAS
========================

- Nunca invente mecânicas.
- Use apenas informações presentes no manual.
- Nunca sugira algo que quebre a economia.
- Evite repetir o saldo do jogador.
- Sempre priorize aumentar os lucros.

========================
QUANDO ACONSELHAR
========================

- Se puder comprar a próxima licença, incentive.
- Se houver dívida, priorize quitá-la.
- Se aparecer excelente oportunidade na Bolsa de Commodities, avise imediatamente.
- Se possuir o Globo Terrestre, parabenize pela vitória.

========================
QUANDO NÃO HOUVER NADA IMPORTANTE
========================

Alterne entre:

- curiosidades de história;
- natureza;
- ciência;
- física;

ou

- comentar o Ranking Global.

Se estiver entre os primeiros:
- elogie.

Caso contrário:
- compare com jogadores mais ricos.
- invente hipóteses engraçadas para explicar por que eles ganharam mais dinheiro.

Nunca utilize palavrões.
"""
if getattr(sys, 'frozen', False):
    pasta_base = sys._MEIPASS
else:
    pasta_base = os.path.dirname(os.path.abspath(__file__))
SUBPASTA = "llama-b9637-bin-win-cpu-x64"
# Mudamos para o llama-server que mantém o modelo aberto na RAM!
motor_server = os.path.join(pasta_base, SUBPASTA, "llama-server.exe")
modelo_ia = os.path.join(pasta_base, "gemma-2-2b-it-Q4_K_M.gguf")
os.system('cls' if os.name == 'nt' else 'clear')
print("Carregando Assistente... Por favor, aguarde.")
# Inicia o servidor em segundo plano de forma oculta
comando_server = [motor_server, "-m", modelo_ia, "--port", "8080", "-c", "2048", "-ngl", "0"]
server_process = subprocess.Popen(
    comando_server,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    stdin=subprocess.DEVNULL
)
# Espera o servidor subir testando a conexão
for _ in range(30):
    try:
        urllib.request.urlopen("http://localhost:8080/health", timeout=1)

        break
    except:
        sleep(1)
def conversar_com_rodolfo(mensagem_usuario=""):
    nomes_comerciais = {
    "Trabalho1": "Trabalhos fáceis",
    "Trabalho2": "Trabalhos Médios",
    "Trabalho3": "Trabalhos Difíceis",
    "Trabalho4": "Desafio do Tesouro"
    }
    global ALERTA_COMMODITIES_PRONTO, NOTICIA_ATUAL_BOLSA
    Garagem = carregar_dados("garagem", default_Garagem)
        
    carteira = carregar_dados("carteira", default_carteira)
        
    nome = carregar_dados("nome",default_nome)
        
    licenças = carregar_dados("licencas", default_licenças)

    texto_do_ranking = puxar_ranking_para_rodolfo(nome)
    url = "http://localhost:8080/completion"
    status_garagem = "Vazia" if not Garagem else Garagem
    lista_licencas = ", ".join([nomes_comerciais.get(k, k) for k, v in licenças.items() if v]) if isinstance(licenças, dict) else "Nenhuma"
    info_jogador = f"""SITUAÇÃO ATUAL DO JOGADOR:
- Nome: {nome}
- Dinheiro no Bolso: R$ {carteira['Bolso']}
- Licenças de trabalho ativas: {lista_licencas}
- Saldo no Banco: R$ {carteira['Banco']}
- Itens na Garagem: {status_garagem}
"""
    
    info_jogador += f"\n\nPLACAR DO RANKING GLOBAL (TOP 10 COMPETIDORES AO VIVO):\n{texto_do_ranking}\n"
    
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
    # Se a garagem estiver vazia, ele avisa no texto do manual
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
    # Fecha o manual colando a diretriz do Rodolfo no final
    MANUAL_FINAL += "\n" + DIRETRIZ_FINAL
    if  "GLOBO TERRESTRE" in Garagem:
        comando_vitoria = (
            "ATENÇÃO CRÍTICA: O jogador COMPROU o GLOBO TERRESTRE e ZEROU o jogo! "
            "Esqueça todas as dicas de farmar ou trabalhar. Parabenize-o pela vitória absoluta "
            "com o seu tom de velho ranzinza orgulioso, reconhecendo que ele agora é o SOBERANO DA ECONOMIA."
        )
    else:
        comando_vitoria = "Diga o seu conselho financeiro atual baseando-se estritamente na situação do jogador."

    prompt = (
        f"<bos><start_of_turn>user\n"
        f"{MANUAL_FINAL}\n"
        f"{info_jogador}\n"
        f"Você é Rodolfo. Instruções: {comando_vitoria}<end_of_turn>\n"
        f"<start_of_turn>model\n"
        f"Rodolfo: "
    )
    
    corpo_requisicao = {
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.7,
        "stream": False # Garante que ele envie a resposta de uma vez só
    }
    
    # 2. Transforma em JSON garantindo que os acentos fiquem em formato UTF-8 puro (ensure_ascii=False)
    dados_json = json.dumps(corpo_requisicao, ensure_ascii=False).encode("utf-8")
    
    # 3. Configura a requisição HTTP oficial
    req = urllib.request.Request(url, data=dados_json, headers={'Content-Type': 'application/json; charset=utf-8'})
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resposta:
            resultado = json.loads(resposta.read().decode("utf-8"))
            texto = resultado.get("content", "").strip()
            texto_limpo = texto.replace("<end_of_turn>", "").replace('"', '').strip()
            texto_sem_emojis = "".join(c for c in texto_limpo if c.isalnum() or c in " .,;:!?()'-$R$+-/%")
            return texto_sem_emojis.strip()
    except Exception as e:
        return f"Um satélite saiu de órbita... (Erro: {e})"
# === LOOP DO CHAT INSTANTÂNEO ===
try:
    while True:
        
        

        # Puxa o conselho atualizado com base no save
        resposta = conversar_com_rodolfo()
        
        # Desenha a interface limpa no terminal lateral
        os.system('cls' if os.name == 'nt' else 'clear')
        
        texto_limpo = f"Rodolfo diz: \"{resposta}\""
        linhas_texto = textwrap.wrap(texto_limpo, width=50)
        largura = 56 # Garante um tamanho mínimo bonito
        
        print("╔" + "═" * (largura - 2) + "╗")
        print("║" + " MENTOR FINANCEIRO: RODOLFO CAVALCANTI ".center(largura - 2, " ") + "║")
        print("╠" + "═" * (largura - 2) + "╣")
        print("║" + "".center(largura - 2, " ") + "║")
        
        # 3. Imprime cada pedaço do texto centralizado e envelopado na borda
        for linha in linhas_texto:
            print("║" + f" {linha} ".center(largura - 2, " ") + "║")
            
        print("║" + "".center(largura - 2, " ") + "║")
        print("╚" + "═" * (largura - 2) + "╝")
        
        # Tempo para a próxima análise do jogo
        tempo = random.randint(7,20)
        sleep(tempo)    
except (EOFError, KeyboardInterrupt):
    pass
finally:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Desligando assistente...")
    server_process.terminate()
    server_process.wait()