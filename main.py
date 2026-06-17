"""SGL - Sistema de Gestao Local: menu, loop principal e funcoes de dominio."""

from utils import ler_int, ler_float, proximo_id, formatar_preco
from storage import carregar_dados, salvar_dados

def buscar_produtos(produtos, texto):
    """Retorna produtos cujo nome contenha o texto informado."""
    texto = texto.strip().lower()
    return [produto for produto in produtos if texto in produto["nome"].lower()]

def listar_produtos(produtos, categoria=None):
    """Exibe os produtos ordenados por nome, com filtro opcional por categoria."""
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    alvo = produtos
    if categoria:
        categoria = categoria.strip().lower()
        alvo = [p for p in produtos if p["categoria"].lower() == categoria]
        if not alvo:
            print("Nenhum produto nessa categoria.")
            return

    produtos_ordenados = sorted(alvo, key=lambda p: p["nome"].lower())
    print("\nID | Nome | Categoria | Preco | Estoque")
    print("---|------|-----------|-------|--------")
    for produto in produtos_ordenados:
        print(
            f"{produto['id']} | {produto['nome']} | {produto['categoria']} | "
            f"{formatar_preco(produto['preco'])} | {produto['estoque']}"
        )


def listar_produtos_menu(produtos):
    """Opcao de menu: lista produtos com filtro opcional por categoria."""
    categoria = input(
        "Filtrar por categoria (Enter para listar todas): "
    ).strip()
    listar_produtos(produtos, categoria or None)


def selecionar_produto(produtos):
    """Seleciona um produto pelo ID."""
    if not produtos:
        print("Nao ha produtos cadastrados.")
        return None

    listar_produtos(produtos)
    while True:
        produto_id = ler_int("Informe o ID do produto: ", minimo=1)
        for produto in produtos:
            if produto["id"] == produto_id:
                return produto
        print("Produto nao encontrado. Tente novamente.")


def cadastrar_produto(produtos):
    """Cadastra um novo produto com validacao dos campos."""
    print("\n=== Cadastro de Produto ===")

    while True:
        nome = input("Nome: ").strip()
        if nome:
            break
        print("Erro: o nome nao pode ficar vazio.")

    categoria = input("Categoria (Alimento, Limpeza, Outros): ").strip()
    if not categoria:
        categoria = "Outros"

    preco = ler_float("Preco: ", minimo=0)
    estoque = ler_int("Estoque inicial: ", minimo=0)

    produto = {
        "id": proximo_id(produtos),
        "nome": nome,
        "categoria": categoria,
        "preco": preco,
        "estoque": estoque,
    }
    produtos.append(produto)
    print("Produto cadastrado com sucesso.")


def buscar_produto_por_nome(produtos):
    """Busca produtos por parte do nome ou por ID, sem diferenciar maiusculas."""
    print("\n=== Buscar Produto (nome ou ID) ===")
    texto = input("Digite parte do nome ou o ID: ").strip()
    if not texto:
        print("Erro: informe um texto ou ID para pesquisar.")
        return

    if texto.isdigit():
        encontrados = [p for p in produtos if p["id"] == int(texto)]
    else:
        encontrados = buscar_produtos(produtos, texto)
    if not encontrados:
        print("Nenhum produto encontrado.")
        return

    print(f"{len(encontrados)} produto(s) encontrado(s):")
    for produto in encontrados:
        print(
            f"{produto['id']} | {produto['nome']} | {produto['categoria']} | "
            f"{formatar_preco(produto['preco'])} | {produto['estoque']}"
        )


def registrar_mov(produtos, movs, tipo):
    """Registra entrada ou saida de estoque e atualiza o produto."""
    if not produtos:
        print("Nao ha produtos cadastrados para movimentacao.")
        return

    descricao = "entrada" if tipo == "E" else "saida"
    print(f"\n=== Registrar {descricao} de estoque ===")

    produto = selecionar_produto(produtos)
    if produto is None:
        return

    while True:
        quantidade = ler_int("Quantidade: ", minimo=1)
        if tipo == "S" and quantidade > produto["estoque"]:
            print("Erro: nao e possivel retirar mais do que o estoque disponivel.")
            print(f"Estoque atual: {produto['estoque']}")
            continue
        break

    data = input("Data: ").strip()
    observacao = input("Observacao (opcional): ").strip()

    movimento = {
        "id": proximo_id(movs),
        "produto_id": produto["id"],
        "tipo": tipo,
        "quantidade": quantidade,
        "data": data or "-",
        "observacao": observacao or "-",
    }
    movs.append(movimento)

    if tipo == "E":
        produto["estoque"] += quantidade
    else:
        produto["estoque"] -= quantidade

    print(f"Movimentacao de {descricao} registrada com sucesso.")


def relatorio_movimentacoes(produtos, movs):
    """Exibe todas as movimentacoes com totais de entrada e saida."""
    if not movs:
        print("Nenhuma movimentacao registrada.")
        return

    print("\n=== Relatorio de Movimentacoes ===")
    print("ID | Data | Tipo | Prod.ID | Produto | Quantidade | Observacao")
    print("---|------|------|---------|---------|------------|-----------")

    total_entradas = 0
    total_saidas = 0

    for mov in movs:
        produto = next((p for p in produtos if p["id"] == mov["produto_id"]), None)
        nome_produto = produto["nome"] if produto else "Produto removido"
        tipo_desc = "Entrada" if mov["tipo"] == "E" else "Saida"

        print(
            f"{mov['id']} | {mov['data']} | {tipo_desc} | {mov['produto_id']} | "
            f"{nome_produto} | {mov['quantidade']} | {mov['observacao']}"
        )

        if mov["tipo"] == "E":
            total_entradas += mov["quantidade"]
        else:
            total_saidas += mov["quantidade"]

    print(f"\nTotal de entradas: {total_entradas}")
    print(f"Total de saidas: {total_saidas}")


def relatorio_gerencial(produtos, movs):
    """Gera estatisticas gerenciais do estoque."""
    if not produtos:
        print("Nenhum produto cadastrado para gerar relatorio.")
        return

    print("\n=== Relatorio Gerencial ===")

    maior_estoque = max(produto["estoque"] for produto in produtos)
    menor_estoque = min(produto["estoque"] for produto in produtos)

    produtos_maior = [p for p in produtos if p["estoque"] == maior_estoque]
    produtos_menor = [p for p in produtos if p["estoque"] == menor_estoque]

    print("Produto(s) com maior estoque:")
    for produto in produtos_maior:
        print(f"- {produto['nome']} (ID {produto['id']}, estoque {produto['estoque']})")

    print("\nProduto(s) com menor estoque:")
    for produto in produtos_menor:
        print(f"- {produto['nome']} (ID {produto['id']}, estoque {produto['estoque']})")

    valor_total = sum(produto["estoque"] * produto["preco"] for produto in produtos)
    print(f"\nValor total do estoque: {formatar_preco(valor_total)}")

    categorias = {}
    for produto in produtos:
        categoria = produto["categoria"]
        categorias[categoria] = categorias.get(categoria, 0) + 1

    print("\nQuantidade de produtos por categoria:")
    for categoria, quantidade in sorted(categorias.items()):
        print(f"- {categoria}: {quantidade}")

    top_valor = sorted(
        produtos,
        key=lambda produto: produto["estoque"] * produto["preco"],
        reverse=True,
    )[:3]

    print("\nTop 3 produtos com maior valor em estoque:")
    for produto in top_valor:
        valor_produto = produto["estoque"] * produto["preco"]
        print(f"- {produto['nome']} (ID {produto['id']}): {formatar_preco(valor_produto)}")


def editar_produto(produtos):
    """Edita preco e/ou categoria de um produto existente."""
    print("\n=== Editar Produto ===")
    produto = selecionar_produto(produtos)
    if produto is None:
        return

    print(f"Editando: {produto['nome']} (deixe em branco para manter o valor atual)")

    nova_categoria = input(
        f"Nova categoria [{produto['categoria']}]: "
    ).strip()
    if nova_categoria:
        produto["categoria"] = nova_categoria

    resp = input(f"Alterar preco (atual {formatar_preco(produto['preco'])})? (s/N): ")
    if resp.strip().lower() == "s":
        produto["preco"] = ler_float("Novo preco: ", minimo=0)

    print("Produto atualizado com sucesso.")


def montar_relatorio_texto(produtos, movs):
    """Monta o conteudo textual dos relatorios para exportacao."""
    linhas = ["=== SGL - Relatorio Geral ===", ""]

    linhas.append("--- Produtos ---")
    if produtos:
        for produto in sorted(produtos, key=lambda p: p["nome"].lower()):
            linhas.append(
                f"{produto['id']} | {produto['nome']} | {produto['categoria']} | "
                f"{formatar_preco(produto['preco'])} | estoque {produto['estoque']}"
            )
    else:
        linhas.append("Nenhum produto cadastrado.")

    linhas.append("")
    linhas.append("--- Movimentacoes ---")
    total_entradas = 0
    total_saidas = 0
    if movs:
        for mov in movs:
            produto = next((p for p in produtos if p["id"] == mov["produto_id"]), None)
            nome_produto = produto["nome"] if produto else "Produto removido"
            tipo_desc = "Entrada" if mov["tipo"] == "E" else "Saida"
            linhas.append(
                f"{mov['id']} | {mov['data']} | {tipo_desc} | {mov['produto_id']} | "
                f"{nome_produto} | {mov['quantidade']} | {mov['observacao']}"
            )
            if mov["tipo"] == "E":
                total_entradas += mov["quantidade"]
            else:
                total_saidas += mov["quantidade"]
    else:
        linhas.append("Nenhuma movimentacao registrada.")

    linhas.append("")
    linhas.append(f"Total de entradas: {total_entradas}")
    linhas.append(f"Total de saidas: {total_saidas}")

    valor_total = sum(p["estoque"] * p["preco"] for p in produtos)
    linhas.append(f"Valor total do estoque: {formatar_preco(valor_total)}")

    return "\n".join(linhas) + "\n"


def exportar_relatorio(produtos, movs):
    """Exporta os relatorios para relatorio.txt."""
    conteudo = montar_relatorio_texto(produtos, movs)
    try:
        with open("relatorio.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
        print("Relatorio exportado para relatorio.txt")
    except OSError:
        print("Erro ao exportar o relatorio. Verifique as permissoes da pasta.")


def exibir_menu():
    """Exibe o menu principal."""
    print("\n=== SGL - Sistema de Gestao Local ===")
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("3 - Buscar produto por nome")
    print("4 - Registrar entrada de estoque")
    print("5 - Registrar saida de estoque")
    print("6 - Relatorio de movimentacoes")
    print("7 - Relatorio gerencial")
    print("8 - Salvar e sair")
    print("9 - Editar produto (preco/categoria)")
    print("10 - Exportar relatorio em TXT")


def main():
    produtos, movs = carregar_dados()

    while True:
        exibir_menu()
        try:
            opcao = ler_int("Escolha uma opcao (1-10): ", minimo=1, maximo=10)
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando. Salvando os dados...")
            salvar_dados(produtos, movs)
            break

        if opcao == 1:
            cadastrar_produto(produtos)
        elif opcao == 2:
            listar_produtos_menu(produtos)
        elif opcao == 3:
            buscar_produto_por_nome(produtos)
        elif opcao == 4:
            registrar_mov(produtos, movs, "E")
        elif opcao == 5:
            registrar_mov(produtos, movs, "S")
        elif opcao == 6:
            relatorio_movimentacoes(produtos, movs)
        elif opcao == 7:
            relatorio_gerencial(produtos, movs)
        elif opcao == 8:
            salvar_dados(produtos, movs)
            print("Encerrando o sistema. Ate mais!")
            break
        elif opcao == 9:
            editar_produto(produtos)
        elif opcao == 10:
            exportar_relatorio(produtos, movs)


if __name__ == "__main__":
    main()
