import re

MARCAS_VALIDAS = ["Toyota", "Honda", "Ford"]

class Veiculo:
    def init(self, placa, marca, modelo):
        self.placa = placa
        self.marca = marca
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

        print("Marcas disponíveis:", MARCAS_VALIDAS)
        marca = input("Marca: ").title()

        if marca not in MARCAS_VALIDAS:
            print("Marca inválida")
            return

        modelo = input("Modelo: ")

        self.veiculos.append(Veiculo(placa, marca, modelo))
        print("Veículo cadastrado")

sistema = SistemaFrota()
sistema.cadastrar()