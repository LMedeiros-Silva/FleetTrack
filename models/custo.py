class Custo:
    def __init__(self, veiculo, tipo_manutencao, descricao, valor, data, status="pending"):
        self.veiculo = veiculo
        self.tipo_manutencao = tipo_manutencao
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.status = status