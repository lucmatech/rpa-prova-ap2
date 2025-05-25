# 🤖 Projeto RPA - Extração de Dados de Países e Livros

Este projeto foi desenvolvido como parte da atividade da disciplina de **RPA (Automação de Processos Robóticos)**. Ele tem como objetivo automatizar a coleta de dados públicos de forma estruturada, usando duas técnicas:

- **API REST** para buscar dados sobre países
- **Web Scraping** para coletar informações de livros

---

## 📌 Parte 1 – Extração de Dados via API REST

Neste módulo, o sistema solicita ao usuário que informe o nome de 3 países. Para cada país, ele consulta a [REST Countries API](https://restcountries.com/) e extrai as seguintes informações:

- Nome comum e oficial
- Capital
- Continente
- Região e sub-região
- População e área
- Moeda (nome e símbolo)
- Idioma principal
- Fuso horário
- URL da bandeira

Esses dados são armazenados localmente no banco de dados **SQLite**, no arquivo `paises.db`, na tabela `paises`.

---

## 📘 Parte 2 – Web Scraping com BeautifulSoup

Nesta etapa, usamos a biblioteca **BeautifulSoup** para acessar o site [Books to Scrape](https://books.toscrape.com/) e extrair informações dos **10 primeiros livros da página principal**, incluindo:

- Título
- Preço
- Avaliação (quantidade de estrelas)
- Disponibilidade

Essas informações são salvas no banco de dados **SQLite**, no arquivo `livraria.db`, na tabela `livros`.

---

## 🧠 Tecnologias Utilizadas

- Python 3
- SQLite3
- Requests
- BeautifulSoup
- REST Countries API
- Site Books to Scrape (web scraping)

---

## 🔧 Execução

Para rodar o projeto localmente:

```bash
python projeto_rpa.py
