"""
1 - Tirei umas variáveis de umas funções porque eu achei que não tava precisando usar elas
2 - Fiz a função pra pegar os parâmetros da instrução
3 - Troquei o nome de duas variáveis(fazer e quebrainst) para (parametros e argumentos)
4 - Adicionei as instruções INC e CMP no decodifica só usando a função Separa_Instrução
"""


with open("fib.txt","r") as arquivo:
    codigo = arquivo.readlines()

with open("mem.txt", "r") as arquivo_memoria:
    mem = arquivo_memoria.readlines()

ir = 0
pc = ir + 1
ciclos = 0
opcao = 0
parametros = []

def Busca_Memoria(indice):
    return mem[indice]

def Coloca_Memoria(indice):
    return mem[indice]

def Separa_Instrucao(arg):

    if arg[0][0].isalpha():  # verifica se a primeira posição eh uma letra
        parametros.append(arg[0])

    elif arg[0][0] == '[':  # verifica se a primeira posição eh um colchete

        # tira os colchetes do parâmetro
        MAR = arg[0][0].split('[')
        MAR = MAR[1].split(']')
        MAR = int(MAR[0])
        parametros.append(MAR)

    # Compara o segundo parâmetro da instrução
    elif arg[1][0].isalpha():
        parametros.append(arg[1])

    elif arg[1][0] == '[':
        MAR = arg[1][0].split('[')
        MAR = MAR[1].split(']')
        MAR = int(MAR[0])
        MBR = Busca_Memoria(MAR)
        parametros.append(MBR)

    elif arg[1][0].isnumeric():
        parametros.append(int(arg[1]))

    else:
        print('Erro de sintaxe!')


def Busca_Instrucao (reginstrucao):
        global ciclos
        inst = codigo[reginstrucao]
        inst = inst.split()
        ciclos+=1
        return inst

def Decodifica_Instrucao(instrucao):
    global pc, x, ir, ciclos, opcao, prontapraexec

    if instrucao[0] == 'MOV':
        argumentos = instrucao[1].split(',')

        Separa_Instrucao(argumentos)

        opcao = 1
        prontapraexec = 1


    elif instrucao[0] == 'ADD':
        argumentos = instrucao[1].split(',')

        Separa_Instrucao(argumentos)

        opcao = 2
        prontapraexec=1

    elif instrucao[0] == 'INC':

        Separa_Instrucao(instrucao[1])
        opcao = 3

    elif instrucao[0] == 'CMP':
        argumentos = instrucao[1].split(',')

        Separa_Instrucao(argumentos)
        opcao = 4


    else:
        x=1
    ir = pc
    pc += 1
    return prontapraexec


def Executa_Instrucao():
    global AL,prontapraexec,ula,acc,opcao,ciclos

    if opcao == 1:
        if parametros[0] == 'AL':
             AL = parametros[1]
        print('AL = {}'.format(AL))
        prontapraexec = 0
        mov = 0
        ciclos += 1

    if opcao == 2:
        #ula = oper1+oper2
        print('Valor da Soma = {}'.format(ula))
        acc=ula
        prontapraexec = 0
        add=0
        ciclos += 1

    #Para apagar os parâmetros da instruções que foi executada
    parametros.clear()

x = 0
while x != 1:
    instruction = Busca_Instrucao(ir)
    pexec = Decodifica_Instrucao(instruction)

    if pexec == 1:
        Executa_Instrucao()


print('\nA instrução levou {} Ciclos de Clock '.format(ciclos))
