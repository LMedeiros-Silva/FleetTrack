from models.custo import Custo

class CustoController:
    def __init__(self):
        self.custos = []

    def adicionar(self, descricao, valor):
        custo = Custo(descricao, valor)
        self.custos.append(custo)

    def listar(self):
        return self.custos

    def total_custos(self):
        total = 0

        for custo in self.custos:
            total += custo.valor

        return total