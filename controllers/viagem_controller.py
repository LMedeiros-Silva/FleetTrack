from models.viagem import Viagem
from services.previsao_custo import calcular_custo
from services.persistencia import Persistencia


class ViagemController:
    def __init__(self):
        self.viagens = []
        self.historico_previsoes = []
        self.carregar_previsoes()

    def criar(self, veiculo, rota, data, preco_combustivel):
        custo = calcular_custo(
            rota.distancia,
            veiculo.consumo,
            preco_combustivel
        )

        viagem = Viagem(veiculo, rota, data, custo)
        self.viagens.append(viagem)

        return viagem

    def listar(self):
        return self.viagens

    def carregar_previsoes(self):
        self.historico_previsoes = Persistencia.carregar("previsoes.json")

    def salvar_previsoes(self):
        Persistencia.salvar("previsoes.json", self.historico_previsoes)

    def prever_custo(self, distancia, consumo, preco_combustivel, fator_manutencao=15):
        fator = fator_manutencao / 100

        litros = distancia / consumo
        custo_combustivel = litros * preco_combustivel
        custo_manutencao = custo_combustivel * fator
        custo_total = custo_combustivel + custo_manutencao

        previsao = {
            "distancia": distancia,
            "consumo": consumo,
            "preco_combustivel": preco_combustivel,
            "fator_manutencao": fator_manutencao,
            "litros": round(litros, 2),
            "custo_combustivel": round(custo_combustivel, 2),
            "custo_manutencao": round(custo_manutencao, 2),
            "custo": round(custo_total, 2)
        }

        self.historico_previsoes.append(previsao)
        self.salvar_previsoes()

        return round(custo_total, 2)

    def listar_historico_previsoes(self):
        return self.historico_previsoes