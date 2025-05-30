import sqlite3
import requests
import urllib3
from openpyxl import Workbook
from datetime import datetime

# Desativa avisos SSL temporariamente (caso necessário)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===== Parte 1: API de países =====

def extrair_dados_paises():
    conn = sqlite3.connect("paises.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paises (
            nome_comum TEXT,
            nome_oficial TEXT,
            capital TEXT,
            continente TEXT,
            regiao TEXT,
            sub_regiao TEXT,
            populacao INTEGER,
            area REAL,
            moeda_nome TEXT,
            moeda_simbolo TEXT,
            idioma TEXT,
            fuso_horario TEXT,
            url_bandeira TEXT
        )
    """)

    for i in range(3):
        pais = input(f"Digite o nome do país #{i+1}: ").strip()

        try:
            resposta = requests.get(f"https://restcountries.com/v3.1/name/{pais}", verify=False)
            dados = resposta.json()[0]

            nome_comum = dados["name"]["common"]
            nome_oficial = dados["name"]["official"]
            capital = dados.get("capital", ["N/A"])[0]
            continente = dados.get("continents", ["N/A"])[0]
            regiao = dados.get("region", "N/A")
            sub_regiao = dados.get("subregion", "N/A")
            populacao = dados.get("population", 0)
            area = dados.get("area", 0)
            moedas = list(dados.get("currencies", {}).values())[0]
            moeda_nome = moedas.get("name", "N/A")
            moeda_simbolo = moedas.get("symbol", "N/A")
            idioma = list(dados.get("languages", {}).values())[0]
            fuso_horario = dados.get("timezones", ["N/A"])[0]
            url_bandeira = dados.get("flags", {}).get("png", "N/A")

            cursor.execute("""
                INSERT INTO paises VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome_comum, nome_oficial, capital, continente, regiao, sub_regiao,
                  populacao, area, moeda_nome, moeda_simbolo, idioma, fuso_horario, url_bandeira))

            print(f"✅ Dados de {nome_comum} salvos com sucesso.\n")

        except Exception as e:
            print(f"Erro ao buscar dados de '{pais}': {e}")

    conn.commit()
    conn.close()

    
# ===== Parte 2: Web Scraping dos livros =====

from bs4 import BeautifulSoup
import sqlite3
import requests

def extrair_dados_livros():
    conn = sqlite3.connect("livraria.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            titulo TEXT,
            preco TEXT,
            avaliacao TEXT,
            disponibilidade TEXT
        )
    """)

    url_base = "https://books.toscrape.com/"
    resposta = requests.get(url_base)
    sopa = BeautifulSoup(resposta.content, "html.parser")
    livros = sopa.find_all("article", class_="product_pod")[:10]

    for livro in livros:
        titulo = livro.h3.a["title"]
        preco = livro.find("p", class_="price_color").text.strip()
        avaliacao = livro.p["class"][1]
        disponibilidade = livro.find("p", class_="instock availability").text.strip()

        cursor.execute("""
            INSERT INTO livros VALUES (?, ?, ?, ?)
        """, (titulo, preco, avaliacao, disponibilidade))

        print(f"📚 Livro salvo: {titulo}")

    conn.commit()
    conn.close()

def gerar_relatorio_excel():
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Países"

    # Cabeçalho do relatório
    ws1.append(["Relatório Gerado por: SEU_NOME_AQUI"])
    ws1.append(["Data de geração:", datetime.now().strftime("%d/%m/%Y %H:%M")])
    ws1.append([])

    # Tabela de países
    ws1.append(["Nome Comum", "Nome Oficial", "Capital", "Continente", "Região", "Sub-região",
                "População", "Área", "Moeda", "Símbolo", "Idioma", "Fuso Horário", "Bandeira"])

    conn = sqlite3.connect("paises.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paises")
    for row in cursor.fetchall():
        ws1.append(row)
    conn.close()

    # Nova aba para livros
    ws2 = wb.create_sheet(title="Livros")
    ws2.append(["Título", "Preço", "Avaliação", "Disponibilidade"])

    conn = sqlite3.connect("livraria.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    for row in cursor.fetchall():
        ws2.append(row)
    conn.close()

    # Salvar o arquivo
    wb.save("relatorio_final.xlsx")
    print("📄 Relatório gerado com sucesso: relatorio_final.xlsx")

# ===== Execução principal =====

if __name__ == "__main__":
    print("🔎 Iniciando extração de dados de países...")
    extrair_dados_paises()

    print("\n🔎 Iniciando extração de dados de livros...")
    extrair_dados_livros()

    print("\n✅ Etapas 1 e 2 concluídas. Arquivos 'paises.db' e 'livraria.db' gerados.")
    
    print("\n📄 Gerando relatório final em Excel...")
    gerar_relatorio_excel()

