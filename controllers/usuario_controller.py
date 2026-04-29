from models.usuario import Usuario
from utils.validacoes import validar_texto

class UsuarioController:
    def __init__(self):
        self.usuarios = []

    def cadastrar(self, nome, email, senha, confirmar_senha):
        if not validar_texto(nome):
            return False, "Nome inválido."

        if not validar_texto(email) or "@" not in email:
            return False, "Email inválido."

        if not validar_texto(senha):
            return False, "Senha inválida."

        if senha != confirmar_senha:
            return False, "As senhas não conferem."

        for usuario in self.usuarios:
            if usuario.email == email:
                return False, "Email já cadastrado."

        usuario = Usuario(nome, email, senha)
        self.usuarios.append(usuario)

        return True, "Cadastro realizado com sucesso."

    def login(self, email, senha):
        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                return usuario

        return None