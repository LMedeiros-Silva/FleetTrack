from models.rota import Rota
from utils.validacoes import validar_texto, validar_float_positivo
from services.persistencia import Persistencia


class RotaController:
    def __init__(self):
        self.rotas = []
        self.carregar_rotas()

    def carregar_rotas(self):
        dados = Persistencia.carregar("rotas.json")

        for item in dados:
            rota = Rota(
                item["origem"],
                item["destino"],
                item["distancia"]
            )
            self.rotas.append(rota)

    def salvar_rotas(self):
        dados = []

        for rota in self.rotas:
            dados.append({
                "origem": rota.origem,
                "destino": rota.destino,
                "distancia": rota.distancia
            })

        Persistencia.salvar("rotas.json", dados)

    def cadastrar(self, origem, destino, distancia):
        if not validar_texto(origem):
            return False, "Origem inválida."

        if not validar_texto(destino):
            return False, "Destino inválido."

        if not validar_float_positivo(distancia):
            return False, "Distância inválida."

        rota = Rota(origem, destino, float(distancia))
        self.rotas.append(rota)
        self.salvar_rotas()

        return True, "Rota cadastrada com sucesso."

    def listar(self):
        return self.rotas