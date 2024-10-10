from abc import ABC, abstractmethod
from datetime import datetime
import textwrap
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco 
        self._contas = []

    def transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nasc, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nasc = data_nasc

class Contas(Cliente):

    
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero 
        self._agencia = "0001" 
        self._cliente = cliente 
        self._historico = Historico()
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    

    def sacar(self, valor):

        excedeu_saldo = valor > self._saldo

        if excedeu_saldo:
            print("O valor a ser sacado é meior que o saldo atual!")

        elif valor > 0:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True

        else:
            print("OPS! Ocorreu um erro inesperado, por favor tente novamente mais tarde!")
            return False
        
    
    def depositar(self, valor):
        
        if valor > 0:
            self._saldo += valor
            print('Deposito realizado com sucesso! ')
            return True

        else:
            print("O valor a ser depositado pode estar errado, por favor confirme novamente!")
            return False

class ContaCorrente(Contas):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque 

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self._historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self._limite
        excedeu_saque = numero_saques > self._limite_saque

        if excedeu_limite:
            print("\n O valor excedeu seu límite!")
        elif excedeu_saque:
            print("\n Você excedeu seus saques diarios")

        else:
            return super().sacar(valor)
        return False


    def __str__(self):
        return f"""\n 
Agência:\t{self._agencia}\n 
C/C:\t\t{self._numero}\n 
Titular:\t{self._cliente._nome}"""

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def add_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("id-%d-%m-%Y %H:%M:%S"),
            }
        )

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
        sucesso_transacao = conta.sacar(self._valor)

        if sucesso_transacao:
            conta.historico.add_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor 

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.add_transacao(self)

def menu():

    menu = """\n
    __________________  MENU  __________________
    [1]\t Depositar
    [2]\t Sacar
    [3]\t Extrato
    [4]\t Novo usuário
    [5]\t Nova conta
    [6]\t Listar contas
    [7]\t Sair
    => """
    return input(textwrap.dedent(menu))

def recuperar_conta_cliente(cliente):
    if not cliente._contas:
        print("\n Cliente não possui conta!")
        return 
    # FIXME: não permite o cliente escolhar a conta
    return cliente._contas[0]

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente._cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def depositar(clientes):
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n Cliente não encontrado! ')
        return 
    
    valor = float(input("Informe o valor do deposito: R$"))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.transacao(conta, transacao)

def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n Cliente não encontrado!')
        return 
    valor = float(input('Digite o valor a ser sacado: R$'))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.transacao(conta, transacao)

def exibir_extrato(clientes):
    
    cpf = input('Infore o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print('\n____________________ EXTRATO ___________________')
    transacoes = conta.historico.transacoes 

    extrato = ""
    if not transacoes:
        extrato = "Não  foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    
    print(extrato)
    print(f'\nSaldo:\n\tR$: {conta.saldo:.2f}')
    print("____________________________________")

def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPS do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado, criação de conta cancelada!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente._contas.append(conta)

    print('\n Conta criada com sucesso! ')

def listar_contas(contas):  
    for conta in contas:
        print('_' * 100)
        print(textwrap.dedent(str(conta)))

def criar_cliente(clientes):
    cpf = input('Informe o CPF (somente números): ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('\n Já existe um cliente cadastrado com esse CPF, por favor, verifique!')
        return

    nome = input('Informe seu nome completo: ')
    data_nascimento = input('Informe sua data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereco ( logradouro, nro - bairro - cidade/sigla estado): ')

    cliente = PessoaFisica(nome=nome, data_nasc=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('\n Cliente criado com sucesso!')

def main():
    clientes = []
    contas = []

    while True: 
        opcao = menu()

        if opcao == '1':
            depositar(clientes)
        
        elif opcao == '2':
            sacar(clientes)
        
        elif opcao == '3':
            exibir_extrato(clientes)

        elif opcao == '4':
            criar_cliente(clientes)
        
        elif opcao == '5':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == '6':
            listar_contas(contas)

        elif opcao == '7':
            break

        else:
            print('OPS! Você digitou uma opção inválida')

main()