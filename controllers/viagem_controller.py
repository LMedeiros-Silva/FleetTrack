from models.viagem import Viagem
from services.previsao_custo import calcular_custo


class ViagemController:
    def __init__(self):
        self.viagens = []
        self.historico_previsoes = []

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

    def prever_custo(self, distancia, consumo, preco_combustivel):
        custo = calcular_custo(distancia, consumo, preco_combustivel)

        previsao = {
            "distancia": distancia,
            "consumo": consumo,
            "preco_combustivel": preco_combustivel,
            "custo": custo
        }

        self.historico_previsoes.append(previsao)

        return custo

    def listar_historico_previsoes(self):
        return self.historico_previsoes