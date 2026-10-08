# Trading_Master
![Visualização do Painel](dashboard.png)

# 📊 Gestor de Trade Pro 

Uma aplicação gerencial moderna voltada para o mercado financeiro (B3), desenvolvida em **Python** com **CustomTkinter** e **Pandas**. O software resolve de forma automatizada o maior problema do investidor de ações: a apuração do preço médio, lucros mensais, lucros anuais acumulados e rentabilidade real da carteira.

---

## 🎯 Funcionalidades Principais

* **✍️ Lançamento Manual Adaptativo:** Caso o usuário deseje, o app possui um formulário completo para registrar transações individuais.
* **📈 Métricas Anuais:** Exibe de forma centralizada o lucro/prejuízo exato do mês atual e o acumulado do ano fiscal corrente.
* **🗃️ Banco de Dados em Excel Integrado:** Toda operação alimenta uma planilha local estruturada (`historico_trades.xlsx`) sem depender de internet.
* **🧽 Remoção Automática de Duplicidades:** Filtros inteligentes que evitam que a mesma linha seja computada duas vezes por engano.

---

## 🛠️ Tecnologias Utilizadas

* **Python** (Linguagem Principal)
* **CustomTkinter** (Interface Gráfica com Suporte a Modo Escuro Automático do Windows)
* **Pandas** (Engenharia de Dados e Relatórios Financeiros)
** **PyInstaller** (Empacotamento para Executável Nativo `.exe`)

---

## 💻 Como Executar o Projeto

Se você quiser rodar o código direto pelo ambiente de desenvolvimento (Jupyter Notebook/VS Code):

1. Clone este repositório:
```bash
git clone https://github.com[seu-usuario]/[nome-do-repositorio].git
```

2. Instale as bibliotecas requeridas:
```bash
pip install customtkinter pandas openpyxl pdfplumber pyinstaller
```

3. Execute o programa principal:
```bash
python calculadora_trade2.py
```

### 📦 Como Gerar o Executável (.exe)
Para compilar este script em um aplicativo independente para a Área de Trabalho sem console preto, execute:
```bash
pyinstaller --clean --noconsole --onefile --exclude-module matplotlib calculadora_trade2.py
```

---

## 📄 Licença e Uso Comercial
Este projeto é de código aberto e está disponível sob a licença MIT. Você é totalmente livre para clonar, estudar, adaptar ou até comercializar esta ferramenta gerencial de aplicações financeiras!

---
Desenvolvido por **[Jardeilsom Oliveira]** 🚀 | Conecte-se comigo no [LinkedIn](www.linkedin.com/in/jardeilsomoliveira)
