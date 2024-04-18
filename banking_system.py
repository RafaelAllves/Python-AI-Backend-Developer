import textwrap
from datetime import datetime
from abc import ABC, abstractmethod


class Cliente():
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta():
    def __init__(self, numero, cliente):
        self._agencia = "0001"
        self._numero = numero
        self._saldo = 0
        self._cliente = cliente
        self._historico = Historico()

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    def depositar(self, valor):
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        self._saldo += valor
        return True
    
    def sacar(self, valor):
        if valor > self._saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False
        
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        self._saldo -= valor
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self.limite = 500
        self.limite_saques = 3
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        if numero_saques >= self.limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False
        
        if valor > self.limite:
            print("Operação falhou! O valor do saque excede o limite.")
            return False
        
        return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico():
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass
    

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

LIMITE_SAQUES = 3

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
contas = []
clientes = []

def depositar():
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return
    
    if not cliente.contas:
        print("O cliente não possui contas!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = cliente.contas[0]
    if not conta:
        print("Conta não encontrada!")
        return

    cliente.realizar_transacao(conta, transacao)

def sacar():
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado!")
        return
    
    if not cliente.contas:
        print("O cliente não possui contas!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = cliente.contas[0]
    if not conta:
        print("Conta não encontrada!")
        return

    cliente.realizar_transacao(conta, transacao)

def mostrar_extrato():

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    if not cliente.contas:
        print("O cliente não possui contas!")
        return
    
    conta = cliente.contas[0]
    if not conta:
        print("Conta não encontrada!")
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    if not cpf.isdigit():
        print("CPF inválido! Apenas números são permitidos!")
        return

    if filtrar_clientes(cpf, clientes):
        print("Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)

    clientes.append(cliente)

    print("=== Cliente criado com sucesso! ===")

def filtrar_clientes(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def criar_conta(clientes, contas):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, fluxo de criação de conta encerrado!")
        return None

    numero_conta = input("Informe o número da conta: ")
    
    conta = ContaCorrente.nova_conta(numero_conta, cliente)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")
    return 

def listar_contas(contas):

    if not contas:
        print("Não existem contas cadastradas!")
        return
    for conta in contas:
        linha = f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
        """
        print("=" * 42)
        print(textwrap.dedent(linha))

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar conta
[u] Criar cliente
[l] Listar contas
[q] Sair

=> """

while True:
    opcao = input(menu)

    if opcao == "d":
        depositar()

    elif opcao == "s":
        sacar()

    elif opcao == "e":
        mostrar_extrato()

    elif opcao == "c":
        conta = criar_conta(clientes, contas)
        if conta:
            contas.append(conta)

    elif opcao == "u":
        criar_cliente(clientes)

    elif opcao == "l":
        listar_contas(contas)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
