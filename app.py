import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QMessageBox,
    QScrollArea
)
from PySide6.QtCore import Qt

from controllers.usuario_controller import UsuarioController
from controllers.veiculo_controller import VeiculoController
from controllers.rota_controller import RotaController
from controllers.viagem_controller import ViagemController
from controllers.custo_controller import CustoController


usuario_controller = UsuarioController()
veiculo_controller = VeiculoController()
rota_controller = RotaController()
viagem_controller = ViagemController()
custo_controller = CustoController(veiculo_controller)


STYLE = """
QWidget {
    background-color: #101014;
    color: #FFFFFF;
    font-family: Arial;
}

QLineEdit {
    background-color: #2A2A32;
    border: 1px solid #33333D;
    border-radius: 16px;
    padding: 13px;
    color: white;
    font-size: 14px;
}

QPushButton {
    background-color: #ED145B;
    color: white;
    border: none;
    border-radius: 18px;
    padding: 13px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #d01250;
}

QFrame {
    background-color: #1E1E24;
    border-radius: 24px;
}

QScrollArea {
    border: none;
}
"""


def criar_titulo(texto):
    titulo = QLabel(texto)
    titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF;")
    return titulo


def criar_subtitulo(texto):
    subtitulo = QLabel(texto)
    subtitulo.setStyleSheet("font-size: 13px; color: #A0A0A8;")
    return subtitulo


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FleetTrack FIAP - Login")
        self.setFixedSize(390, 650)

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 45, 35, 35)
        layout.setSpacing(18)

        titulo = QLabel("FleetTrack FIAP")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 30px; font-weight: bold; color: #ED145B;")

        subtitulo = QLabel("Gestão inteligente da frota institucional")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("font-size: 13px; color: #A0A0A8;")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.senha = QLineEdit()
        self.senha.setPlaceholderText("Senha")
        self.senha.setEchoMode(QLineEdit.Password)

        btn_login = QPushButton("Entrar")
        btn_login.clicked.connect(self.login)

        btn_cadastro = QPushButton("Criar conta")
        btn_cadastro.clicked.connect(self.abrir_cadastro)

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addSpacing(45)
        layout.addWidget(self.email)
        layout.addWidget(self.senha)
        layout.addWidget(btn_login)
        layout.addWidget(btn_cadastro)
        layout.addStretch()

        self.setLayout(layout)

    def login(self):
        usuario = usuario_controller.login(self.email.text(), self.senha.text())

        if usuario:
            self.close()
            self.dashboard = Dashboard(usuario)
            self.dashboard.show()
        else:
            QMessageBox.warning(self, "Erro", "Email ou senha inválidos.")

    def abrir_cadastro(self):
        self.close()
        self.cadastro = Cadastro()
        self.cadastro.show()


class Cadastro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FleetTrack FIAP - Cadastro")
        self.setFixedSize(390, 650)

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 45, 35, 35)
        layout.setSpacing(18)

        titulo = QLabel("Criar Conta")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 30px; font-weight: bold; color: #ED145B;")

        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome completo")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.senha = QLineEdit()
        self.senha.setPlaceholderText("Senha")
        self.senha.setEchoMode(QLineEdit.Password)

        self.confirmar_senha = QLineEdit()
        self.confirmar_senha.setPlaceholderText("Confirmar senha")
        self.confirmar_senha.setEchoMode(QLineEdit.Password)

        btn_cadastrar = QPushButton("Cadastrar")
        btn_cadastrar.clicked.connect(self.cadastrar)

        btn_voltar = QPushButton("Voltar para login")
        btn_voltar.clicked.connect(self.voltar_login)

        layout.addWidget(titulo)
        layout.addSpacing(30)
        layout.addWidget(self.nome)
        layout.addWidget(self.email)
        layout.addWidget(self.senha)
        layout.addWidget(self.confirmar_senha)
        layout.addWidget(btn_cadastrar)
        layout.addWidget(btn_voltar)
        layout.addStretch()

        self.setLayout(layout)

    def cadastrar(self):
        sucesso, mensagem = usuario_controller.cadastrar(
            self.nome.text(),
            self.email.text(),
            self.senha.text(),
            self.confirmar_senha.text()
        )

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.voltar_login()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def voltar_login(self):
        self.close()
        self.login = Login()
        self.login.show()


class Dashboard(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("FleetTrack FIAP - Dashboard")
        self.setFixedSize(430, 780)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(20)

        titulo = criar_titulo("FleetTrack FIAP")
        saudacao = criar_subtitulo(f"Olá, {usuario.nome}!")

        grid = QGridLayout()
        grid.setSpacing(14)

        grid.addWidget(self.card_estatistica("🚗", "Veículos cadastrados", str(len(veiculo_controller.listar())), "#ED145B"), 0, 0)
        grid.addWidget(self.card_estatistica("📍", "Rotas cadastradas", str(len(rota_controller.listar())), "#7C3AED"), 0, 1)
        grid.addWidget(self.card_estatistica("📅", "Viagens do dia", str(len(viagem_controller.listar())), "#06B6D4"), 1, 0)
        grid.addWidget(self.card_estatistica("💰", "Custos do mês", f"R$ {custo_controller.total_custos():.2f}", "#F59E0B"), 1, 1)

        layout.addWidget(titulo)
        layout.addWidget(saudacao)
        layout.addLayout(grid)

        layout.addWidget(self.card_proximas_viagens())
        layout.addWidget(self.card_custos_categoria())

        btn_veiculo = QPushButton("Cadastrar Veículo")
        btn_veiculo.clicked.connect(self.abrir_cadastro_veiculo)

        btn_rota = QPushButton("Cadastrar Rota")
        btn_rota.clicked.connect(self.abrir_cadastro_rota)

        btn_manutencao = QPushButton("Cadastrar Manutenção")
        btn_manutencao.clicked.connect(self.abrir_cadastro_manutencao)

        btn_historico = QPushButton("Histórico Geral")
        btn_historico.clicked.connect(self.abrir_historico)

        layout.addWidget(btn_veiculo)
        layout.addWidget(btn_rota)
        layout.addWidget(btn_manutencao)
        layout.addWidget(btn_historico)

        container.setLayout(layout)
        scroll.setWidget(container)

        main_layout.addWidget(scroll)
        main_layout.addLayout(self.navbar())

        self.setLayout(main_layout)

    def card_estatistica(self, icone, label, valor, cor):
        frame = QFrame()
        frame.setFixedSize(175, 145)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        icon = QLabel(icone)
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(46, 46)
        icon.setStyleSheet(f"background-color: {cor}; border-radius: 16px; font-size: 22px;")

        valor_label = QLabel(valor)
        valor_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #FFFFFF;")

        label_widget = QLabel(label)
        label_widget.setWordWrap(True)
        label_widget.setStyleSheet("font-size: 12px; color: #A0A0A8;")

        layout.addWidget(icon)
        layout.addWidget(valor_label)
        layout.addWidget(label_widget)

        frame.setLayout(layout)
        return frame

    def card_proximas_viagens(self):
        frame = QFrame()

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        titulo = QLabel("Próximas Viagens")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(titulo)

        viagens = [
            ("São Paulo", "Campinas", "09:30", "Van Mercedes", "Carlos Silva"),
            ("Guarulhos", "São José", "11:00", "Ônibus Volvo", "Ana Santos"),
            ("Ribeirão Preto", "Franca", "14:15", "Micro-ônibus", "João Costa")
        ]

        for origem, destino, horario, veiculo, motorista in viagens:
            item = QFrame()
            item.setStyleSheet("background-color: #2A2A32; border-radius: 18px;")

            item_layout = QVBoxLayout()
            item_layout.setContentsMargins(14, 12, 14, 12)

            linha1 = QLabel(f"📍 {origem} → {destino}     {horario}")
            linha1.setStyleSheet("font-size: 13px; color: #FFFFFF;")

            linha2 = QLabel(f"{veiculo}  •  {motorista}")
            linha2.setStyleSheet("font-size: 12px; color: #A0A0A8;")

            item_layout.addWidget(linha1)
            item_layout.addWidget(linha2)
            item.setLayout(item_layout)

            layout.addWidget(item)

        frame.setLayout(layout)
        return frame

    def card_custos_categoria(self):
        frame = QFrame()

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        titulo = QLabel("Custos por Categoria")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(titulo)

        dados = [
            ("Combustível", 55, "#ED145B", "R$ 6.820"),
            ("Manutenção", 30, "#7C3AED", f"R$ {custo_controller.total_custos():.2f}"),
            ("Outros", 15, "#06B6D4", "R$ 1.860")
        ]

        for categoria, porcentagem, cor, valor in dados:
            linha = QLabel(f"{categoria} — {valor}")
            linha.setStyleSheet("font-size: 13px; color: #FFFFFF;")

            barra_fundo = QFrame()
            barra_fundo.setFixedHeight(12)
            barra_fundo.setStyleSheet("background-color: #2A2A32; border-radius: 6px;")

            barra_layout = QHBoxLayout()
            barra_layout.setContentsMargins(0, 0, 0, 0)

            barra = QFrame()
            barra.setFixedWidth(int(320 * porcentagem / 100))
            barra.setFixedHeight(12)
            barra.setStyleSheet(f"background-color: {cor}; border-radius: 6px;")

            barra_layout.addWidget(barra)
            barra_layout.addStretch()
            barra_fundo.setLayout(barra_layout)

            layout.addWidget(linha)
            layout.addWidget(barra_fundo)

        frame.setLayout(layout)
        return frame

    def navbar(self):
        nav = QHBoxLayout()
        nav.setContentsMargins(18, 10, 18, 12)
        nav.setSpacing(8)

        botoes = [
            ("Dashboard", self.recarregar_dashboard),
            ("Veículos", self.abrir_lista_veiculos),
            ("Rotas", self.abrir_lista_rotas),
            ("Custos", self.abrir_previsao)
        ]

        for texto, funcao in botoes:
            botao = QPushButton(texto)
            botao.setStyleSheet("""
                QPushButton {
                    background-color: #1E1E24;
                    color: #A0A0A8;
                    border-radius: 16px;
                    padding: 10px;
                    font-size: 11px;
                }

                QPushButton:hover {
                    background-color: #ED145B;
                    color: white;
                }
            """)
            botao.clicked.connect(funcao)
            nav.addWidget(botao)

        return nav

    def recarregar_dashboard(self):
        self.close()
        self.tela = Dashboard(self.usuario)
        self.tela.show()

    def abrir_cadastro_veiculo(self):
        self.close()
        self.tela = CadastroVeiculo(self.usuario)
        self.tela.show()

    def abrir_cadastro_rota(self):
        self.close()
        self.tela = CadastroRota(self.usuario)
        self.tela.show()

    def abrir_cadastro_manutencao(self):
        self.close()
        self.tela = CadastroManutencao(self.usuario)
        self.tela.show()

    def abrir_lista_veiculos(self):
        self.close()
        self.tela = ListaVeiculos(self.usuario)
        self.tela.show()

    def abrir_lista_rotas(self):
        self.close()
        self.tela = ListaRotas(self.usuario)
        self.tela.show()

    def abrir_previsao(self):
        self.close()
        self.tela = PrevisaoCusto(self.usuario)
        self.tela.show()

    def abrir_historico(self):
        self.close()
        self.tela = HistoricoGeral(self.usuario)
        self.tela.show()


class CadastroVeiculo(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Cadastrar Veículo")
        self.setFixedSize(390, 650)

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(15)

        layout.addWidget(criar_titulo("Cadastrar Veículo"))
        layout.addWidget(criar_subtitulo("Adicione um veículo institucional da FIAP."))

        self.placa = QLineEdit()
        self.placa.setPlaceholderText("Placa")

        self.modelo = QLineEdit()
        self.modelo.setPlaceholderText("Modelo")

        self.tipo = QLineEdit()
        self.tipo.setPlaceholderText("Tipo: carro, van ou ônibus")

        self.capacidade = QLineEdit()
        self.capacidade.setPlaceholderText("Capacidade")

        self.consumo = QLineEdit()
        self.consumo.setPlaceholderText("Consumo médio km/l")

        btn_salvar = QPushButton("Salvar Veículo")
        btn_salvar.clicked.connect(self.salvar)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(self.placa)
        layout.addWidget(self.modelo)
        layout.addWidget(self.tipo)
        layout.addWidget(self.capacidade)
        layout.addWidget(self.consumo)
        layout.addWidget(btn_salvar)
        layout.addWidget(btn_voltar)
        layout.addStretch()

        self.setLayout(layout)

    def salvar(self):
        sucesso, mensagem = veiculo_controller.cadastrar(
            self.placa.text(),
            self.modelo.text(),
            self.tipo.text(),
            self.capacidade.text(),
            self.consumo.text()
        )

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.voltar()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def voltar(self):
        self.close()
        self.dashboard = Dashboard(self.usuario)
        self.dashboard.show()


class CadastroRota(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Cadastrar Rota")
        self.setFixedSize(390, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(15)

        layout.addWidget(criar_titulo("Cadastrar Rota"))
        layout.addWidget(criar_subtitulo("Registre uma rota usada pela frota."))

        self.origem = QLineEdit()
        self.origem.setPlaceholderText("Origem")

        self.destino = QLineEdit()
        self.destino.setPlaceholderText("Destino")

        self.distancia = QLineEdit()
        self.distancia.setPlaceholderText("Distância em km")

        btn_salvar = QPushButton("Salvar Rota")
        btn_salvar.clicked.connect(self.salvar)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(self.origem)
        layout.addWidget(self.destino)
        layout.addWidget(self.distancia)
        layout.addWidget(btn_salvar)
        layout.addWidget(btn_voltar)
        layout.addStretch()

        self.setLayout(layout)

    def salvar(self):
        sucesso, mensagem = rota_controller.cadastrar(
            self.origem.text(),
            self.destino.text(),
            self.distancia.text()
        )

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.voltar()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def voltar(self):
        self.close()
        self.dashboard = Dashboard(self.usuario)
        self.dashboard.show()


class CadastroManutencao(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Cadastrar Manutenção")
        self.setFixedSize(390, 700)

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(15)

        layout.addWidget(criar_titulo("Cadastrar Manutenção"))
        layout.addWidget(criar_subtitulo("Registre custos reais de manutenção."))

        self.indice_veiculo = QLineEdit()
        self.indice_veiculo.setPlaceholderText("Índice do veículo")

        self.tipo_manutencao = QLineEdit()
        self.tipo_manutencao.setPlaceholderText("Tipo: preventiva, corretiva, revisão")

        self.descricao = QLineEdit()
        self.descricao.setPlaceholderText("Descrição da manutenção")

        self.valor = QLineEdit()
        self.valor.setPlaceholderText("Valor da manutenção")

        self.data = QLineEdit()
        self.data.setPlaceholderText("Data da manutenção")

        lista = QLabel(self.gerar_lista_veiculos())
        lista.setStyleSheet("font-size: 12px; color: #A0A0A8;")
        lista.setWordWrap(True)

        btn_salvar = QPushButton("Salvar Manutenção")
        btn_salvar.clicked.connect(self.salvar)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(lista)
        layout.addWidget(self.indice_veiculo)
        layout.addWidget(self.tipo_manutencao)
        layout.addWidget(self.descricao)
        layout.addWidget(self.valor)
        layout.addWidget(self.data)
        layout.addWidget(btn_salvar)
        layout.addWidget(btn_voltar)
        layout.addStretch()

        self.setLayout(layout)

    def gerar_lista_veiculos(self):
        veiculos = veiculo_controller.listar()

        if not veiculos:
            return "Nenhum veículo cadastrado. Cadastre um veículo antes."

        texto = "Veículos disponíveis:\n"

        for i, veiculo in enumerate(veiculos):
            texto += f"{i} - {veiculo.modelo} | {veiculo.placa}\n"

        return texto

    def salvar(self):
        try:
            indice = int(self.indice_veiculo.text())
            veiculo = veiculo_controller.listar()[indice]

            sucesso, mensagem = custo_controller.adicionar(
                veiculo,
                self.tipo_manutencao.text(),
                self.descricao.text(),
                self.valor.text(),
                self.data.text()
            )

            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.voltar()
            else:
                QMessageBox.warning(self, "Erro", mensagem)

        except:
            QMessageBox.warning(self, "Erro", "Selecione um índice de veículo válido.")

    def voltar(self):
        self.close()
        self.dashboard = Dashboard(self.usuario)
        self.dashboard.show()


class ListaVeiculos(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Veículos Cadastrados")
        self.setFixedSize(430, 720)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 30, 25, 25)
        layout.setSpacing(15)

        layout.addWidget(criar_titulo("Veículos Cadastrados"))

        veiculos = veiculo_controller.listar()

        if not veiculos:
            vazio = criar_subtitulo("Nenhum veículo cadastrado.")
            layout.addWidget(vazio)
        else:
            for veiculo in veiculos:
                card = QFrame()
                card_layout = QVBoxLayout()

                texto = QLabel(
                    f"Placa: {veiculo.placa}\n"
                    f"Modelo: {veiculo.modelo}\n"
                    f"Tipo: {veiculo.tipo}\n"
                    f"Capacidade: {veiculo.capacidade}\n"
                    f"Consumo: {veiculo.consumo} km/l"
                )

                texto.setStyleSheet("font-size: 13px; color: #FFFFFF;")
                card_layout.addWidget(texto)
                card.setLayout(card_layout)

                layout.addWidget(card)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(btn_voltar)
        layout.addStretch()

        self.setLayout(layout)

    def voltar(self):
        self.close()
        self.dashboard = Dashboard(self.usuario)
        self.dashboard.show()


class ListaRotas(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Rotas Cadastradas")
        self.setFixedSize(430, 720)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 30, 25, 25)
        layout.setSpacing(15)

        layout.addWidget(criar_titulo("Rotas Cadastradas"))

        rotas = rota_controller.listar()

        if not rotas:
            vazio = criar_subtitulo("Nenhuma rota cadastrada.")
            layout.addWidget(vazio)
        else:
            for rota in rotas:
                card = QFrame()
                card_layout = QVBoxLayout()

                texto = QLabel(
                    f"Origem: {rota.origem}\n"
                    f"Destino: {rota.destino}\n"
                    f"Distância: {rota.distancia} km"
                )

                texto.setStyleSheet("font-size: 13px; color: #FFFFFF;")
                card_layout.addWidget(texto)
                card.setLayout(card_layout)

                layout.addWidget(card)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(btn_voltar)
        layout.addStretch()

        self.setLayout(layout)

    def voltar(self):
        self.close()
        self.dashboard = Dashboard(self.usuario)
        self.dashboard.show()


class PrevisaoCusto(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Previsão de Custo")
        self.setFixedSize(430, 780)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 20)
        main_layout.setSpacing(18)

        main_layout.addWidget(criar_titulo("Previsão de Custo"))
        main_layout.addWidget(criar_subtitulo("Simulação inteligente de custos de viagem"))

        card_inputs = QFrame()
        inputs_layout = QVBoxLayout()
        inputs_layout.setContentsMargins(18, 18, 18, 18)
        inputs_layout.setSpacing(14)

        self.distancia = QLineEdit()
        self.distancia.setPlaceholderText("Distância da viagem (km)")

        self.consumo = QLineEdit()
        self.consumo.setPlaceholderText("Consumo médio do veículo (km/l)")

        self.preco = QLineEdit()
        self.preco.setPlaceholderText("Preço do combustível (R$/l)")

        self.fator = QLineEdit()
        self.fator.setPlaceholderText("Fator de manutenção (%)")

        inputs_layout.addWidget(QLabel("Distância da viagem (km)"))
        inputs_layout.addWidget(self.distancia)
        inputs_layout.addWidget(QLabel("Consumo médio do veículo (km/l)"))
        inputs_layout.addWidget(self.consumo)
        inputs_layout.addWidget(QLabel("Preço do combustível (R$/l)"))
        inputs_layout.addWidget(self.preco)
        inputs_layout.addWidget(QLabel("Fator de manutenção (%)"))
        inputs_layout.addWidget(self.fator)

        card_inputs.setLayout(inputs_layout)

        btn_calcular = QPushButton("🧮 Calcular Custo")
        btn_calcular.clicked.connect(self.calcular)

        self.card_resultado = QFrame()
        self.card_resultado.setStyleSheet("background-color: #ED145B; border-radius: 24px;")
        resultado_layout = QVBoxLayout()
        resultado_layout.setContentsMargins(18, 18, 18, 18)

        self.resultado = QLabel("")
        self.resultado.setStyleSheet("font-size: 34px; font-weight: bold; color: #FFFFFF;")

        self.detalhes = QLabel("")
        self.detalhes.setStyleSheet("font-size: 13px; color: #FFFFFF;")
        self.detalhes.setWordWrap(True)

        resultado_layout.addWidget(QLabel("Custo Total Estimado"))
        resultado_layout.addWidget(self.resultado)
        resultado_layout.addWidget(self.detalhes)

        self.card_resultado.setLayout(resultado_layout)
        self.card_resultado.hide()

        dica = QFrame()
        dica_layout = QVBoxLayout()
        dica_layout.setContentsMargins(18, 18, 18, 18)

        dica_titulo = QLabel("💡 Dica Inteligente")
        dica_titulo.setStyleSheet("font-weight: bold; color: #FFFFFF;")

        dica_texto = QLabel(
            "Manutenções preventivas podem reduzir custos e evitar gastos inesperados."
        )
        dica_texto.setWordWrap(True)
        dica_texto.setStyleSheet("font-size: 12px; color: #A0A0A8;")

        dica_layout.addWidget(dica_titulo)
        dica_layout.addWidget(dica_texto)
        dica.setLayout(dica_layout)

        main_layout.addWidget(card_inputs)
        main_layout.addWidget(btn_calcular)
        main_layout.addWidget(self.card_resultado)
        main_layout.addWidget(dica)
        main_layout.addStretch()
        main_layout.addLayout(self.navbar())

        self.setLayout(main_layout)

    def calcular(self):
        try:
            distancia = float(self.distancia.text())
            consumo = float(self.consumo.text())
            preco = float(self.preco.text())
            fator = float(self.fator.text())

            custo = viagem_controller.prever_custo(distancia, consumo, preco, fator)

            litros = distancia / consumo
            custo_combustivel = litros * preco
            custo_manutencao = custo - custo_combustivel

            self.resultado.setText(f"R$ {custo:.2f}")
            self.detalhes.setText(
                f"Litros necessários: {litros:.2f} L\n"
                f"Custo combustível: R$ {custo_combustivel:.2f}\n"
                f"Custo manutenção: R$ {custo_manutencao:.2f}"
            )

            self.card_resultado.show()

        except:
            QMessageBox.warning(self, "Erro", "Preencha os campos com números válidos.")

    def navbar(self):
        nav = QHBoxLayout()

        botoes = [
            ("Dashboard", self.voltar),
            ("Veículos", self.abrir_lista_veiculos),
            ("Rotas", self.abrir_lista_rotas),
            ("Custos", lambda: None)
        ]

        for texto, funcao in botoes:
            botao = QPushButton(texto)
            botao.setStyleSheet("""
                QPushButton {
                    background-color: #1E1E24;
                    color: #A0A0A8;
                    border-radius: 16px;
                    padding: 10px;
                    font-size: 11px;
                }

                QPushButton:hover {
                    background-color: #ED145B;
                    color: white;
                }
            """)
            botao.clicked.connect(funcao)
            nav.addWidget(botao)

        return nav

    def abrir_lista_veiculos(self):
        self.close()
        self.tela = ListaVeiculos(self.usuario)
        self.tela.show()

    def abrir_lista_rotas(self):
        self.close()
        self.tela = ListaRotas(self.usuario)
        self.tela.show()

    def voltar(self):
        self.close()
        self.dashboard = Dashboard(self.usuario)
        self.dashboard.show()


class HistoricoGeral(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Histórico Geral")
        self.setFixedSize(430, 720)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 30, 25, 25)
        layout.setSpacing(12)

        layout.addWidget(criar_titulo("Histórico Geral"))

        historico = QLabel(self.gerar_texto_historico())
        historico.setStyleSheet("font-size: 12px; color: #FFFFFF;")
        historico.setWordWrap(True)

        layout.addWidget(historico)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(btn_voltar)
        layout.addStretch()

        self.setLayout(layout)

    def gerar_texto_historico(self):
        texto = ""

        texto += "VEÍCULOS CADASTRADOS:\n"
        veiculos = veiculo_controller.listar()

        if not veiculos:
            texto += "- Nenhum veículo cadastrado.\n"
        else:
            for veiculo in veiculos:
                texto += f"- {veiculo.modelo} | {veiculo.placa} | {veiculo.tipo}\n"

        texto += "\nROTAS CADASTRADAS:\n"
        rotas = rota_controller.listar()

        if not rotas:
            texto += "- Nenhuma rota cadastrada.\n"
        else:
            for rota in rotas:
                texto += f"- {rota.origem} -> {rota.destino} | {rota.distancia} km\n"

        texto += "\nMANUTENÇÕES CADASTRADAS:\n"
        manutencoes = custo_controller.listar()

        if not manutencoes:
            texto += "- Nenhuma manutenção cadastrada.\n"
        else:
            for manutencao in manutencoes:
                texto += (
                    f"- {manutencao.veiculo.modelo} | "
                    f"{manutencao.tipo_manutencao} | "
                    f"R$ {manutencao.valor:.2f} | "
                    f"{manutencao.data}\n"
                )

        texto += "\nPREVISÕES DE CUSTO:\n"
        previsoes = viagem_controller.listar_historico_previsoes()

        if not previsoes:
            texto += "- Nenhuma previsão realizada.\n"
        else:
            for previsao in previsoes:
                texto += (
                    f"- Distância: {previsao['distancia']} km | "
                    f"Consumo: {previsao['consumo']} km/l | "
                    f"Custo previsto: R$ {previsao['custo']:.2f}\n"
                )

        return texto

    def voltar(self):
        self.close()
        self.dashboard = Dashboard(self.usuario)
        self.dashboard.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    janela = Login()
    janela.show()

    sys.exit(app.exec())