Projeto desenvolvido como parte do bootcamp de Python AI Backend Developer da **[DIO (Digital Innovation One)](https://dio.me/)**.

O objetivo deste projeto foi construir um sistema bancário em Python, evoluindo de uma versão procedural simples para um sistema robusto e completo baseado em **Programação Orientada a Objetos (POO)**.

## 🧠 O Desafio: De Procedural para Orientado a Objetos

O desafio principal foi refatorar um código procedural, aplicando os pilares da POO para criar um sistema mais organizado, manutenível e escalável, baseado em um diagrama UML.

**Principais conceitos de POO aplicados:**
* **Classes e Objetos:** `Cliente`, `PessoaFica`, `Conta`, `ContaCorrente`.
* **Abstração:** Criação de classes abstratas (`Transacao`, `Conta`) para definir "contratos" (interfaces).
* **Herança:** `Cliente` herda de `PessoaFica`, e `ContaCorrente` herda de `Conta`.
* **Polimorfismo:** `Saque` e `Deposito` são tratados como tipos de `Transacao`, cada um com sua própria implementação do método `registrar`.
* **Encapsulamento:** Separação clara de responsabilidades, onde a lógica de negócio (como `sacar`) não imprime na tela, apenas retorna o sucesso ou falha da operação.

---

## 🚀 Funcionalidades do Sistema (`projeto_banco.py`)

O sistema é controlado por um menu interativo no terminal e permite:

* **[1] Depositar:** Adiciona um valor ao saldo da conta.
* **[2] Sacar:** Permite sacar um valor, respeitando o saldo, um limite de R$ 500,00 por saque e um máximo de 3 saques diários.
* **[3] Extrato:** Exibe o histórico de transações e o saldo atual da conta.
* **[4] Nova Conta:** Cria uma nova conta corrente (Agência `0001`) para um usuário existente.
* **[5] Listar Contas:** Exibe todas as contas cadastradas.
* **[6] Novo Usuário:** Cadastra um novo cliente (Pessoa Física) no sistema.
* **[7] Listar Usuários:** Exibe todos os usuários cadastrados.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Programação Orientada a Objetos (POO)**
* Módulo `abc` (Abstract Base Classes) para criar interfaces e classes abstratas.
* Módulo `datetime` para registro de data e hora das transações.
* Módulo `textwrap` para formatação do menu.

---

## 🏁 Como Executar

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/ArthurDays/dio.git](https://github.com/ArthurDays/dio.git)
    ```
2.  Navegue até a pasta do projeto:
    ```bash
    cd dio
    ```
3.  Execute o script principal do sistema bancário:
    ```bash
    python projeto_banco.py
    ```
4.  Siga as instruções do menu interativo no terminal.

---

## 👨‍💻 ArthurDays
