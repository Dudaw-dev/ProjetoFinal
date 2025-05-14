import requests
import os
from dotenv import load_dotenv

load_dotenv()

def buscar_noticias(tema, quantidade):
    """
    Função para buscar as noticias da API
    Recebendo o tema e a quantidade de noticias que o usuário solicitar
    Retorna com as noticias
    """
    api_key = os.getenv("API_KEY_NEWS")
    
    if not api_key:
        raise ValueError("API Key não encontrada nas variáveis de ambiente.")

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": tema,
        "pageSize": quantidade,
        "sortBy": "publishedAt",
        "language": "pt",
    }

    headers = {
        'x-api-key': api_key
    }

    resposta = requests.get(url=url, headers=headers, params=params)

    if resposta.status_code != 200:
        print(f"Erro na requisição: {resposta.status_code}")
        return []

    artigos = resposta.json().get("articles", [])
    return artigos

def exibir_noticias(artigos):
    """
    Função para mostrar as noticias
    Recebe as noticias da busca de noticias
    """
    if not artigos:
        print("Nenhuma notícia encontrada para esse tema.")
        return

    for i, artigo in enumerate(artigos, 1):
        titulo = artigo.get("title", "Sem título")
        fonte = artigo.get("source", {}).get("name", "Fonte desconhecida")
        autor = artigo.get("author", "Autor desconhecido")
        url = artigo.get("url", "Link indisponível")
        print(f"\nNotícia {i}:")
        print(f"Título: {titulo}")
        print(f"Autor: {autor}")
        print(f"Fonte: {fonte}")
        print(f"Link: {url}")

def menu():
    """
    Função para menu interativo
    Usuário indica quantas noticias deseja ver 
    Noticias armazenadas no histórico
    """
    historico_noticias = []
    total_noticias = 0

    print("MENU DE NOTÍCIAS")

    while True:
        tema = input("\nDigite um tema para buscar notícias (ou 'sair' para finalizar): ").strip()

        if tema.lower() == 'sair':
            break

        while True:
            try:
                quantidade = int(input("Quantas notícias deseja ver? (1 a 10): "))
                if 1 <= quantidade <= 10:
                    break
                else:
                    print("Digite um número entre 1 e 10.")
            except ValueError:
                print("Por favor, digite um número válido.")

        print(f"\nBuscando {quantidade} notícia(s) sobre: '{tema}'...\n")
        
        noticias = buscar_noticias(tema, quantidade)
        exibir_noticias(noticias)

        historico_noticias.append((tema, len(noticias)))
        total_noticias += len(noticias)

    print("Temas pesquisados: ")
    
    for tema, qtd in historico_noticias:
        print(f"Tema: {tema} - {qtd} notícia(s)")
    print(f"\nTotal de notícias buscadas: {total_noticias}")
    print("Obrigado por usar o sistema!")

#principal
if __name__ == "__main__":
    menu()