# 🚗 FleetTrack FIAP — Sistema de Gerenciamento de Frota

## 📌 Descrição do Problema

A gestão de veículos institucionais, como os ônibus fretados da FIAP (FIAPÃO), muitas vezes é realizada de forma manual ou descentralizada, o que pode gerar:

Falta de controle operacional da frota
Dificuldade no acompanhamento de viagens
Ausência de controle de manutenções
Erros na estimativa de custos
Baixa eficiência na tomada de decisão
---

## 🚀 Solução Proposta

O FleetTrack FIAP é um sistema desktop desenvolvido em Python que centraliza o gerenciamento da frota institucional, permitindo:

Controle completo de veículos
Gerenciamento de viagens (rotas)
Controle de manutenções
Atualização automática de status dos veículos
Cálculo de custo de combustível por viagem
Interface gráfica moderna e intuitiva
---

## 🛠️ Tecnologias Utilizadas

Python 3.11
PySide6 (Interface gráfica)
JSON (persistência de dados)
Arquitetura em camadas (Models, Controllers, Services, Utils)

---

## ⚙️ Como Executar

```
pip install PySide6
python app.py
```

---

## 📂 Estrutura do Projeto

```
fleettrack/
├── app.py
├── models/
│   ├── usuario.py
│   ├── veiculo.py
│   ├── viagem.py
│   ├── custo.py
├── controllers/
│   ├── usuario_controller.py
│   ├── veiculo_controller.py
│   ├── viagem_controller.py
│   ├── custo_controller.py
├── services/
│   ├── persistencia.py
├── utils/
│   ├── validacoes.py
```

---

## 🧩 Funcionalidades Implementadas

## Autenticação
Cadastro de usuário (UC01)
Login de usuário (UC02)
Bloqueio de acesso sem autenticação

## Veículos
Cadastro de veículos institucionais (UC03)
Listagem de veículos
Filtro por status (ativo / manutenção)
Exclusão de veículos

## Viagens (Rotas)
Cadastro de viagens (UC04)
Listagem de viagens
Filtro por status (agendada / em andamento / concluída)
Atualização de status da viagem
Exclusão de viagens

## Manutenções
Cadastro de manutenções
Alteração automática do status do veículo
Conclusão de manutenção
Retorno automático do veículo para ativo
Histórico de manutenções

## Dashboard
Resumo de veículos (total, ativos, em manutenção)
Resumo de viagens (agendadas, em andamento, concluídas)

## Custos
Cálculo de custo de combustível (UC05 - Diferencial)
Histórico de previsões de custo

---

## 🧠 Diferencial

O sistema possui um módulo de previsão de custo que calcula automaticamente o gasto estimado de combustível de uma viagem com base em:

Distância da viagem
Consumo médio do veículo
Preço do combustível

##Benefícios
Auxilia no planejamento financeiro
Reduz erros de estimativa manual
Simula cenários reais de operação

## Benefícios
Auxilia no planejamento financeiro
Reduz erros de estimativa manual
Simula cenários reais de operação


## Limitações

Nesta versão, o sistema não inclui:
Integração com banco de dados externo (MySQL, PostgreSQL)
Sistema de múltiplos níveis de usuário (admin/operador)
Integração com APIs externas (mapas, combustível em tempo real)
Rastreamento em tempo real dos veículos

---

## 👨‍💻 Integrantes do Grupo

* Leonardo Medeiros (commits: feat, docs) (RM559220)
* Arthur Bergamaço (commits: feat, refactor) (RM556207)
* Breno Barbosa (commits: feat, test) (RM555348)
* Renan Melo (commits: docs, feat) (RM558535)
* Pietro Rodriguez (commits: feat) (RM555899)
* Mateus Souza (commits: test, docs) (RM559118)

---

## 🔗 Links

* Repositório: https://github.com/LMedeiros-Silva/FleetTrack
* Miro: (https://miro.com/app/board/uXjVGpfw9Tc=/)
* Vídeo: (https://youtu.be/cMjPn5fjZrM)
