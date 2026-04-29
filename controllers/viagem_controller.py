from models.viagem import Viagem
from services.persistencia import Persistencia
from utils.validacoes import validar_texto, validar_float_positivo


class ViagemController:
    def __init__(self):
        self.viagens = []
        self.historico_previsoes = []
        self.carregar_viagens()
        self.carregar_previsoes()

    def carregar_viagens(self):
        dados = Persistencia.carregar("viagens.json")

        for item in dados:
            viagem = Viagem(
                item["origem"],
                item["destino"],
                item["distancia"],
                item["data"],
                item["horario"],
                item["motorista"],
                item["veiculo_modelo"],
                item["veiculo_placa"],
                item["status"]
            )
            self.viagens.append(viagem)

    def salvar_viagens(self):
        dados = []

        for viagem in self.viagens:
            dados.append({
                "origem": viagem.origem,
                "destino": viagem.destino,
                "distancia": viagem.distancia,
                "data": viagem.data,
                "horario": viagem.horario,
                "motorista": viagem.motorista,
                "veiculo_modelo": viagem.veiculo_modelo,
                "veiculo_placa": viagem.veiculo_placa,
                "status": viagem.status
            })

        Persistencia.salvar("viagens.json", dados)

    def cadastrar_viagem(
        self,
        origem,
        destino,
        distancia,
        data,
        horario,
        motorista,
        veiculo,
        status
    ):
        if not validar_texto(origem):
            return False, "Origem inválida."

        if not validar_texto(destino):
            return False, "Destino inválido."

        if not validar_float_positivo(distancia):
            return False, "Distância inválida."

        if not validar_texto(data):
            return False, "Data inválida."

        if not validar_texto(horario):
            return False, "Horário inválido."

        if not validar_texto(motorista):
            return False, "Motorista inválido."

        if veiculo is None:
            return False, "Veículo inválido."

        if status not in ["scheduled", "in-progress", "completed"]:
            return False, "Status inválido."

        viagem = Viagem(
            origem,
            destino,
            float(distancia),
            data,
            horario,
            motorista,
            veiculo.modelo,
            veiculo.placa,
            status
        )

        self.viagens.append(viagem)
        self.salvar_viagens()

        return True, "Viagem cadastrada com sucesso."

    def listar(self):
        return self.viagens

    def excluir_por_indice(self, indice):
        try:
            self.viagens.pop(indice)
            self.salvar_viagens()
            return True, "Viagem excluída com sucesso."
        except IndexError:
            return False, "Viagem não encontrada."

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