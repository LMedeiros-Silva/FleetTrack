import re

class Veiculo:
    def init(self, placa, modelo):
        self.placa = placa
        self.modelo = modelo
        self.historico = []

class SistemaFrota:
    def init(self):
        self.veiculos = []

    def cadastrar(self):
        placa = input("Placa: ")

        if not re.match(r'^[A-Z]{3}\d{4}$', placa.upper()):
            print("Placa inválida")
            return

        modelo = input("Modelo: ")
        self.veiculos.append(Veiculo(placa, modelo))
        print("Veículo cadastrado")

sistema = SistemaFrota()
sistema.cadastrar()