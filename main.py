menu = '''
[1] Deposito
[2] Saque
[3] Extrato
[4] Sair

=>'''

saldo = 0
limite = 500
extrato = ''
numeros_saques = 0
LIMITE_SAQUES = 3

while True:

    print(menu)
    opcao = int(input('Digite a ação que deseja: '))

    if opcao == 1:
        valor = float(input('Digite o valor do deposito: R$'))

        if valor > 0:
            saldo += valor
            extrato += f'Depósito: R${valor:.2f}\n'
        
        else:
            print('O valor inserido está inválido')

    elif opcao == 2:
        valor = float(input('Qual o valor a ser sacado: R$'))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saque = numeros_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print('O valor insérido é maior que o saldo atual!')
        elif excedeu_limite:
            print('O valor inserido é maior que o seu limite!')
        elif excedeu_saque:
            print('Você já atingiu seu limite de saques diários!')

        elif valor > 0:
            saldo -= valor
            extrato += f'Saque: R${valor:.2f}\n'
        else:
            print('O valor digitado é inválido')
    
    elif opcao == 3:
        print('\n-------------------Extrato-------------------')
        print('Não foram realizadas movimentações.' if not extrato else extrato)
        print(f'\nSaldo: R${saldo:.2f}')
        print('-----------------------------------------------')

    elif opcao == 4:
        break

    else:
        print('Ação Inválida! Digite novamente...')