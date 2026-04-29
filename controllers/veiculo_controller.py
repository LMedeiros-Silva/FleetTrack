from models.veiculo import Veiculo
from utils.validacoes import validar_texto, validar_numero_positivo, validar_float_positivo, validar_placa
from services.persistencia import Persistencia


class VeiculoController:
    def __init__(self):
        self.veiculos = []
        self.carregar_veiculos()

    def carregar_veiculos(self):
        dados = Persistencia.carregar("veiculos.json")

        for item in dados:
            veiculo = Veiculo(
                item["placa"],
                item["modelo"],
                item["tipo"],
                item["capacidade"],
                item["consumo"]
            )
            self.veiculos.append(veiculo)

    def salvar_veiculos(self):
        dados = []

        for veiculo in self.veiculos:
            dados.append({
                "placa": veiculo.placa,
                "modelo": veiculo.modelo,
                "tipo": veiculo.tipo,
                "capacidade": veiculo.capacidade,
                "consumo": veiculo.consumo
            })

        Persistencia.salvar("veiculos.json", dados)

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

        for veiculo in self.veiculos:
            if veiculo.placa == placa.upper():
                return False, "Já existe um veículo com essa placa."

        veiculo = Veiculo(
            placa.upper(),
            modelo,
            tipo,
            int(capacidade),
            float(consumo)
        )

        self.veiculos.append(veiculo)
        self.salvar_veiculos()

        return True, "Veículo cadastrado com sucesso."

    def listar(self):
        return self.veiculos