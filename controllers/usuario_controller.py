import hashlib

from models.usuario import Usuario
from utils.validacoes import validar_texto
from services.persistencia import Persistencia


class UsuarioController:
    def __init__(self):
        self.usuarios = []
        self.carregar_usuarios()

    def gerar_hash(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def carregar_usuarios(self):
        dados = Persistencia.carregar("usuarios.json")

        for item in dados:
            usuario = Usuario(
                item["nome"],
                item["email"],
                item["senha"]
            )
            self.usuarios.append(usuario)

    def salvar_usuarios(self):
        dados = []

        for usuario in self.usuarios:
            dados.append({
                "nome": usuario.nome,
                "email": usuario.email,
                "senha": usuario.senha
            })

        Persistencia.salvar("usuarios.json", dados)

    def cadastrar(self, nome, email, senha, confirmar_senha):
        if not validar_texto(nome):
            return False, "Nome inválido."

        if not validar_texto(email) or "@" not in email or "." not in email:
            return False, "Email inválido."

        if not validar_texto(senha) or len(senha) < 6:
            return False, "A senha deve ter no mínimo 6 caracteres."

        if senha != confirmar_senha:
            return False, "As senhas não conferem."

        for usuario in self.usuarios:
            if usuario.email == email:
                return False, "Email já cadastrado."

        senha_hash = self.gerar_hash(senha)

        usuario = Usuario(nome, email, senha_hash)
        self.usuarios.append(usuario)
        self.salvar_usuarios()

        return True, "Cadastro realizado com sucesso."

    def login(self, email, senha):
        if not validar_texto(email):
            return None

        if not validar_texto(senha):
            return None

        senha_hash = self.gerar_hash(senha)

        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha_hash:
                return usuario

        return None