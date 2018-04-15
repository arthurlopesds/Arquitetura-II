"""
1 - Comentei mais um pouco, falta mais um pouco da parte da execução, o resto é praticamente repetição
"""

with open("fatorial.txt", "r") as arquivo: #leitura do arquivo que contem o codigo assembly
    codigo = arquivo.readlines() #readlines coloca cada linha do codigo em um indice do array codigo

with open("memfat.txt", "r") as arquivo_memoria: #leitura do arquivo de memoria que contem os valores que serão usados
                                                 #usados na execução, ou necessario tambem para alguma modificação
    mem = arquivo_memoria.readlines()
add=0
cmp=0
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

def Zera_Registrador():
    for i in range(5):
        reg.append(0)
def Escreve_Memoria(indice,dado):
    mem[indice-1] = dado #indice-1 pois ja que é um array começa do 0
def Busca_Memoria(indice):
    return mem[indice-1]
def Pega_Segundo_Parametro(arg):
    if arg[0].isalpha(): #se for uma letra(registradores)
        parametros.append(reg[int(arg[1])-1])

    elif arg[0] == '[': #endereço de memoria
        MAR = arg.split('[')
        MAR = MAR[1].split(']')
        MAR = int(MAR[0])
        MBR = Busca_Memoria(MAR)
        parametros.append(MBR)

    else: #constante
        parametros.append(arg)
def Separa_Instrucao(arg, jump):
    global add,cmp,inc,printa
    parametros.clear()# Para apagar os parâmetros da instruções que foi executada

    if arg[0][0].isalpha():  # verifica se a primeira posição eh uma letra

        #Flag do jump porque quando passava o parâmetro "arg[0]" pegava apenas a primeira letra
        if jump == 1:
            parametros.append(arg)

        else:
            parametros.append(arg[0])

        #verifica se o instrução tem 2 parametros
        if len(arg) == 2:
            Pega_Segundo_Parametro(arg[1])


    elif arg[0][0] == '[':  # verifica se a primeira posição eh um colchete

        if printa == 1: # pego o valor que vai ser printado correspondente ao endereço de memoria
            MAR = arg[0].split('[')
            MAR = MAR[1].split(']')
            MAR = int(MAR[0])
            parametros.append(Busca_Memoria(MAR))
            printa = 0 #"desligo printa"

        elif inc == 1: #pego o endereço que eu vou buscar o valor(ja que vai ter que ser substituido na memoria)
                       #e pego o valor que eu vou incrementar
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
    if reginstrucao>tam-1: #se caso o ir for maior do que o tamanho do codigo(quantidade das intruções), encerra.
                           # o -1 é porque é um array
       return 'END'
    inst = codigo[reginstrucao]
    inst = inst.split() #"quebra" o nome da instrução e os seus parametros, cada 1 em 1 indice(nome da instrução em 1,
                        #e seus parametros em outro indice).
    ciclos += 1
    return inst
def Decodifica_Instrucao(instrucao):
    global pc, x, ir, ciclos, opcao, prontapraexec,add,cmp,inc,printa

    if instrucao[0] == 'MOV':
        argumentos = instrucao[1].split(',')  #"quebra" os parametros da instrução para tratar cada 1
        Separa_Instrucao(argumentos, 0)
        opcao = 1
        prontapraexec = 1


    elif instrucao[0] == 'ADD':
        argumentos = instrucao[1].split(',')
        add = 1
        Separa_Instrucao(argumentos, 0)

        opcao = 2
        prontapraexec = 1

    elif instrucao[0] == 'INC':
        inc = 1
        Separa_Instrucao(instrucao[1], 0)
        opcao = 3
        prontapraexec = 1

    elif instrucao[0] == 'CMP':
        argumentos = instrucao[1].split(',')
        cmp = 1
        Separa_Instrucao(argumentos, 0)
        opcao = 4
        prontapraexec = 1

    elif instrucao[0] == 'JE':

        Separa_Instrucao(instrucao[1], 1)
        opcao = 5
        prontapraexec = 1

    elif instrucao[0] == 'JL':
        Separa_Instrucao(instrucao[1], 1)
        opcao = 6
        prontapraexec = 1

    elif instrucao[0] == 'JG':
        Separa_Instrucao(instrucao[1], 1)
        opcao = 7
        prontapraexec = 1

    elif instrucao[0] == 'MUL':
        argumentos = instrucao[1].split(',')

        Separa_Instrucao(argumentos, 0)
        opcao = 8
        prontapraexec = 1

    elif instrucao[0] == 'DIV':
        argumentos = instrucao[1].split(',')

        Separa_Instrucao(argumentos, 0)
        opcao = 9
        prontapraexec = 1

    elif instrucao[0][len(instrucao[0])-1] == ':': #se o final da instrução tiver ':' é um label
        pjumpInst.append(instrucao[0]) #pego o nome do label (que vai servir pra verificar com o JG
        pjumpIR.append(ir) #e pego o valor do IR pra saber em que lugar ele ta, acho que dava pra pegar a posicao do arquivo
                           #tambem, mas assim fica até mais facil
        opcao = 10
        prontapraexec = 1

    elif instrucao[0] == 'PRINTF':
        printa = 1
        argumentos = instrucao[1].split(',')
        Separa_Instrucao(argumentos, 0)
        opcao = 11
        prontapraexec=1

    elif instrucao[0] == 'DEC':
        inc = 1
        Separa_Instrucao(instrucao[1], 0)
        opcao = 12
        prontapraexec = 1


    else:
        x = 1

    ir = pc #IR recebe a proxima instrução
    pc += 1

    return prontapraexec #retorno para saber se a instrução esta pronta pra execução ou não

def Executa_Instrucao():
    global EAX, prontapraexec, ula, acc, opcao, ciclos,pexec,ir,pc,resultado


    #executa o MOV
    if opcao == 1:

        if type(parametros[0]) != int: #se for diferente do tipo Inteiro
            reg[int(parametros[0][1])-1] = int(parametros[1]) #o determinado valor é movido para o determinado registrador
        else:
            Escreve_Memoria(int(parametros[0]), str(parametros[1])) #se nao for, escreve o valor no determinado endereço

        prontapraexec=0 #instrução acabou
        pexec = 0

    # executa o ADD
    elif opcao == 2:
        if type(parametros[0]) != int:
            ula = reg[int(parametros[0][1])-1] + int(parametros[1])
            acc = ula
            reg[int(parametros[0][1]) - 1] = acc

        prontapraexec = 0
        pexec = 0
        ciclos += 1

    # executa o INC
    elif opcao == 3:
        valor = int(parametros[1]) #pego o valor
        valor +=1 #incremento
        Escreve_Memoria(parametros[0],str(valor)+'\n') #o primeiro parametro é onde eu vou escrever, o segundo é o valor
                                                       # com o \n pra pular linha e nao ficar numeros juntos num mesmo
                                                       #indice
        prontapraexec = 0
        pexec=0

    # executa o CMP
    elif opcao == 4:
        if type(parametros[0]) != int:

            resultado = int(reg[int(parametros[0][1])-1]) - int(parametros[1])  # diminui o primeiro parametro com o segundo
        else:
            resultado = Busca_Memoria(reg[int(parametros[0])-1]) - int(parametros[1])

        prontapraexec = 0
        pexec = 0

    #executa o JE
    elif opcao == 5:

        if resultado == 0:
            for i in range(len(pjumpInst)): #do tamanho do array de labels
                if pjumpInst[i] == (parametros[0]+":"):  #comparando de acordo com os labels que tão no array
                    ir = pjumpIR[i] #fazendo o jmp
                    pc = ir + 1

    #executa o JL
    elif opcao == 6:

        if resultado < 0:
            for i in range(len(pjumpInst)): #do tamanho do array de labels
                if pjumpInst[i] == (parametros[0]+":"):  #comparando de acordo com os labels que tão no array
                    ir = pjumpIR[i] #fazendo o jmp
                    pc = ir + 1

    #executa o JG
    elif opcao == 7:

        if resultado > 0:
            for i in range(len(pjumpInst)): #do tamanho do array de labels
                if pjumpInst[i] == (parametros[0]+":"):  #comparando de acordo com os labels que tão no array
                    ir = pjumpIR[i] #fazendo o jmp
                    pc = ir + 1
        prontapraexec = 0
        pexec = 0

    # executa o MUL
    elif opcao == 8:

        #Verifica se o primeiro parâmetro da instrução é um registrador ou memória
        if type(parametros[0]) != int:
            reg[int(parametros[0][1])-1] = reg[int(parametros[0][1])-1] * int(parametros[1])

        else: #Busca na memoria o valor correspondente ao endereço
            mult = Busca_Memoria(int(parametros[0])) * int(parametros[1])
            Escreve_Memoria(int(parametros[0]), str(mult))

        prontapraexec=0
        pexec = 0

    # executa o DIV
    elif opcao == 9:
        # Verifica se o primeiro parâmetro da instrução é um registrador ou memória
        if type(parametros[0]) != int:
            reg[4] = reg[int(parametros[0][1]) - 1] % int(parametros[1]) #Registrador 5 fica salvo o resto da divisão
            reg[int(parametros[0][1]) - 1] = reg[int(parametros[0][1]) - 1] // int(parametros[1]) #Divisao de dois inteiros

        else:
            divisao = Busca_Memoria(int(parametros[0])) // int(parametros[1])
            Escreve_Memoria(int(parametros[0]), str(divisao))

        prontapraexec = 0
        pexec = 0

    # executa o LABEL
    elif opcao == 10:
        ir = ir #Continua o fluxo do codigo, ja que IR recebe o valor da proxima instrução no Decodifica
        pc = pc
        prontapraexec = 0
        pexec = 0

    # executa o PRINTF
    elif opcao == 11:
        for i in range(len(parametros)): #dependendo da quantidade de parametros no print
            print('{} '.format(parametros[i]))

        prontapraexec=0
        pexec=0

    # executa o DEC
    elif opcao == 12:
        valor = int(parametros[1])  # pego o valor
        valor -= 1  # incremento
        Escreve_Memoria(parametros[0], str(valor) + '\n')

        prontapraexec = 0
        pexec = 0
x = 0
Zera_Registrador()
while x != 1:
    instruction = Busca_Instrucao(ir) #buscando a instrução e retornando a linha da instrução para instruction
    pexec = Decodifica_Instrucao(instruction)  #retorna o valor 1 ou 0 para saber está tudo pronta pra execução ou nao,
                                               #respectivamente
    if pexec == 1:
        Executa_Instrucao()

with open("mem.txt","w") as arquivo_memoria: #depois da execução o que foi alterado na memoria, agora é escrito
    for i in range(len(mem)): #até o tamanho da memoria
        arquivo_memoria.write(str(mem[i])) #reescrevendo na memoria, o que foi alterado é sobreescrit
print('\nA instrução levou {} Ciclos de Clock '.format(ciclos)) #Print para a quantidade de ciclos que foi necessário para
                                                                #executar o codigo