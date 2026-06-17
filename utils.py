"""Funcoes genericas de leitura, validacao de entrada e formatacao."""


def ler_int(msg, minimo=None, maximo=None):
    """Le um numero inteiro validado entre limites opcionais."""
    while True:
        valor = input(msg).strip()
        try:
            valor = int(valor)
            if minimo is not None and valor < minimo:
                print(f"Erro: o valor deve ser maior ou igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Erro: o valor deve ser menor ou igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("Erro: informe um numero inteiro valido.")


def ler_float(msg, minimo=None, maximo=None):
    """Le um numero real validado entre limites opcionais."""
    while True:
        valor = input(msg).strip().replace(",", ".")
        try:
            valor = float(valor)
            if minimo is not None and valor < minimo:
                print(f"Erro: o valor deve ser maior ou igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Erro: o valor deve ser menor ou igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("Erro: informe um numero real valido.")


def proximo_id(lista):
    """Retorna o proximo ID disponivel."""
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


def formatar_preco(valor):
    """Formata valores monetarios no padrao brasileiro simples."""
    return f"R$ {valor:.2f}"
