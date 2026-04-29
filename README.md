# 🚗 FleetTrack FIAP — Sistema de Gerenciamento de Frota

## 📌 Descrição do Problema

A gestão de veículos institucionais, como ônibus fretados e veículos administrativos, muitas vezes é feita de forma manual ou descentralizada, o que pode gerar:

* Falta de controle operacional
* Dificuldade no planejamento de rotas
* Erros no cálculo de custos
* Baixa eficiência na tomada de decisão

---

## 🚀 Solução Proposta

Desenvolvimento de um sistema em Python para gerenciamento de frota institucional da FIAP, permitindo:

* Cadastro de veículos (incluindo ônibus FIAPÃO)
* Cadastro de rotas
* Controle de viagens
* Simulação e previsão de custos operacionais
* Interface gráfica moderna para melhor experiência do usuário

---

## 🛠️ Tecnologias Utilizadas

* Python 3.11
* PySide6 (Interface gráfica)
* Arquitetura MVC

---

## ⚙️ Como Executar

```bash
pip install PySide6
python app.py
```

---

## 📂 Estrutura do Projeto

```text
fleettrack/
├── app.py
├── models/
├── controllers/
├── services/
├── utils/
```

---

## 🧩 Funcionalidades Implementadas

* Login de usuário (UC01)
* Cadastro de usuário (UC02)
* Cadastro de veículos institucionais (UC03)
* Cadastro de rotas (UC04)
* Visualização no dashboard (UC05)
* Previsão de custo de viagem (UC06 - Diferencial)

---

## 🧠 Diferencial

O sistema possui um módulo de **previsão inteligente de custo**, que calcula automaticamente o custo de uma viagem com base em:

* Distância
* Consumo do veículo
* Preço do combustível
* Taxa de manutenção preventiva

Esse recurso simula um cenário real de gestão de frota e auxilia na tomada de decisão.

---

## 📸 Demonstração

(Coloque aqui o link do seu vídeo atualizado)

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
