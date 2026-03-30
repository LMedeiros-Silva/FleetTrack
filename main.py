import re

class Veiculo:
    def init(self, placa, modelo):
        self.placa = placa
        self.modelo = modelo

class Manutencao:
    def init(self, tipo, custo):
        self.tipo = tipo
        self.custo = custo

def validar_placa(placa):
    return re.match(r'^[A-Z]{3}\d{4}$', placa.upper())

veiculos = []

def cadastrar():
    placa = input("Placa: ")

    if not validar_placa(placa):
        print("Placa inválida")
        return

    modelo = input("Modelo: ")
    veiculos.append(Veiculo(placa, modelo))
    print("Veículo cadastrado")

cadastrar()