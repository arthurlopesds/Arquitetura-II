with open("fib.txt", "r") as arquivo:
    codigo = arquivo.readlines()

with open("mem.txt", "r") as arquivo_memoria:
    mem = arquivo_memoria.readlines()
add=0
cmp=0
jg=0
inc=0
printa=0
ir = 0
pc = ir + 1
ciclos = 0
opcao = 0
parametros = []
reg = []
pjumpInst = []
pjumpIR = []


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
    global add,cmp,jg,inc,printa
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
        elif jg == 1:
            parametros.append(arg+':')
            jg=0

        else:
            parametros.append(arg[0])

        if len(arg) == 2:
            Pega_Segundo_Parametro(arg[1])


    elif arg[0][0] == '[':  # verifica se a primeira posição eh um colchete

        if printa == 1:
            MAR = arg[0].split('[')
            MAR = MAR[1].split(']')
            MAR = int(MAR[0])
            parametros.append(Busca_Memoria(MAR))
            printa = 0

        elif inc == 1:
            MAR = arg.split('[')
            MAR = MAR[1].split(']')
            MAR = int(MAR[0])
            parametros.append(MAR)
            parametros.append(Busca_Memoria(MAR))
            inc = 0
        else:
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
    global pc, x, ir, ciclos, opcao, prontapraexec,add,cmp,jg,inc,printa

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
        inc = 1
        Separa_Instrucao(instrucao[1])
        opcao = 3
        prontapraexec = 1

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
        prontapraexec = 1

    elif instrucao[0] == 'MUL':
        argumentos = instrucao[1].split(',')

        Separa_Instrucao(argumentos)
        opcao = 8

    elif instrucao[0] == 'DIV':
        argumentos = instrucao[1].split(',')

        Separa_Instrucao(argumentos)
        opcao = 9

    elif instrucao[0][len(instrucao[0])-1] == ':':
        pjumpInst.append(instrucao[0])
        pjumpIR.append(ir)
        opcao = 10
        prontapraexec = 1

    elif instrucao[0] == 'PRINTF':
        printa = 1
        argumentos = instrucao[1].split(',')
        Separa_Instrucao(argumentos)
        opcao = 11
        prontapraexec=1

    else:
        x = 1

    ir = pc
    pc += 1

    return prontapraexec


def Executa_Instrucao():
    global EAX, prontapraexec, ula, acc, opcao, ciclos,pexec,ir,pc,resultado,jg

    if opcao == 1:
        if parametros[0] == 'EAX':
            EAX = int(parametros[1])
            #print('EAX = ',EAX)
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
        #print('EAX = ',EAX)

    elif opcao == 3:
        valor = int(parametros[1])
        valor +=1
        Escreve_Memoria(parametros[0],str(valor)+'\n')
        prontapraexec = 0
        pexec=0

    elif opcao == 4:
        resultado = int(parametros[0]) - int(parametros[1])
        #print('RESULTADO = {} '.format(resultado))
        if resultado > 0:
            jg=1
        else:
            jg=0
        prontapraexec = 0
        pexec = 0

    elif opcao == 7:
        for i in range(len(pjumpInst)):
            if pjumpInst[i] == parametros[0]:
                ir = pjumpIR[i]
                pc = ir + 1
        prontapraexec = 0
        pexec = 0

    elif opcao == 10:
        ir = ir
        pc = pc
        prontapraexec = 0
        pexec = 0

    elif opcao == 11:
        for i in range(len(parametros)):
            print('{} '.format(parametros[i]))

        prontapraexec=0
        pexec=0



    # Para apagar os parâmetros da instruções que foi executada
    parametros.clear()

x = 0
while x != 1:
    instruction = Busca_Instrucao(ir)
    pexec = Decodifica_Instrucao(instruction)

    if pexec == 1:
        Executa_Instrucao()

with open("mem.txt","w") as arquivo_memoria:
    for i in range(len(mem)):
        arquivo_memoria.write(str(mem[i]))


print('\nA instrução levou {} Ciclos de Clock '.format(ciclos))