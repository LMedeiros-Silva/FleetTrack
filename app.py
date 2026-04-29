import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFrame,
    QMessageBox, QScrollArea, QComboBox
)
from PySide6.QtCore import Qt

from controllers.usuario_controller import UsuarioController
from controllers.veiculo_controller import VeiculoController
from controllers.viagem_controller import ViagemController
from controllers.custo_controller import CustoController


usuario_controller = UsuarioController()
veiculo_controller = VeiculoController()
viagem_controller = ViagemController()
custo_controller = CustoController(veiculo_controller)


STYLE = """
QWidget {
    background-color: #0B0B0F;
    color: #FFFFFF;
    font-family: Arial;
}

QLabel {
    background-color: transparent;
    border: none;
}

QLineEdit, QComboBox {
    background-color: #191A22;
    border: 1px solid #2B2D38;
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
    background-color: #ff2a6d;
}

QFrame {
    background-color: #15161D;
    border-radius: 24px;
}

QScrollArea {
    border: none;
    background-color: #0B0B0F;
}
"""


def titulo(texto):
    label = QLabel(texto)
    label.setStyleSheet("font-size: 28px; font-weight: bold; color: #FFFFFF;")
    return label


def subtitulo(texto):
    label = QLabel(texto)
    label.setStyleSheet("font-size: 14px; color: #9CA3AF;")
    return label


def botao_secundario(texto):
    btn = QPushButton(texto)
    btn.setStyleSheet("""
        QPushButton {
            background-color: #191A22;
            color: #D1D5DB;
            border-radius: 16px;
            padding: 12px;
            font-size: 13px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #252733;
            color: white;
        }
    """)
    return btn


def botao_filtro(texto, ativo):
    btn = QPushButton(texto)

    if ativo:
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ED145B;
                color: white;
                border-radius: 18px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }
        """)
    else:
        btn.setStyleSheet("""
            QPushButton {
                background-color: #191A22;
                color: #9CA3AF;
                border-radius: 18px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #252733;
                color: white;
            }
        """)

    return btn


def criar_scroll():
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)

    container = QWidget()
    layout = QVBoxLayout()
    layout.setContentsMargins(22, 24, 22, 24)
    layout.setSpacing(18)

    container.setLayout(layout)
    scroll.setWidget(container)

    return scroll, layout


def criar_navbar(tela_atual, usuario, ativo):
    nav = QHBoxLayout()
    nav.setContentsMargins(14, 10, 14, 12)
    nav.setSpacing(8)

    def ir_dashboard():
        tela_atual.close()
        tela_atual.tela = Dashboard(usuario)
        tela_atual.tela.show()

    def ir_veiculos():
        tela_atual.close()
        tela_atual.tela = TelaVeiculos(usuario)
        tela_atual.tela.show()

    def ir_viagens():
        tela_atual.close()
        tela_atual.tela = TelaViagens(usuario)
        tela_atual.tela.show()

    def ir_custos():
        tela_atual.close()
        tela_atual.tela = PrevisaoCusto(usuario)
        tela_atual.tela.show()

    itens = [
        ("Dashboard", "dashboard", ir_dashboard),
        ("Veículos", "vehicles", ir_veiculos),
        ("Viagens", "trips", ir_viagens),
        ("Custos", "costs", ir_custos)
    ]

    for texto, key, funcao in itens:
        btn = botao_filtro(texto, ativo == key)
        btn.clicked.connect(funcao)
        nav.addWidget(btn)

    return nav


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FleetTrack FIAP - Login")
        self.setFixedSize(390, 650)

        layout = QVBoxLayout()
        layout.setContentsMargins(34, 50, 34, 34)
        layout.setSpacing(18)

        logo = QLabel("FleetTrack")
        logo.setAlignment(Qt.AlignCenter)
        logo.setAttribute(Qt.WA_TranslucentBackground)
        logo.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
                font-size: 36px;
                font-weight: bold;
                color: #ED145B;
            }
        """)

        desc = QLabel("Gestão inteligente da frota FIAP")
        desc.setAlignment(Qt.AlignCenter)
        desc.setAttribute(Qt.WA_TranslucentBackground)
        desc.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
                font-size: 14px;
                color: #9CA3AF;
            }
        """)

        self.email = QLineEdit()
        self.email.setPlaceholderText("E-mail")

        self.senha = QLineEdit()
        self.senha.setPlaceholderText("Senha")
        self.senha.setEchoMode(QLineEdit.Password)

        btn_login = QPushButton("Entrar")
        btn_login.clicked.connect(self.login)

        btn_cadastro = botao_secundario("Criar conta")
        btn_cadastro.clicked.connect(self.abrir_cadastro)

        layout.addStretch()
        layout.addWidget(logo)
        layout.addWidget(desc)
        layout.addSpacing(30)
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
            self.tela = Dashboard(usuario)
            self.tela.show()
        else:
            QMessageBox.warning(self, "Erro", "E-mail ou senha inválidos.")

    def abrir_cadastro(self):
        self.close()
        self.tela = Cadastro()
        self.tela.show()


class Cadastro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FleetTrack FIAP - Cadastro")
        self.setFixedSize(390, 650)

        layout = QVBoxLayout()
        layout.setContentsMargins(34, 50, 34, 34)
        layout.setSpacing(18)

        header = titulo("Criar conta")
        desc = subtitulo("Cadastre-se para acessar o FleetTrack")

        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome completo")

        self.email = QLineEdit()
        self.email.setPlaceholderText("E-mail")

        self.senha = QLineEdit()
        self.senha.setPlaceholderText("Senha")
        self.senha.setEchoMode(QLineEdit.Password)

        self.confirmar_senha = QLineEdit()
        self.confirmar_senha.setPlaceholderText("Confirmar senha")
        self.confirmar_senha.setEchoMode(QLineEdit.Password)

        btn_cadastrar = QPushButton("Cadastrar")
        btn_cadastrar.clicked.connect(self.cadastrar)

        btn_voltar = botao_secundario("Voltar para login")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(header)
        layout.addWidget(desc)
        layout.addSpacing(20)
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
            self.voltar()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def voltar(self):
        self.close()
        self.tela = Login()
        self.tela.show()


class Dashboard(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("FleetTrack FIAP")
        self.setFixedSize(430, 780)

        main = QVBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)

        scroll, layout = criar_scroll()

        header = QFrame()
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(20, 18, 20, 18)

        h1 = QLabel("FleetTrack FIAP")
        h1.setStyleSheet("font-size: 28px; font-weight: bold; color: #FFFFFF;")

        h2 = QLabel(f"Olá, {self.usuario.nome}! Controle sua frota com inteligência.")
        h2.setWordWrap(True)
        h2.setStyleSheet("font-size: 13px; color: #9CA3AF;")

        header_layout.addWidget(h1)
        header_layout.addWidget(h2)
        header.setLayout(header_layout)

        layout.addWidget(header)

        total_veiculos = len(veiculo_controller.listar())
        total_viagens = len(viagem_controller.listar())
        total_manutencoes = len(custo_controller.listar())
        total_custos = custo_controller.total_custos()

        grid = QGridLayout()
        grid.setSpacing(14)

        grid.addWidget(self.card_dashboard("🚗", "Veículos", total_veiculos, "#ED145B"), 0, 0)
        grid.addWidget(self.card_dashboard("🚌", "Viagens", total_viagens, "#06B6D4"), 0, 1)
        grid.addWidget(self.card_dashboard("🛠️", "Manutenções", total_manutencoes, "#F59E0B"), 1, 0)
        grid.addWidget(self.card_dashboard("💰", "Custos", f"R$ {total_custos:.2f}", "#7C3AED"), 1, 1)

        layout.addLayout(grid)

        btn_veiculo = QPushButton("Cadastrar Veículo")
        btn_veiculo.clicked.connect(self.abrir_cadastro_veiculo)

        btn_viagem = QPushButton("Cadastrar Viagem")
        btn_viagem.clicked.connect(self.abrir_cadastro_viagem)

        btn_manutencao = QPushButton("Cadastrar Manutenção")
        btn_manutencao.clicked.connect(self.abrir_cadastro_manutencao)

        btn_previsao = QPushButton("Previsão de Custo")
        btn_previsao.clicked.connect(self.abrir_previsao)

        btn_logout = botao_secundario("Sair da Conta")
        btn_logout.clicked.connect(self.logout)

        layout.addWidget(btn_veiculo)
        layout.addWidget(btn_viagem)
        layout.addWidget(btn_manutencao)
        layout.addWidget(btn_previsao)
        layout.addWidget(btn_logout)
        layout.addStretch()

        main.addWidget(scroll)
        main.addLayout(criar_navbar(self, self.usuario, "dashboard"))

        self.setLayout(main)

    def card_dashboard(self, icone, texto, valor, cor):
        card = QFrame()
        card.setFixedSize(175, 135)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        icon = QLabel(icone)
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(46, 46)
        icon.setStyleSheet(f"background-color: {cor}; border-radius: 16px; font-size: 22px;")

        value = QLabel(str(valor))
        value.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF;")

        label = QLabel(texto)
        label.setStyleSheet("font-size: 12px; color: #9CA3AF;")

        layout.addWidget(icon)
        layout.addWidget(value)
        layout.addWidget(label)

        card.setLayout(layout)
        return card

    def abrir_cadastro_veiculo(self):
        self.close()
        self.tela = CadastroVeiculo(self.usuario)
        self.tela.show()

    def abrir_cadastro_viagem(self):
        self.close()
        self.tela = CadastroViagem(self.usuario)
        self.tela.show()

    def abrir_cadastro_manutencao(self):
        self.close()
        self.tela = CadastroManutencao(self.usuario)
        self.tela.show()

    def abrir_previsao(self):
        self.close()
        self.tela = PrevisaoCusto(self.usuario)
        self.tela.show()

    def logout(self):
        self.close()
        self.tela = Login()
        self.tela.show()


class TelaVeiculos(QWidget):
    def __init__(self, usuario, filtro="all"):
        super().__init__()
        self.usuario = usuario
        self.filtro = filtro
        self.setWindowTitle("Veículos")
        self.setFixedSize(430, 780)
        self.montar()

    def montar(self):
        main = QVBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)

        scroll, layout = criar_scroll()

        layout.addWidget(titulo("Veículos"))
        layout.addWidget(subtitulo("Gestão da frota institucional"))

        veiculos = veiculo_controller.listar()

        total = len(veiculos)
        ativos = len([v for v in veiculos if v.status == "active"])
        manutencao = len([v for v in veiculos if v.status == "maintenance"])

        stats = QGridLayout()
        stats.setSpacing(10)
        stats.addWidget(self.card_resumo(total, "Total", "#FFFFFF"), 0, 0)
        stats.addWidget(self.card_resumo(ativos, "Ativos", "#10B981"), 0, 1)
        stats.addWidget(self.card_resumo(manutencao, "Manutenção", "#F59E0B"), 0, 2)

        layout.addLayout(stats)
        layout.addLayout(self.filtros())

        if self.filtro == "all":
            filtrados = veiculos
        else:
            filtrados = [v for v in veiculos if v.status == self.filtro]

        if not filtrados:
            layout.addWidget(subtitulo("Nenhum veículo encontrado."))
        else:
            for veiculo in filtrados:
                layout.addWidget(self.card_veiculo(veiculo))

        btn = QPushButton("Adicionar Novo Veículo")
        btn.clicked.connect(self.abrir_cadastro)
        layout.addWidget(btn)
        layout.addStretch()

        main.addWidget(scroll)
        main.addLayout(criar_navbar(self, self.usuario, "vehicles"))

        self.setLayout(main)

    def card_resumo(self, valor, texto, cor):
        card = QFrame()
        card.setFixedSize(116, 82)

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)

        v = QLabel(str(valor))
        v.setAlignment(Qt.AlignCenter)
        v.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {cor};")

        t = QLabel(texto)
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet("font-size: 11px; color: #9CA3AF;")

        layout.addWidget(v)
        layout.addWidget(t)

        card.setLayout(layout)
        return card

    def filtros(self):
        layout = QHBoxLayout()
        layout.setSpacing(8)

        botoes = [
            ("Todos", "all"),
            ("Ativos", "active"),
            ("Manutenção", "maintenance")
        ]

        for texto, filtro in botoes:
            btn = botao_filtro(texto, self.filtro == filtro)
            btn.clicked.connect(lambda checked=False, f=filtro: self.trocar_filtro(f))
            layout.addWidget(btn)

        return layout

    def trocar_filtro(self, filtro):
        self.close()
        self.tela = TelaVeiculos(self.usuario, filtro)
        self.tela.show()

    def card_veiculo(self, v):
        card = QFrame()

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        topo = QHBoxLayout()

        nome = QLabel(f"{v.modelo}\n{v.placa}")
        nome.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")

        status_texto = "Ativo" if v.status == "active" else "Manutenção"
        status_cor = "#10B981" if v.status == "active" else "#F59E0B"

        status = QLabel(status_texto)
        status.setAlignment(Qt.AlignCenter)
        status.setStyleSheet(f"background-color: {status_cor}; border-radius: 12px; padding: 6px; font-size: 11px;")

        topo.addWidget(nome)
        topo.addStretch()
        topo.addWidget(status)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.info("📈", "Quilometragem", f"{v.quilometragem} km"), 0, 0)
        grid.addWidget(self.info("⛽", "Consumo", f"{v.consumo} km/l"), 0, 1)
        grid.addWidget(self.info("🛠️", "Próx. manutenção", f"{v.proxima_manutencao} km"), 1, 0)
        grid.addWidget(self.info("⛽", "Combustível", f"{v.combustivel}%"), 1, 1)

        layout.addLayout(topo)
        layout.addLayout(grid)

        card.setLayout(layout)
        return card

    def info(self, icone, texto, valor):
        card = QFrame()
        card.setStyleSheet("background-color: #20222D; border-radius: 18px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        label = QLabel(f"{icone} {texto}")
        label.setStyleSheet("font-size: 11px; color: #9CA3AF;")

        value = QLabel(valor)
        value.setStyleSheet("font-size: 13px; font-weight: bold; color: #FFFFFF;")

        layout.addWidget(label)
        layout.addWidget(value)

        card.setLayout(layout)
        return card

    def abrir_cadastro(self):
        self.close()
        self.tela = CadastroVeiculo(self.usuario)
        self.tela.show()


class TelaViagens(QWidget):
    def __init__(self, usuario, filtro="all"):
        super().__init__()
        self.usuario = usuario
        self.filtro = filtro
        self.setWindowTitle("Viagens")
        self.setFixedSize(430, 780)
        self.montar()

    def montar(self):
        main = QVBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)

        scroll, layout = criar_scroll()

        layout.addWidget(titulo("Viagens"))
        layout.addWidget(subtitulo("Histórico e agendamento de rotas"))

        viagens = viagem_controller.listar()

        total = len(viagens)
        agendadas = len([v for v in viagens if v.status == "scheduled"])
        andamento = len([v for v in viagens if v.status == "in-progress"])
        concluidas = len([v for v in viagens if v.status == "completed"])

        stats = QGridLayout()
        stats.setSpacing(8)
        stats.addWidget(self.card_resumo(total, "Total", "#FFFFFF"), 0, 0)
        stats.addWidget(self.card_resumo(agendadas, "Agendadas", "#06B6D4"), 0, 1)
        stats.addWidget(self.card_resumo(andamento, "Em curso", "#F59E0B"), 0, 2)
        stats.addWidget(self.card_resumo(concluidas, "Concluídas", "#10B981"), 0, 3)

        layout.addLayout(stats)
        layout.addLayout(self.filtros())

        if self.filtro == "all":
            filtradas = viagens
        else:
            filtradas = [v for v in viagens if v.status == self.filtro]

        if not filtradas:
            layout.addWidget(subtitulo("Nenhuma viagem encontrada."))
        else:
            for viagem in filtradas:
                layout.addWidget(self.card_viagem(viagem))

        btn = QPushButton("Agendar Nova Viagem")
        btn.clicked.connect(self.abrir_cadastro)
        layout.addWidget(btn)
        layout.addStretch()

        main.addWidget(scroll)
        main.addLayout(criar_navbar(self, self.usuario, "trips"))

        self.setLayout(main)

    def card_resumo(self, valor, texto, cor):
        card = QFrame()
        card.setFixedSize(82, 80)

        layout = QVBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)

        v = QLabel(str(valor))
        v.setAlignment(Qt.AlignCenter)
        v.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {cor};")

        t = QLabel(texto)
        t.setAlignment(Qt.AlignCenter)
        t.setWordWrap(True)
        t.setStyleSheet("font-size: 9px; color: #9CA3AF;")

        layout.addWidget(v)
        layout.addWidget(t)

        card.setLayout(layout)
        return card

    def filtros(self):
        layout = QHBoxLayout()
        layout.setSpacing(8)

        botoes = [
            ("Todas", "all"),
            ("Agendadas", "scheduled"),
            ("Em andamento", "in-progress"),
            ("Concluídas", "completed")
        ]

        for texto, filtro in botoes:
            btn = botao_filtro(texto, self.filtro == filtro)
            btn.clicked.connect(lambda checked=False, f=filtro: self.trocar_filtro(f))
            layout.addWidget(btn)

        return layout

    def trocar_filtro(self, filtro):
        self.close()
        self.tela = TelaViagens(self.usuario, filtro)
        self.tela.show()

    def card_viagem(self, v):
        card = QFrame()

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        status_map = {
            "scheduled": ("Agendada", "#06B6D4"),
            "in-progress": ("Em andamento", "#F59E0B"),
            "completed": ("Concluída", "#10B981")
        }

        texto_status, cor_status = status_map.get(v.status, ("Agendada", "#06B6D4"))

        topo = QHBoxLayout()

        rota = QLabel(f"{v.origem} → {v.destino}\n{v.distancia} km")
        rota.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")

        status = QLabel(texto_status)
        status.setAlignment(Qt.AlignCenter)
        status.setStyleSheet(f"background-color: {cor_status}; border-radius: 12px; padding: 6px; font-size: 11px;")

        topo.addWidget(rota)
        topo.addStretch()
        topo.addWidget(status)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.info("📅", "Data", v.data), 0, 0)
        grid.addWidget(self.info("⏰", "Horário", v.horario), 0, 1)
        grid.addWidget(self.info("👤", "Motorista", v.motorista), 1, 0)
        grid.addWidget(self.info("🚗", "Veículo", f"{v.veiculo_modelo}\n{v.veiculo_placa}"), 1, 1)

        layout.addLayout(topo)
        layout.addLayout(grid)

        card.setLayout(layout)
        return card

    def info(self, icone, texto, valor):
        card = QFrame()
        card.setStyleSheet("background-color: #20222D; border-radius: 18px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        label = QLabel(f"{icone} {texto}")
        label.setStyleSheet("font-size: 11px; color: #9CA3AF;")

        value = QLabel(str(valor))
        value.setStyleSheet("font-size: 13px; font-weight: bold; color: #FFFFFF;")

        layout.addWidget(label)
        layout.addWidget(value)

        card.setLayout(layout)
        return card

    def abrir_cadastro(self):
        self.close()
        self.tela = CadastroViagem(self.usuario)
        self.tela.show()


class CadastroVeiculo(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Cadastrar Veículo")
        self.setFixedSize(390, 740)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        layout.addWidget(titulo("Novo Veículo"))
        layout.addWidget(subtitulo("O status inicial será Ativo."))

        self.placa = QLineEdit()
        self.placa.setPlaceholderText("Placa")

        self.modelo = QLineEdit()
        self.modelo.setPlaceholderText("Modelo")

        self.tipo = QLineEdit()
        self.tipo.setPlaceholderText("Tipo")

        self.capacidade = QLineEdit()
        self.capacidade.setPlaceholderText("Capacidade")

        self.consumo = QLineEdit()
        self.consumo.setPlaceholderText("Consumo km/l")

        self.quilometragem = QLineEdit()
        self.quilometragem.setPlaceholderText("Quilometragem atual")

        self.proxima_manutencao = QLineEdit()
        self.proxima_manutencao.setPlaceholderText("Próxima manutenção em km")

        self.combustivel = QLineEdit()
        self.combustivel.setPlaceholderText("Combustível (%)")

        campos = [
            self.placa, self.modelo, self.tipo, self.capacidade,
            self.consumo, self.quilometragem, self.proxima_manutencao,
            self.combustivel
        ]

        for campo in campos:
            layout.addWidget(campo)

        btn_salvar = QPushButton("Salvar Veículo")
        btn_salvar.clicked.connect(self.salvar)

        btn_voltar = botao_secundario("Voltar")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(btn_salvar)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def salvar(self):
        sucesso, mensagem = veiculo_controller.cadastrar(
            self.placa.text(),
            self.modelo.text(),
            self.tipo.text(),
            self.capacidade.text(),
            self.consumo.text(),
            self.quilometragem.text(),
            self.proxima_manutencao.text(),
            self.combustivel.text()
        )

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.voltar()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def voltar(self):
        self.close()
        self.tela = TelaVeiculos(self.usuario)
        self.tela.show()


class CadastroViagem(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Cadastrar Viagem")
        self.setFixedSize(390, 760)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        layout.addWidget(titulo("Nova Viagem"))
        layout.addWidget(subtitulo("Agende uma nova rota da frota."))

        self.origem = QLineEdit()
        self.origem.setPlaceholderText("Origem")

        self.destino = QLineEdit()
        self.destino.setPlaceholderText("Destino")

        self.distancia = QLineEdit()
        self.distancia.setPlaceholderText("Distância em km")

        self.data = QLineEdit()
        self.data.setPlaceholderText("Data")

        self.horario = QLineEdit()
        self.horario.setPlaceholderText("Horário")

        self.motorista = QLineEdit()
        self.motorista.setPlaceholderText("Motorista")

        self.veiculo_combo = QComboBox()

        veiculos = veiculo_controller.listar()

        for i, veiculo in enumerate(veiculos):
            self.veiculo_combo.addItem(f"{i} - {veiculo.modelo} | {veiculo.placa}", i)

        self.status = QComboBox()
        self.status.addItem("Agendada", "scheduled")
        self.status.addItem("Em andamento", "in-progress")
        self.status.addItem("Concluída", "completed")

        campos = [
            self.origem, self.destino, self.distancia, self.data,
            self.horario, self.motorista
        ]

        for campo in campos:
            layout.addWidget(campo)

        layout.addWidget(self.veiculo_combo)
        layout.addWidget(self.status)

        btn_salvar = QPushButton("Salvar Viagem")
        btn_salvar.clicked.connect(self.salvar)

        btn_voltar = botao_secundario("Voltar")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(btn_salvar)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def salvar(self):
        if len(veiculo_controller.listar()) == 0:
            QMessageBox.warning(self, "Erro", "Cadastre um veículo primeiro.")
            return

        indice = self.veiculo_combo.currentData()
        veiculo = veiculo_controller.buscar_por_indice(indice)

        sucesso, mensagem = viagem_controller.cadastrar_viagem(
            self.origem.text(),
            self.destino.text(),
            self.distancia.text(),
            self.data.text(),
            self.horario.text(),
            self.motorista.text(),
            veiculo,
            self.status.currentData()
        )

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.voltar()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def voltar(self):
        self.close()
        self.tela = TelaViagens(self.usuario)
        self.tela.show()


class CadastroManutencao(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Cadastrar Manutenção")
        self.setFixedSize(390, 700)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        layout.addWidget(titulo("Nova Manutenção"))
        layout.addWidget(subtitulo("O veículo será marcado como Em manutenção."))

        self.veiculo_combo = QComboBox()

        veiculos = veiculo_controller.listar()

        for i, veiculo in enumerate(veiculos):
            self.veiculo_combo.addItem(f"{i} - {veiculo.modelo} | {veiculo.placa}", i)

        self.tipo = QLineEdit()
        self.tipo.setPlaceholderText("Tipo de manutenção")

        self.descricao = QLineEdit()
        self.descricao.setPlaceholderText("Descrição")

        self.valor = QLineEdit()
        self.valor.setPlaceholderText("Valor")

        self.data = QLineEdit()
        self.data.setPlaceholderText("Data")

        layout.addWidget(self.veiculo_combo)
        layout.addWidget(self.tipo)
        layout.addWidget(self.descricao)
        layout.addWidget(self.valor)
        layout.addWidget(self.data)

        btn_salvar = QPushButton("Salvar Manutenção")
        btn_salvar.clicked.connect(self.salvar)

        btn_voltar = botao_secundario("Voltar")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(btn_salvar)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def salvar(self):
        if len(veiculo_controller.listar()) == 0:
            QMessageBox.warning(self, "Erro", "Cadastre um veículo primeiro.")
            return

        indice = self.veiculo_combo.currentData()
        veiculo = veiculo_controller.buscar_por_indice(indice)

        sucesso, mensagem = custo_controller.adicionar(
            veiculo,
            self.tipo.text(),
            self.descricao.text(),
            self.valor.text(),
            self.data.text()
        )

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.voltar()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def voltar(self):
        self.close()
        self.tela = TelaVeiculos(self.usuario)
        self.tela.show()


class PrevisaoCusto(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Previsão de Custo")
        self.setFixedSize(430, 780)

        main = QVBoxLayout()
        main.setContentsMargins(26, 26, 26, 26)
        main.setSpacing(16)

        main.addWidget(titulo("Previsão de Custo"))
        main.addWidget(subtitulo("Simule o custo estimado de uma viagem."))

        self.distancia = QLineEdit()
        self.distancia.setPlaceholderText("Distância da viagem (km)")

        self.consumo = QLineEdit()
        self.consumo.setPlaceholderText("Consumo médio (km/l)")

        self.preco = QLineEdit()
        self.preco.setPlaceholderText("Preço do combustível")

        self.fator = QLineEdit()
        self.fator.setPlaceholderText("Fator de manutenção (%)")

        for campo in [self.distancia, self.consumo, self.preco, self.fator]:
            main.addWidget(campo)

        btn = QPushButton("Calcular Custo")
        btn.clicked.connect(self.calcular)

        self.resultado = QLabel("")
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("font-size: 34px; font-weight: bold; color: #ED145B;")

        self.detalhes = QLabel("")
        self.detalhes.setAlignment(Qt.AlignCenter)
        self.detalhes.setWordWrap(True)
        self.detalhes.setStyleSheet("font-size: 13px; color: #9CA3AF;")

        main.addWidget(btn)
        main.addWidget(self.resultado)
        main.addWidget(self.detalhes)
        main.addStretch()
        main.addLayout(criar_navbar(self, self.usuario, "costs"))

        self.setLayout(main)

    def calcular(self):
        try:
            distancia = float(self.distancia.text())
            consumo = float(self.consumo.text())
            preco = float(self.preco.text())
            fator = float(self.fator.text())

            custo = viagem_controller.prever_custo(distancia, consumo, preco, fator)
            litros = distancia / consumo
            combustivel = litros * preco
            manutencao = custo - combustivel

            self.resultado.setText(f"R$ {custo:.2f}")
            self.detalhes.setText(
                f"Litros necessários: {litros:.2f} L\n"
                f"Custo combustível: R$ {combustivel:.2f}\n"
                f"Custo manutenção: R$ {manutencao:.2f}"
            )

        except Exception:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos corretamente.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    janela = Login()
    janela.show()

    sys.exit(app.exec())