class Veiculo:
    def __init__(
        self,
        placa,
        modelo,
        tipo,
        capacidade,
        consumo,
        quilometragem,
        proxima_manutencao,
        combustivel,
        status="active"
    ):
        self.placa = placa
        self.modelo = modelo
        self.tipo = tipo
        self.capacidade = capacidade
        self.consumo = consumo
        self.quilometragem = quilometragem
        self.proxima_manutencao = proxima_manutencao
        self.combustivel = combustivel
        self.status = status