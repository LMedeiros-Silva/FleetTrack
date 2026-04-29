from models.custo import Custo
from utils.validacoes import validar_texto, validar_float_positivo
from services.persistencia import Persistencia


class CustoController:
    def __init__(self, veiculo_controller):
        self.veiculo_controller = veiculo_controller
        self.custos = []
        self.carregar_custos()

    def carregar_custos(self):
        dados = Persistencia.carregar("manutencoes.json")

        for item in dados:
            veiculo = self.buscar_veiculo_por_placa(item["placa_veiculo"])

            if veiculo:
                custo = Custo(
                    veiculo,
                    item["tipo_manutencao"],
                    item["descricao"],
                    item["valor"],
                    item["data"]
                )
                self.custos.append(custo)

    def salvar_custos(self):
        dados = []

        for custo in self.custos:
            dados.append({
                "placa_veiculo": custo.veiculo.placa,
                "tipo_manutencao": custo.tipo_manutencao,
                "descricao": custo.descricao,
                "valor": custo.valor,
                "data": custo.data
            })

        Persistencia.salvar("manutencoes.json", dados)

    def buscar_veiculo_por_placa(self, placa):
        for veiculo in self.veiculo_controller.listar():
            if veiculo.placa == placa:
                return veiculo

        return None

    def adicionar(self, veiculo, tipo_manutencao, descricao, valor, data):
        if veiculo is None:
            return False, "Selecione um veículo válido."

        if not validar_texto(tipo_manutencao):
            return False, "Tipo de manutenção inválido."

        if not validar_texto(descricao):
            return False, "Descrição inválida."

        if not validar_float_positivo(valor):
            return False, "Valor inválido."

        if not validar_texto(data):
            return False, "Data inválida."

        custo = Custo(
            veiculo,
            tipo_manutencao,
            descricao,
            float(valor),
            data
        )

        self.custos.append(custo)
        self.salvar_custos()

        self.veiculo_controller.atualizar_status(veiculo, "maintenance")

        return True, "Manutenção cadastrada com sucesso. O veículo foi marcado como Em manutenção."

    def listar(self):
        return self.custos

    def total_custos(self):
        total = 0

        for custo in self.custos:
            total += custo.valor

        return total