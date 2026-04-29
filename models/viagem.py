class Viagem:
    def __init__(
        self,
        origem,
        destino,
        distancia,
        data,
        horario,
        motorista,
        veiculo_modelo,
        veiculo_placa,
        status
    ):
        self.origem = origem
        self.destino = destino
        self.distancia = distancia
        self.data = data
        self.horario = horario
        self.motorista = motorista
        self.veiculo_modelo = veiculo_modelo
        self.veiculo_placa = veiculo_placa
        self.status = status