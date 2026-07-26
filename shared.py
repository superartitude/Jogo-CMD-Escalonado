import base64
import json
import pymongo

LINK_MONGO =  "mongodb+srv://superartitude_db_user:123Mongo@cluster0.tbesz68.mongodb.net/?appName=Cluster0"
client = pymongo.MongoClient(LINK_MONGO)
db = client.get_database('jogo_vida')
ranking_col = db.ranking


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
            zerou = j.get('Zerou', 0)
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