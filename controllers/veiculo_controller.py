from models.veiculo import Veiculo
from utils.validacoes import validar_texto, validar_numero_positivo, validar_float_positivo, validar_placa

class VeiculoController:
    def __init__(self):
        self.veiculos = []

    def cadastrar(self, placa, modelo, tipo, capacidade, consumo):
        if not validar_placa(placa):
            return False, "Placa inválida."

        if not validar_texto(modelo):
            return False, "Modelo inválido."

        if not validar_texto(tipo):
            return False, "Tipo inválido."

        if not validar_numero_positivo(capacidade):
            return False, "Capacidade inválida."

        if not validar_float_positivo(consumo):
            return False, "Consumo inválido."

        veiculo = Veiculo(
            placa.upper(),
            modelo,
            tipo,
            int(capacidade),
            float(consumo)
        )

        self.veiculos.append(veiculo)
        return True, "Veículo cadastrado com sucesso."

    def listar(self):
        return self.veiculos