def calcular_custo(distancia, consumo, preco_combustivel):
    litros_necessarios = distancia / consumo
    custo_combustivel = litros_necessarios * preco_combustivel
    custo_manutencao = custo_combustivel * 0.15
    custo_total = custo_combustivel + custo_manutencao

    return round(custo_total, 2)