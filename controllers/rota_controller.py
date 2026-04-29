from models.rota import Rota
from utils.validacoes import validar_texto, validar_float_positivo

class RotaController:
    def __init__(self):
        self.rotas = []

    def cadastrar(self, origem, destino, distancia):
        if not validar_texto(origem):
            return False, "Origem inválida."

        if not validar_texto(destino):
            return False, "Destino inválido."

        if not validar_float_positivo(distancia):
            return False, "Distância inválida."

        rota = Rota(origem, destino, float(distancia))
        self.rotas.append(rota)

        return True, "Rota cadastrada com sucesso."

    def listar(self):
        return self.rotas