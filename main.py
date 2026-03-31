import re

MARCAS_VALIDAS = ["Toyota", "Honda", "Ford"]

def sugerir_marca(nome):
    for m in MARCAS_VALIDAS:
        if m.lower().startswith(nome.lower()):
            return m
    return None

class Veiculo:
    def __init__(self, placa, marca, modelo):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.historico = []

class SistemaFrota:
    def __init__(self):
        self.veiculos = []

    def cadastrar(self):
        placa = input("Placa: ")

        if not re.match(r'^[A-Z]{3}\d{4}$', placa.upper()):
            print("Placa inválida")
            return

        marca_input = input("Marca: ")
        marca = sugerir_marca(marca_input)

        if not marca:
            print("Marca não encontrada")
            return

        modelo = input("Modelo: ")

        self.veiculos.append(Veiculo(placa, marca, modelo))
        print("Veículo cadastrado")

class Manutencao:
    def __init__(self, tipo, custo):
        if custo <= 0:
            raise ValueError("Custo inválido")
        self.tipo = tipo
        self.custo = custo

sistema = SistemaFrota()
sistema.cadastrar()
