import textwrap
from abc import ABC, abstractmethod
from datetime import datetime, date

# ===================================================================
# 1. DEFINIÇÃO DAS CLASSES (Sem alterações)
# ===================================================================

class PessoaFisica:
    def __init__(self, nome: str, data_nascimento: date, cpf: str):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Cliente(PessoaFisica):
    def __init__(self, endereco: str, **kwargs):
        super().__init__(**kwargs)
        self.endereco = endereco
        self.contas = [] 

    def adicionar_conta(self, conta: 'Conta'):
        self.contas.append(conta)

    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao'):
        return transacao.registrar(conta)


class Transacao(ABC):
    def __init__(self, valor: float):
        self.valor = valor
        self.data = datetime.now()

    @property
    @abstractmethod
    def tipo(self) -> str:
        pass

    @abstractmethod
    def registrar(self, conta: 'Conta') -> tuple[bool, str | None]:
        pass

class Deposito(Transacao):
    @property
    def tipo(self) -> str:
        return "Depósito"

    def registrar(self, conta: 'Conta') -> tuple[bool, str | None]:
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(self)
            return (True, None)
        else:
            return (False, "O valor informado é inválido.")


class Saque(Transacao):
    @property
    def tipo(self) -> str:
        return "Saque"

    def registrar(self, conta: 'Conta') -> tuple[bool, str | None]:
        excedeu_saldo = self.valor > conta.saldo
        
        if self.valor <= 0:
             return (False, "O valor informado é inválido.")
             
        if excedeu_saldo:
            return (False, "Você não tem saldo suficiente.")

        if isinstance(conta, ContaCorrente):
            excedeu_limite = self.valor > conta.limite
            excedeu_saques = conta.numero_saques >= conta.limite_saques

            if excedeu_limite:
                return (False, "O valor do saque excede o limite.")
            elif excedeu_saques:
                return (False, "Número máximo de saques excedido.")
            
            conta.numero_saques += 1
        
        conta.saldo -= self.valor
        conta.historico.adicionar_transacao(self)
        return (True, None)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(transacao)

    def gerar_extrato(self, saldo_atual: float) -> str:
        extrato_str = "\n================ EXTRATO ================\n"
        if not self._transacoes:
            extrato_str += "Não foram realizadas movimentações.\n"
        else:
            for transacao in self._transacoes:
                extrato_str += f"{transacao.tipo}:\tR$ {transacao.valor:.2f} \t({transacao.data.strftime('%d-%m-%Y %H:%M:%S')})\n"
        
        extrato_str += f"\nSaldo:\t\tR$ {saldo_atual:.2f}\n"
        extrato_str += "=========================================="
        return extrato_str


class Conta(ABC):
    def __init__(self, numero: int, cliente: Cliente):
        self._saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()
        cliente.adicionar_conta(self)

    @property
    def saldo(self) -> float:
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor: float):
        self._saldo = valor

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> 'Conta':
        return ContaCorrente(numero=numero, cliente=cliente)

    def exibir_extrato(self):
        extrato_string = self.historico.gerar_extrato(self.saldo)
        print(extrato_string)
        

class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

# ===================================================================
# 2. FUNÇÕES AUXILIARES (UI - Interface do Usuário)
# ===================================================================

def menu():
    """
    *** MENU ATUALIZADO COM A OPÇÃO [7] ***
    """
    menu_texto = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tListar usuários
    [0]\tSair
    => """
    return input(textwrap.dedent(menu_texto))


def filtrar_usuario(cpf: str, usuarios: list[Cliente]) -> Cliente | None:
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def selecionar_conta(cliente: Cliente) -> Conta | None:
    if not cliente.contas:
        print("\n@@@ Cliente não possui contas cadastradas! @@@")
        return None
    
    if len(cliente.contas) == 1:
        return cliente.contas[0]
    
    print("\nCliente possui múltiplas contas:")
    for i, conta in enumerate(cliente.contas):
        print(f"  [{i+1}] Agência: {conta.agencia} | Conta: {conta.numero}")
    
    while True:
        try:
            escolha_str = input(f"Digite o número da conta (1 a {len(cliente.contas)}): ")
            escolha_idx = int(escolha_str) - 1
            if 0 <= escolha_idx < len(cliente.contas):
                return cliente.contas[escolha_idx]
            else:
                print("\n@@@ Opção inválida! @@@")
        except ValueError:
            print("\n@@@ Entrada inválida. Digite apenas o número. @@@")


def criar_usuario(usuarios: list[Cliente]):
    cpf = input("Informe o seu CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Parece que já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o seu nome completo: ")
    data_nascimento_str = input("Informe a data do seu nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o seu endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    try:
        data_nascimento_obj = datetime.strptime(data_nascimento_str, "%d-%m-%Y").date()
    except ValueError:
        print("\n@@@ Data de nascimento em formato inválido! Cadastro cancelado. @@@")
        return

    novo_cliente = Cliente(
        nome=nome,
        data_nascimento=data_nascimento_obj,
        cpf=cpf,
        endereco=endereco
    )
    
    usuarios.append(novo_cliente)
    print("\n=== Usuário criado com sucesso! ===")


def criar_conta(numero_conta: int, usuarios: list[Cliente], contas: list[Conta]):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_usuario(cpf, usuarios)

    if cliente:
        nova_conta = ContaCorrente(numero=numero_conta, cliente=cliente)
        contas.append(nova_conta)
        print("\n=== Conta criada com sucesso! ===")
    else:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas: list[Conta]):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return
        
    for conta in contas:
        linha = f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# *** NOVA FUNÇÃO ADICIONADA AQUI ***
def listar_usuarios(usuarios: list[Cliente]):
    """Exibe uma lista de todos os usuários cadastrados."""
    print("\n--- Lista de Usuários Cadastrados ---")
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado. @@@")
        return
        
    for i, usuario in enumerate(usuarios):
        print("=" * 100)
        print(f"Usuário #{i+1}")
        print(f"Nome:\t\t{usuario.nome}")
        print(f"CPF:\t\t{usuario.cpf}")
        print(f"Nascimento:\t{usuario.data_nascimento.strftime('%d/%m/%Y')}")
        print(f"Endereço:\t{usuario.endereco}")
    print("=" * 100)


# ===================================================================
# 3. FUNÇÃO PRINCIPAL (UI - Lógica de Interface)
# ===================================================================

def main():
    usuarios: list[Cliente] = []
    contas: list[Conta] = []

    while True:
        opcao = menu()

        if opcao == "1": # Depositar
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_usuario(cpf, usuarios)
            
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue 
                
            conta = selecionar_conta(cliente)
            if not conta:
                continue 

            try:
                valor = float(input("Informe o valor do depósito: "))
                transacao = Deposito(valor)
                sucesso, mensagem_erro = cliente.realizar_transacao(conta, transacao)
                
                if sucesso:
                    print("\n=== Depósito realizado com sucesso! ===")
                else:
                    print(f"\n@@@ Operação falhou! {mensagem_erro} @@@")
                    
            except ValueError:
                print("\n@@@ Valor inválido! Digite um número. @@@")


        elif opcao == "2": # Sacar
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_usuario(cpf, usuarios)
            
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
                
            conta = selecionar_conta(cliente)
            if not conta:
                continue

            try:
                valor = float(input("Informe o valor do saque: "))
                transacao = Saque(valor)
                sucesso, mensagem_erro = cliente.realizar_transacao(conta, transacao)

                if sucesso:
                    print("\n=== Saque realizado com sucesso! ===")
                else:
                    print(f"\n@@@ Operação falhou! {mensagem_erro} @@@")
                    
            except ValueError:
                print("\n@@@ Valor inválido! Digite um número. @@@")


        elif opcao == "3": # Extrato
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_usuario(cpf, usuarios)
            
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
                
            conta = selecionar_conta(cliente)
            if not conta:
                continue
            
            conta.exibir_extrato()


        elif opcao == "6": # Novo usuário
            criar_usuario(usuarios)

        elif opcao == "4": # Nova conta
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, usuarios, contas)

        elif opcao == "5": # Listar contas
            listar_contas(contas)
            
        # *** NOVA OPÇÃO ADICIONADA AQUI ***
        elif opcao == "7": # Listar usuários
            listar_usuarios(usuarios)

        elif opcao == "0": # Sair
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


# Executa o programa
main()