import re

def validar_texto(texto):
    return texto.strip() != ""

def validar_numero_positivo(valor):
    try:
        numero = int(valor)
        return numero > 0
    except ValueError:
        return False

def validar_float_positivo(valor):
    try:
        numero = float(valor)
        return numero > 0
    except ValueError:
        return False

def validar_placa(placa):
    placa = placa.upper().replace("-", "").strip()

    padrao_antigo = r"^[A-Z]{3}[0-9]{4}$"
    padrao_mercosul = r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$"

    return bool(
        re.match(padrao_antigo, placa) or
        re.match(padrao_mercosul, placa)
    )