class Veiculo:
    def __init__(self, placa, modelo):
        self.placa = placa
        self.modelo = modelo

veiculos = []

def cadastrar():
    placa = input("Placa: ")
    modelo = input("Modelo: ")
    veiculos.append(Veiculo(placa, modelo))
    print("Veículo cadastrado")

cadastrar()