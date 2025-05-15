import requests

usuarios = {
    1: {"email": "duda@tech.com", "senha": "senha"},
    2: {"email": "nessa@tech.com", "senha": "senha"},
    3: {"email": "alice@tech.com", "senha": "senha"},
}

interacoes = {
    "posts_visualizados": 0,
    "comentarios_visualizados": 0,
    "posts_criados": 0
}

def verificar_login():
    """
    Função para verificar se o login é válido
    Recebe login indicado pelo usuário
    """
    print("Login")
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()
    for user_id, dados in usuarios.items():
        if dados["email"] == email and dados["senha"] == senha:
            print("Login bem-sucedido!\n")
            return user_id
    print("Usuário ou senha inválidos.\n")
    return None

def get_data(url):
    """
    Função para fazer o get e tratamento de erro
    Recebe url e verificar possivel erro
    """
    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return None

def visualizar_posts():
    """
    Função para visualizar todos os posts com limitador de 5 no total
    Recebe a url verificada (get_data)
    Retorna os 5 posts
    """
    print("\nTodos os Posts")
    posts = get_data("https://jsonplaceholder.typicode.com/posts")
    if posts:
        for post in posts[:5]:
            print(f"\nPost ID: {post['id']}\nTítulo: {post['title']}\nConteúdo: {post['body']}")
            interacoes["posts_visualizados"] += 1

def visualizar_comentarios():
    """
    Função para visualizar comentários de um post
    Usuário digita o ID do post desejado
    Apresenta os comentários
    """
    print("\nComentários de um Post")
    post_id = input("Digite o ID do post: ")
    if not post_id.isdigit():
        print("ID inválido. Deve ser um número.")
        return

    comentarios = get_data(f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments")
    if comentarios:
        for c in comentarios:
            print(f"\nComentário de: {c['email']}\n{c['body']}")
            interacoes["comentarios_visualizados"] += 1

def meus_posts(user_id):
    """
    Função para visualizar os próprios posts
    Recebe o usuário autenticado
    Retorna os posts
    """
    print("\nMeus Posts")
    posts = get_data(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")
    if posts:
        for post in posts:
            print(f"\nTítulo: {post['title']}\nConteúdo: {post['body']}")
            interacoes["posts_visualizados"] += 1

def filtrar_posts_usuario():
    """
    Função para verificar posts de um usuário escolhido pelo próprio usuário
    Usuário digita o ID desejado
    Retornar os posts
    """
    print("\nFiltrar por Usuário")
    user_id = input("Digite o ID do usuário (1-10): ")
    if not user_id.isdigit():
        print("ID inválido. Deve ser um número.")
        return

    posts = get_data(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")
    if posts:
        for post in posts[:5]:
            print(f"\nTítulo: {post['title']}\nConteúdo: {post['body']}")
            interacoes["posts_visualizados"] += 1
    else:
        print("Nenhum post encontrado para esse usuário.")

def criar_post(user_id):
    """
    Função para criar um post
    Recebe o usuário autenticado (user_id)
    Cria o post e verifica possiveis erros
    """
    print("\nCriar Novo Post")
    titulo = input("Título do post: ").strip()
    corpo = input("Conteúdo do post: ").strip()

    if not titulo or not corpo:
        print("Título e conteúdo não podem estar vazios.")
        return

    novo_post = {
        "userId": user_id,
        "title": titulo,
        "body": corpo
    }

    try:
        resposta = requests.post("https://jsonplaceholder.typicode.com/posts", json=novo_post, timeout=5)
        if resposta.status_code == 201:
            print("Post criado com sucesso!")
            interacoes["posts_criados"] += 1
        else:
            print("Erro ao criar post.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar post: {e}")

def menu_interativo(user_id):
    """
    Função para o menu interativo
    Recebe user id
    Retorna função escolhida
    """
    while True:
        print("\n=== Menu ===")
        print("1. Visualizar todos os posts")
        print("2. Visualizar comentários de um post")
        print("3. Visualizar meus próprios posts")
        print("4. Filtrar posts por outro usuário")
        print("5. Criar um novo post")
        print("6. Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            visualizar_posts()
        elif escolha == "2":
            visualizar_comentarios()
        elif escolha == "3":
            meus_posts(user_id)
        elif escolha == "4":
            filtrar_posts_por_usuario()
        elif escolha == "5":
            criar_post(user_id)
        elif escolha == "6":
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    """
    Função para indicar login e resumo das operações
    Recebe login do usuário
    Chama função do menu interativo
    Retorna com o resumo das interações realizadas
    """
    user_id = None
    while user_id is None:
        user_id = verificar_login()

    menu_interativo(user_id)

    print("\nInterações")
    print(f"Posts visualizados: {interacoes['posts_visualizados']}")
    print(f"Comentários visualizados: {interacoes['comentarios_visualizados']}")
    print(f"Posts criados: {interacoes['posts_criados']}")
    print("Encerrando programa...")

if __name__ == "__main__":
    main()