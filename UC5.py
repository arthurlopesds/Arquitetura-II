"""
1-  Mudei o busca memoria, no indice do retorno, coloquei o indice-1 pra retornar realmente o valor que agt quer
2 - Mudei algumas paradas nas funções de separar instrução, na verificação dos parametros
3 - Criei o Escreve_Memoria e no final da execução da programa ele altera la no arquivo o que foi mudado no decorrer
do programa.
4 - Tratei o MOV, ADD (de acordo com o que agt vai precisar no fibonacci), e comecei o CMP pra testar
5 - Coloquei uma verificação la no Busca_Instrucao, porque tava dando erro quando eu colocava um codigo de 1,2 linhas,
dava erro,falando que tentando acessar uma posição que não existia.
6- coloquei umas flags pra add e cmp, porque a tratada de cada 1 é diferente, tipo, o primeiro parametro do ADD, se for
um reg no 1º parametro tem que saber o valor dele e ainda armazenar nele depois, eu coloquei no array a regra pra ADD:
['onde salvar a soma','operando1','operando2'].Pra cmp, o 1º parametro eu só tenho que saber qual o valor, se for reg
tbm no caso, a regra pra ele ficou só ['valor1','valor2'], porque o resultado não precisa salvar em lugar nenhum, ta
lgdo? Num sei se eu fiz certo kk, tu vê aí, mas foi assim que veio na cabeça na hora. O mov não precisa saber qual o
valor do primeiro parametro, aí ficou só : ['onde salvar', 'quem salvar'].
7- coloquei aqueles prints no CMP só pra teste, pra gnt ter a ideia do JG, JE ... e tal
8 - Testei com um arquivo que eu ia fazendo na hora pra testar, e uma memoria que eu fiz na hora também.Mas era tipo
partes do codigo de fibonacci. Tentei focar mais no que agt precisava no fibonacci. Depois que agt fizer isso, vamo
passar pra fazer mais coisas pra outros codigos.
9 - Se eu deixei de falar alguma coisa q eu mudei foi porque eu esqueci, mas quando tu for executando um codigo na mão
tu vai se ligando nas mudanças.
10- Se tu quiser testar usando os arquivos que eu tava fazendo e testando é o "assembly.txt" e o "memoria.txt"

"""

with open("assembly.txt", "r") as arquivo:
    codigo = arquivo.readlines()

with open("memoria.txt", "r") as arquivo_memoria:
    mem = arquivo_memoria.readlines()
add=0
cmp=0
ir = 0
pc = ir + 1
ciclos = 0
opcao = 0
parametros = []
reg = []


def Escreve_Memoria(indice,dado):
    mem[indice-1] = dado

def Busca_Memoria(indice):
    return mem[indice-1]

def Pega_Segundo_Parametro(arg):
    if arg.isalpha():
        if arg == 'EAX':
            parametros.append(EAX)

    elif arg[0] == '[':
        MAR = arg.split('[')
        MAR = MAR[1].split(']')
        MAR = int(MAR[0])
        MBR = Busca_Memoria(MAR)
        parametros.append(MBR)
    else:
        parametros.append(arg)


def Separa_Instrucao(arg):
    global add,cmp
    if arg[0][0].isalpha():  # verifica se a primeira posição eh uma letra
        if add == 1:
            if arg[0] == 'EAX':
                parametros.append(arg[0])
                parametros.append(EAX)
                add = 0
        elif cmp == 1:
            if arg[0] == 'EAX':
                parametros.append(EAX)
                cmp = 0
        else:
            parametros.append(arg[0])

        if len(arg) == 2:
            Pega_Segundo_Parametro(arg[1])


    elif arg[0][0] == '[':  # verifica se a primeira posição eh um colchete

        # tira os colchetes do parâmetro
        MAR = arg[0].split('[')
        MAR = MAR[1].split(']')
        MAR = int(MAR[0])
        parametros.append(MAR)

        if len(arg) == 2:
            Pega_Segundo_Parametro(arg[1])

    else:
        print('Erro de sintaxe!')


def Busca_Instrucao(reginstrucao):
    global ciclos
    tam = len(codigo)
    if reginstrucao>tam-1:
        return 'END'
    inst = codigo[reginstrucao]
    inst = inst.split()
    ciclos += 1
    return inst


def Decodifica_Instrucao(instrucao):
    global pc, x, ir, ciclos, opcao, prontapraexec,add,cmp

    if instrucao[0] == 'MOV':
        argumentos = instrucao[1].split(',')
        Separa_Instrucao(argumentos)
        opcao = 1
        prontapraexec = 1


    elif instrucao[0] == 'ADD':
        argumentos = instrucao[1].split(',')
        add = 1
        Separa_Instrucao(argumentos)

        opcao = 2
        prontapraexec = 1

    elif instrucao[0] == 'INC':

        Separa_Instrucao(instrucao[1])
        opcao = 3

    elif instrucao[0] == 'CMP':
        argumentos = instrucao[1].split(',')
        cmp = 1
        Separa_Instrucao(argumentos)
        opcao = 4
        prontapraexec = 1

    elif instrucao[0] == 'JE':

        Separa_Instrucao(instrucao[1])
        opcao = 5

    elif instrucao[0] == 'JL':

        Separa_Instrucao(instrucao[1])
        opcao = 6

    elif instrucao[0] == 'JG':

        Separa_Instrucao(instrucao[1])
        opcao = 7

    elif instrucao[0] == 'MUL':
        argumentos = instrucao[1].split(',')

        Separa_Instrucao(argumentos)
        opcao = 8

    elif instrucao[0] == 'DIV':
        argumentos = instrucao[1].split(',')

        Separa_Instrucao(argumentos)
        opcao = 9


    else:
        x = 1
    ir = pc
    pc += 1
    return prontapraexec


def Executa_Instrucao():
    global EAX, prontapraexec, ula, acc, opcao, ciclos,pexec

    if opcao == 1:
        if parametros[0] == 'EAX':
            EAX = int(parametros[1])
            print('EAX = ',EAX)
        else:
            Escreve_Memoria(parametros[0],str(parametros[1])+'\n')
        prontapraexec=0
        pexec = 0

    elif opcao == 2:
        if parametros[0] == 'EAX':
            ula = int(parametros[1]) + int(parametros[2])
            acc = ula
            EAX = acc

        prontapraexec = 0
        pexec = 0
        ciclos += 1
        print('EAX = ',EAX)

    elif opcao == 4:
        resultado = int(parametros[0]) - int(parametros[1])
        if resultado > 1:
            print('O {} eh maior do que {} '.format(parametros[0], parametros[1]))
        elif resultado < 1:
            print('O {} eh menor do que {} '.format(parametros[0], parametros[1]))
        else:
            print('São Iguais')
        prontapraexec = 0
        pexec = 0


    # Para apagar os parâmetros da instruções que foi executada
    parametros.clear()

x = 0
while x != 1:
    instruction = Busca_Instrucao(ir)
    pexec = Decodifica_Instrucao(instruction)

    if pexec == 1:
        Executa_Instrucao()

with open("memoria.txt","w") as arquivo_memoria:
    for i in range(len(mem)):
        arquivo_memoria.write(str(mem[i]))


print('\nA instrução levou {} Ciclos de Clock '.format(ciclos))