
def menu():
    menu = """\n
    __________________  MENU  __________________
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova conta
    [5] Novo usuário
    [6] Sair
    => """
    return input(menu)


def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f'\tDepósito: R$ {valor:.2f}\n'
        print('Depósito realizado com sucesso!')

    else:
        print('O valor inserido é inválido. Por favor, tente novamente!')

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saque = numero_saques >= limite_saques

    if excedeu_saldo:
        print('O valor insérido é maior que o saldo atual!')
    elif excedeu_limite:
        print('O valor inserido é maior que o seu limite!')
    elif excedeu_saque:
        print('Você já atingiu seu limite de saques diários!')

    elif valor > 0:
        saldo -= valor
        extrato += f'\tSaque: R$ {valor:.2f}\n'
        print('Saque realizado com sucesso!')
        
    else:
        print('O valor digitado é inválido')

    return saldo, extrato
    
def exibir_extrato(saldo,/, *, extrato):
     
     print('\n-------------------Extrato-------------------')
     print('Não foram realizadas movimentações.' if not extrato else extrato)
     print(f'\n\tSaldo: R${saldo:.2f}')
     print('-----------------------------------------------')

def criar_usuario(usuarios):
    cpf = input('Digite seu CPF (somente números): ')
    usuario = filtrar_users(cpf, usuarios)

    if usuario:
        print(" CPF já utilizado por outro usuario!")
        return
    nome = input('Digite seu nome completo: ')
    data_nasc = input('Informe sua data de nascimento (ex: 19-08-1990): ')
    endereco = input('Digite seu endereço (logradouro, nro - bairro - cidade/sigla estado): ')
    usuarios.append({'nome': nome, 'data_nascimento': data_nasc, 'endereço': endereco, 'cpf': cpf})
    print('Usuario registrado com sucesso!')

def filtrar_users(cpf, usuarios):

    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Digite seu CPF: ')
    usuario = filtrar_users(cpf, usuarios)

    if usuario:
        print(' Conta criada com sucesso!')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
    print('Não foi possível encontrar esse usuário, certifique-se de ter um usuário criado!')

def main():
    saldo = 0
    limite = 500
    extrato = ''
    numeros_saques = 0
    usuarios = []
    contas = []
    conta_id = 1
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    while True:


        opcao = int(menu())

    # Deposito
        if opcao == 1:
            valor = float(input('Digite o valor do deposito: R$'))

            saldo, extrato = deposito(saldo, valor, extrato)
            print(saldo)
            
    # Saques
        elif opcao == 2:
            valor = float(input('Qual o valor a ser sacado: R$'))
            saldo, extrato = sacar(saldo=saldo, 
                        valor=valor, extrato=extrato, 
                        limite=limite, 
                        numero_saques=numeros_saques, 
                        limite_saques=LIMITE_SAQUES)
            numeros_saques += 1
            print(saldo)

    # Extrato
        elif opcao == 3:
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == 4:
            
            conta = criar_conta(AGENCIA, conta_id, usuarios)

            if conta:
                contas.append(conta)
                conta_id += 1
        
        elif opcao == 5:
            criar_usuario(usuarios)

        elif opcao == 6:
            break

        else:
            print('Ação Inválida! Digite novamente...')

main()