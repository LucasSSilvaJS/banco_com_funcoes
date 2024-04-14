import os

#variaveis de usuario e conta
AGENCIA = '0001'
usuarios = []
contas = []
numero_da_conta = 0

login_conta = {}

#funções para refatorar

def limpar_console():
    os.system('cls')

def enter_para_continuar():
    print()
    input('Digite enter para continuar: ')
    limpar_console()

def verificar_usuario(cpf):
    global usuarios
    usuario_cadastrado = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuario_cadastrado[0] if usuario_cadastrado else None

def verificar_conta(agencia, numero_da_conta):
    global contas
    conta_cadastrada = [conta_ for conta_ in contas if conta_['agencia'] == agencia and conta_['numero_da_conta'] == numero_da_conta]
    return conta_cadastrada[0] if conta_cadastrada else None

def logado(login_conta):
    return True if login_conta else False

def deslogar():
    global login_conta
    login_conta = {}
    print('Conta desconectada')
    enter_para_continuar()
    
#login

def fazer_login():
    global contas
    global login_conta

    print('Tela de login\n')

    agencia = input('Digite o numero de sua agência: ')
    numero_da_conta = int(input('Digite o numero de sua conta: '))

    limpar_console()
    
    if not(agencia and numero_da_conta):
        print('É preciso informar sua agencia e conta para realizar o login')
        enter_para_continuar()
        return
    
    if verificar_conta(agencia, numero_da_conta):
        print('Login efetuado')
        login_conta = verificar_conta(agencia, numero_da_conta)
        enter_para_continuar()
    else:
        print('Conta não encontrada')
        enter_para_continuar()

#funções para conta e usuario
def criar_usario(nome, data_de_nascimento, cpf, endereco):
    global usuarios

    if verificar_usuario(cpf):
        print('Usuário já cadastrado')
        return

    novo_usuario = {
        'nome': nome, 
        'data_de_nascimento': data_de_nascimento, 
        'cpf': cpf,
        'endereco': endereco
    }

    usuarios.append(novo_usuario)

def solicitar_dados_de_usuario():
    print('Cadastro de usuario\n')

    nome = input('Digite seu nome completo: ')
    data_de_nascimento = input('Digite sua data de nascimento (dd-mm-aaaa): ')
    cpf = input('Digite seu cpf: ')

    logradouro = input('Digite seu logradouro: ')
    bairro = input('Digite seu bairro: ')
    cidade = input('Digite sua cidade: ')
    sigla_do_estado = input('Digite a sigla do seu estado: ')

    endereco = f'{logradouro} - {bairro} - {cidade}/{sigla_do_estado}'

    limpar_console()

    if not(nome and data_de_nascimento and cpf and logradouro and bairro and cidade and sigla_do_estado):
        print('É preciso informar todos os dados')
        enter_para_continuar()
        return

    criar_usario(
        nome,
        data_de_nascimento,
        cpf,
        endereco
    )

    print('Usuario cadastrado com sucesso!')

    enter_para_continuar()

def criar_conta(agencia, usuario):
    global contas
    global numero_da_conta
    
    numero_da_conta += 1

    nova_conta = {
        'agencia': agencia,
        'numero_da_conta': numero_da_conta,
        'usuario': usuario,
        'saldo': 0.00,
        'quantidade_de_saque_diario': 0,
        'extrato': ''
    }

    contas.append(nova_conta)

    print(f'Agencia: {agencia}')
    print(f'Numero da conta: {numero_da_conta}')

def solicitar_dados_de_conta():
    global AGENCIA
    global usuarios

    print('Cadastro de conta\n')
    
    cpf = input('Digite seu cpf: ')

    limpar_console()

    if not cpf:
        print('É preciso informar o cpf')
        enter_para_continuar()
        return

    if verificar_usuario(cpf):
        usuario = verificar_usuario(cpf)
        criar_conta(AGENCIA, usuario)
        print('Conta cadastrada com sucesso!\n')
        
        enter_para_continuar()
    else:
        print('Erro! É necessário possuir um cadastro de usuário')

        enter_para_continuar()

#variaveis de aplicações bancarias
saldo = 0.00
quantidade_de_saque_diario = 0
extrato = ''
VALOR_LIMITE_DE_SAQUE = 500.00
LIMITE_DE_QUANTIDADE_DE_SAQUE = 3
    
def saque(valor, login_conta):
    if valor > 0:
        if login_conta['saldo'] >= valor:
            if valor <= VALOR_LIMITE_DE_SAQUE and login_conta['quantidade_de_saque_diario'] < LIMITE_DE_QUANTIDADE_DE_SAQUE:
                login_conta['saldo'] -= valor
                login_conta['quantidade_de_saque_diario'] += 1
                print(f'Você realizou um saque de R$ {valor:.2f}')
                print()
                login_conta['extrato'] += f'Saque realizado no valor de R$ {valor:.2f}\n'
            else:
                if login_conta['quantidade_de_saque_diario'] >= LIMITE_DE_QUANTIDADE_DE_SAQUE:
                    print('Quantidade de saque diário passou do limite')
                    print()
                if valor > VALOR_LIMITE_DE_SAQUE:
                    print('O saque ultrapassou o limite máximo de R$ 500')
                    print()
        else:
            print('Não será possível sacar o dinheiro por falta de saldo')
            print()
    else:
        print('Operação falhou! O valor informado é inválido.')
        print()

def deposito(valor, login_conta):
    if valor > 0:
        login_conta['saldo'] = login_conta['saldo'] +  valor
        print(f'Você realizou um deposito de R$ {valor:.2f}')
        print()
        login_conta['extrato'] += f'Depósito realizado no valor de R$ {valor:.2f}\n'
    else:
        print('Operação falhou! O valor informado é inválido.')
        print()

def imprimir_extrato(login_conta):
    if login_conta['extrato']:
        login_conta['extrato'] += f'Saldo total: R$ {login_conta['saldo']:.2f}\n'
        print(login_conta['extrato'])
        login_conta['extrato'] = login_conta['extrato'].replace(f'Saldo total: R$ {login_conta['saldo']:.2f}\n', '')
        enter_para_continuar()
    else:
        print('Você não possui movimentações em sua conta')
        enter_para_continuar()

def solicitar_saque(login_conta):
    limpar_console()
    valor = float(input('Digite um valor para saque: '))
    limpar_console()
    saque(valor, login_conta)
    enter_para_continuar()

def solicitar_deposito(login_conta):
    limpar_console()
    valor = float(input('Digite um valor para deposito: '))
    limpar_console()
    deposito(valor, login_conta)
    enter_para_continuar()

def mensagem_menu():
    menu = '''
        Seja bem-vindo ao nosso banco!        

        [l] Login
        [o] Deslogar
        [u] Cadastrar usuario
        [c] Criar conta
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair
        
        Selecione uma opcao: '''
    return menu

def main():
    menu = mensagem_menu()
    while True:
        opcao = input(menu).lower()
        if opcao == 'd':
            limpar_console()
            if not logado(login_conta):
                print('É preciso estar logado para efetuar essa operação')
                enter_para_continuar()
                continue
            solicitar_deposito(login_conta)
        elif opcao == 'l':
            limpar_console()
            fazer_login()
        elif opcao == 'o':
            limpar_console()
            deslogar()
        elif opcao == 'u':
            limpar_console()
            solicitar_dados_de_usuario()
        elif opcao == 'c':
            limpar_console()
            solicitar_dados_de_conta()
        elif opcao == 's':
            limpar_console()
            if not logado(login_conta):
                print('É preciso estar logado para efetuar essa operação')
                enter_para_continuar()
                continue
            solicitar_saque(login_conta)
        elif opcao == 'e':
            limpar_console()
            if not logado(login_conta):
                print('É preciso estar logado para efetuar essa operação')
                enter_para_continuar()
                continue
            limpar_console()
            imprimir_extrato(login_conta)
        elif opcao == 'q':
            limpar_console()
            print('Obrigado pela preferência! Volte sempre :)')
            print()
            enter_para_continuar()
            break
        else:
            limpar_console()
            print('Operação inválida! Por favor, selecione novamente a operação desejada.')
            print()
            enter_para_continuar()

main()