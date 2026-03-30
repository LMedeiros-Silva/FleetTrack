import re
[]
MARCAS_VALIDAS = [
    "Toyota", "Honda", "Ford", "Chevrolet", "Volkswagen",
    "Fiat", "Hyundai", "Nissan", "BMW", "Mercedes-Benz",
    "Audi", "Kia", "Peugeot", "Renault", "Jeep"
]



def validar_placa(placa):
    placa = placa.upper()
    padrao_antigo = r'^[A-Z]{3}-?\d{4}$'
    padrao_novo = r'^[A-Z]{3}\d[A-Z]\d{2}$'
    return re.match(padrao_antigo, placa) or re.match(padrao_novo, placa)



def sugerir_marca(marca_digitada):
    for marca in MARCAS_VALIDAS:
        if marca.lower().startswith(marca_digitada.lower()):
            return marca
    return None


class Veiculo:
    def __init__(self, placa, marca, modelo):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.historico = []

    def adicionar_manutencao(self, manutencao):
        self.historico.append(manutencao)

    def mostrar_historico(self):
        if not self.historico:
            print("Nenhuma manutenção registrada para este veículo.")
        else:
            print(f"\nHistórico do veículo {self.placa} ({self.marca} {self.modelo}):")
            for i, m in enumerate(self.historico):
                print(f"{i} - {m}")


class Manutencao:
    def __init__(self, tipo, custo):
        self.tipo = tipo
        self.custo = custo
        self.status = "Pendente"

    def concluir(self):
        if self.status == "Concluída":
            print("Esta manutenção já está concluída.")
        else:
            self.status = "Concluída"

    def __str__(self):
        return f"{self.tipo} | R$ {self.custo:.2f} | Status: {self.status}"


class SistemaFrota:
    def __init__(self):
        self.veiculos = []

    def cadastrar_veiculo(self):
        print("\n=== Cadastro de Veículo ===")

        while True:
            placa = input("Digite a placa (ABC1234 ou ABC1D23): ").upper()

            if not validar_placa(placa):
                print("Placa inválida! Tente novamente.")
                continue

            if any(v.placa == placa for v in self.veiculos):
                print("Já existe um veículo com essa placa.")
                return

            break

        print("\nMarcas disponíveis:")
        for m in MARCAS_VALIDAS:
            print("-", m)

        marca_input = input("Digite a marca: ").strip()
        marca = sugerir_marca(marca_input)

        if not marca:
            print("Marca não encontrada no sistema.")
            return

        print(f"Marca selecionada: {marca}")

        modelo = input("Digite o modelo do veículo: ").strip()

        if len(modelo) < 2:
            print("Modelo deve ter pelo menos 2 caracteres.")
            return

        self.veiculos.append(Veiculo(placa, marca, modelo))
        print("Veículo cadastrado com sucesso!")

    def listar_veiculos(self):
        print("\n=== Lista de Veículos ===")

        if not self.veiculos:
            print("Nenhum veículo cadastrado.")
        else:
            for v in self.veiculos:
                print(f"{v.placa} - {v.marca} {v.modelo}")

    def buscar_veiculo(self, placa):
        return next((v for v in self.veiculos if v.placa == placa), None)

    def registrar_manutencao(self):
        print("\n=== Registro de Manutenção ===")

        placa = input("Digite a placa do veículo: ").upper()
        veiculo = self.buscar_veiculo(placa)

        if not veiculo:
            print("Veículo não encontrado.")
            return

        tipo = input("Digite o tipo de manutenção: ").strip()

        if len(tipo) < 3:
            print("Tipo deve ter pelo menos 3 caracteres.")
            return

        try:
            custo = float(input("Digite o custo da manutenção: "))
            if custo <= 0 or custo > 100000:
                print("O custo deve ser maior que 0 e menor que 100000.")
                return
        except:
            print("Valor inválido.")
            return

        veiculo.adicionar_manutencao(Manutencao(tipo, custo))
        print("Manutenção registrada com sucesso!")

    def concluir_manutencao(self):
        print("\n=== Conclusão de Manutenção ===")

        placa = input("Digite a placa do veículo: ").upper()
        veiculo = self.buscar_veiculo(placa)

        if not veiculo:
            print("Veículo não encontrado.")
            return

        veiculo.mostrar_historico()

        try:
            index = int(input("Digite o número da manutenção: "))

            if index < 0 or index >= len(veiculo.historico):
                print("Índice inválido.")
                return

            veiculo.historico[index].concluir()
            print("Status atualizado com sucesso!")

        except:
            print("Entrada inválida.")

    def mostrar_historico(self):
        print("\n=== Histórico de Manutenções ===")

        placa = input("Digite a placa do veículo: ").upper()
        veiculo = self.buscar_veiculo(placa)

        if not veiculo:
            print("Veículo não encontrado.")
            return

        veiculo.mostrar_historico()



sistema = SistemaFrota()

while True:
    print("\n===== SISTEMA DE GESTÃO DE FROTA =====")
    print("1 - Cadastrar veículo")
    print("2 - Listar veículos")
    print("3 - Registrar manutenção")
    print("4 - Concluir manutenção")
    print("5 - Consultar histórico")
    print("0 - Sair")

    opcao = input("Selecione uma opção: ")

    if opcao == "1":
        sistema.cadastrar_veiculo()
    elif opcao == "2":
        sistema.listar_veiculos()
    elif opcao == "3":
        sistema.registrar_manutencao()
    elif opcao == "4":
        sistema.concluir_manutencao()
    elif opcao == "5":
        sistema.mostrar_historico()
    elif opcao == "0":
        print("Encerrando o sistema...")
        break
    else:
        print("Opção inválida. Tente novamente.")