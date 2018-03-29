with open("assembly.txt","r") as arquivo:
    codigo = arquivo.readlines()


ir = 0
pc = ir + 1
ciclos = 0
mov=0
add=0
fazer = []
def Busca_Instrucao (reginstrucao):
        global ciclos
        inst = codigo[reginstrucao]
        inst = inst.split()
        ciclos+=1
        return inst

def Decodifica_Instrucao(instrucao):
    global pc,x,ir,ciclos,mov,prontapraexec,add,oper1,oper2,add

    if instrucao[0] == 'MOV':
        quebrainst = instrucao[1].split(',')
        fazer.append(quebrainst[0])
        MAR = int(quebrainst[1])
        for i in range(len(codigo)+1):
            if(MAR ==  i):
                MBR = codigo[i-1]
                fazer.append(MBR)
        mov = 1
        prontapraexec = 1
        ciclos+=1
    elif instrucao[0] == 'ADD':
        quebrainst = instrucao[1].split(',')
        MAR = int(quebrainst[0])
        MAR1 = int(quebrainst[0]) #buffer para poder salvar o valor inicial de MAR
        for i in range(len(codigo)+1):
            if MAR == i:
                oper1 = int(codigo[i - 1])#ula no lugar de oper1
                #oper1 = ula
        MAR = int(quebrainst[1])
        for i in range(len(codigo)+1):
             if MAR == i:
                oper2 = int(codigo[i - 1])
      #          ula += oper2

       # acc = ula
        #print("""
         #          \nINSTRUÇÃO ADD:
          #             MAR(REGISTRADOR DE ENDEREÇO DE MEMORIA) = do 1º operando: {} | do 2º operando: {}
           #            ULA(UNIDADE LOGICA ARITMETICA) = {} + {}
            #           ACC (REGISTRADOR QUE ARMAZENA DADOS DA OPERAÇÃO DA ULA) = {}
           #""".format(MAR1, MAR, oper1,oper2, acc))
        add=1
        prontapraexec=1
        ciclos += 1

    else:
        x=1
    ir = pc
    pc += 1

def Executa_Instrucao():
    global AL,prontapraexec,ula,acc
    if mov == 1:
        if fazer[0] == 'AL':
             AL = fazer[1]
        print('AL = {}'.format(AL))
        prontapraexec = 0

    if add == 1:
        ula = oper1+oper2
        print('Valor da Soma = {}'.format(ula))
        acc=ula
        prontapraexec = 0


x = 0
while x != 1:
    instruction = Busca_Instrucao(ir)
    Decodifica_Instrucao(instruction)
    if prontapraexec == 1:
        Executa_Instrucao()


print('\nA instrução levou {} Ciclos de Clock '.format(ciclos))
