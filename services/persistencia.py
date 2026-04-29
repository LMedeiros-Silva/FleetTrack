import json
import os


class Persistencia:
    @staticmethod
    def garantir_pasta_data():
        if not os.path.exists("data"):
            os.makedirs("data")

    @staticmethod
    def carregar(nome_arquivo):
        Persistencia.garantir_pasta_data()

        caminho = f"data/{nome_arquivo}"

        if not os.path.exists(caminho):
            return []

        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return []

    @staticmethod
    def salvar(nome_arquivo, dados):
        Persistencia.garantir_pasta_data()

        caminho = f"data/{nome_arquivo}"

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)