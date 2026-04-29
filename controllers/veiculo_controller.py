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
                item["consumo"],
                item.get("quilometragem", 0),
                item.get("proxima_manutencao", 0),
                item.get("combustivel", 0),
                item.get("status", "active")
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
                "consumo": veiculo.consumo,
                "quilometragem": veiculo.quilometragem,
                "proxima_manutencao": veiculo.proxima_manutencao,
                "combustivel": veiculo.combustivel,
                "status": veiculo.status
            })

        Persistencia.salvar("veiculos.json", dados)

    def cadastrar(
        self,
        placa,
        modelo,
        tipo,
        capacidade,
        consumo,
        quilometragem,
        proxima_manutencao,
        combustivel
    ):
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

        if not validar_float_positivo(quilometragem):
            return False, "Quilometragem inválida."

        if not validar_float_positivo(proxima_manutencao):
            return False, "Quilometragem da próxima manutenção inválida."

        if not validar_float_positivo(combustivel):
            return False, "Combustível inválido."

        combustivel_float = float(combustivel)

        if combustivel_float < 0 or combustivel_float > 100:
            return False, "Combustível deve estar entre 0 e 100."

        placa_formatada = placa.upper()

        for veiculo in self.veiculos:
            if veiculo.placa == placa_formatada:
                return False, "Já existe um veículo com essa placa."

        veiculo = Veiculo(
            placa_formatada,
            modelo,
            tipo,
            int(capacidade),
            float(consumo),
            float(quilometragem),
            float(proxima_manutencao),
            combustivel_float,
            "active"
        )

        self.veiculos.append(veiculo)
        self.salvar_veiculos()

        return True, "Veículo cadastrado com sucesso."

    def listar(self):
        return self.veiculos

    def buscar_por_indice(self, indice):
        try:
            return self.veiculos[indice]
        except IndexError:
            return None

    def atualizar_status(self, veiculo, novo_status):
        if veiculo is None:
            return False

        veiculo.status = novo_status
        self.salvar_veiculos()
        return True