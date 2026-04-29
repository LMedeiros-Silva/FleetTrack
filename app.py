import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout, QFrame, QMessageBox
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
custo_controller = CustoController()


STYLE = """
QWidget {
    background-color: #101014;
    color: #FFFFFF;
    font-family: Arial;
}

QLineEdit {
    background-color: #1E1E24;
    border: 1px solid #2A2A33;
    border-radius: 14px;
    padding: 12px;
    color: white;
    font-size: 14px;
}

QPushButton {
    background-color: #ED145B;
    color: white;
    border: none;
    border-radius: 14px;
    padding: 12px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #c9104b;
}

QFrame {
    background-color: #1E1E24;
    border-radius: 18px;
}
"""


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
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #ED145B;")

        subtitulo = QLabel("Gestão inteligente da frota institucional")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("font-size: 13px; color: #B8B8C0;")

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
        layout.addSpacing(35)
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
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #ED145B;")

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
        self.setFixedSize(430, 720)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 30, 25, 25)
        layout.setSpacing(18)

        titulo = QLabel("FleetTrack FIAP")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #ED145B;")

        saudacao = QLabel(f"Olá, {usuario.nome}!")
        saudacao.setStyleSheet("font-size: 16px; color: #FFFFFF;")

        grid = QGridLayout()
        grid.setSpacing(14)

        grid.addWidget(self.card("Veículos", str(len(veiculo_controller.listar()))), 0, 0)
        grid.addWidget(self.card("Rotas", str(len(rota_controller.listar()))), 0, 1)
        grid.addWidget(self.card("Viagens", str(len(viagem_controller.listar()))), 1, 0)
        grid.addWidget(self.card("Custos", f"R$ {custo_controller.total_custos():.2f}"), 1, 1)

        btn_veiculo = QPushButton("Cadastrar Veículo")
        btn_veiculo.clicked.connect(self.abrir_cadastro_veiculo)

        btn_rota = QPushButton("Cadastrar Rota")
        btn_rota.clicked.connect(self.abrir_cadastro_rota)

        btn_previsao = QPushButton("Previsão de Custo")
        btn_previsao.clicked.connect(self.abrir_previsao)

        btn_sair = QPushButton("Sair")
        btn_sair.clicked.connect(self.sair)

        layout.addWidget(titulo)
        layout.addWidget(saudacao)
        layout.addLayout(grid)
        layout.addWidget(btn_veiculo)
        layout.addWidget(btn_rota)
        layout.addWidget(btn_previsao)
        layout.addWidget(btn_sair)
        layout.addStretch()

        self.setLayout(layout)

    def card(self, titulo, valor):
        frame = QFrame()
        frame.setFixedSize(175, 105)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 12, 15, 12)

        valor_label = QLabel(valor)
        valor_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #ED145B;")

        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("font-size: 13px; color: #B8B8C0;")

        layout.addWidget(valor_label)
        layout.addWidget(titulo_label)
        frame.setLayout(layout)

        return frame

    def abrir_cadastro_veiculo(self):
        self.close()
        self.tela = CadastroVeiculo(self.usuario)
        self.tela.show()

    def abrir_cadastro_rota(self):
        self.close()
        self.tela = CadastroRota(self.usuario)
        self.tela.show()

    def abrir_previsao(self):
        self.close()
        self.tela = PrevisaoCusto(self.usuario)
        self.tela.show()

    def sair(self):
        self.close()
        self.login = Login()
        self.login.show()


class CadastroVeiculo(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Cadastrar Veículo")
        self.setFixedSize(390, 650)

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(15)

        titulo = QLabel("Cadastrar Veículo")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #ED145B;")

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

        layout.addWidget(titulo)
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

        titulo = QLabel("Cadastrar Rota")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #ED145B;")

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

        layout.addWidget(titulo)
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


class PrevisaoCusto(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Previsão de Custo")
        self.setFixedSize(390, 650)

        layout = QVBoxLayout()
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(15)

        titulo = QLabel("Previsão de Custo")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #ED145B;")

        descricao = QLabel("Simule o custo operacional de uma viagem.")
        descricao.setStyleSheet("font-size: 13px; color: #B8B8C0;")

        self.distancia = QLineEdit()
        self.distancia.setPlaceholderText("Distância da viagem em km")

        self.consumo = QLineEdit()
        self.consumo.setPlaceholderText("Consumo médio do veículo km/l")

        self.preco = QLineEdit()
        self.preco.setPlaceholderText("Preço do combustível por litro")

        btn_calcular = QPushButton("Calcular Custo")
        btn_calcular.clicked.connect(self.calcular)

        self.resultado = QLabel("")
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("font-size: 28px; font-weight: bold; color: #ED145B;")

        self.detalhes = QLabel("")
        self.detalhes.setAlignment(Qt.AlignCenter)
        self.detalhes.setStyleSheet("font-size: 13px; color: #B8B8C0;")

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.voltar)

        layout.addWidget(titulo)
        layout.addWidget(descricao)
        layout.addSpacing(20)
        layout.addWidget(self.distancia)
        layout.addWidget(self.consumo)
        layout.addWidget(self.preco)
        layout.addWidget(btn_calcular)
        layout.addSpacing(20)
        layout.addWidget(self.resultado)
        layout.addWidget(self.detalhes)
        layout.addWidget(btn_voltar)
        layout.addStretch()

        self.setLayout(layout)

    def calcular(self):
        try:
            distancia = float(self.distancia.text())
            consumo = float(self.consumo.text())
            preco = float(self.preco.text())

            custo = viagem_controller.prever_custo(distancia, consumo, preco)
            litros = distancia / consumo
            manutencao = custo - (litros * preco)

            self.resultado.setText(f"R$ {custo:.2f}")
            self.detalhes.setText(
                f"Litros necessários: {litros:.2f} L\n"
                f"Manutenção preventiva: R$ {manutencao:.2f}"
            )

        except ValueError:
            QMessageBox.warning(self, "Erro", "Preencha os campos com números válidos.")

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