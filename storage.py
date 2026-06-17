"""Persistencia dos dados em arquivos JSON."""

import json
import os

PRODUTOS_FILE = "produtos.json"
MOVS_FILE = "movs.json"


def carregar_dados():
    """Carrega produtos e movimentacoes a partir dos arquivos JSON."""
    produtos = []
    movs = []

    if os.path.exists(PRODUTOS_FILE):
        try:
            with open(PRODUTOS_FILE, "r", encoding="utf-8") as arquivo:
                produtos = json.load(arquivo)
        except (json.JSONDecodeError, OSError):
            print(f"Atencao: nao foi possivel ler {PRODUTOS_FILE}.")

    if os.path.exists(MOVS_FILE):
        try:
            with open(MOVS_FILE, "r", encoding="utf-8") as arquivo:
                movs = json.load(arquivo)
        except (json.JSONDecodeError, OSError):
            print(f"Atencao: nao foi possivel ler {MOVS_FILE}.")

    return produtos, movs


def salvar_dados(produtos, movs):
    """Salva produtos e movimentacoes em JSON com indentacao."""
    try:
        with open(PRODUTOS_FILE, "w", encoding="utf-8") as arquivo:
            json.dump(produtos, arquivo, indent=2, ensure_ascii=False)
        with open(MOVS_FILE, "w", encoding="utf-8") as arquivo:
            json.dump(movs, arquivo, indent=2, ensure_ascii=False)
        print("Dados salvos com sucesso.")
    except OSError:
        print("Erro ao salvar os dados. Verifique as permissoes da pasta.")
