with open("assembly.txt","r") as arquivo:
    codigo = arquivo.readlines()


ir = 0
pc = ir + 1
def Busca_Instrucao (reginstrucao):
        inst = codigo[reginstrucao]
        inst = inst.split()
        return inst

def Decodifica_Instrucao(instrucao):
    global pc
    global x
    global ir
    if instrucao[0] == 'MOV':
        quebrainst = instrucao[1].split(',')
        MAR = int(quebrainst[1])
        for i in range(len(codigo)+1):
            if(MAR ==  i):
                MBR = codigo[i-1]
        if quebrainst[0] == 'AL':
            AL = MBR
        print("""
                \nINSTRUÇÃO MOV:
                    MAR(REGISTRADOR DE ENDEREÇO DE MEMORIA) = {}
                    MBR(REGISTRADOR DE BLOCO DE MEMORIA) = {}
                    AL (REGISTRADOR) = {}
        """.format(MAR,MBR,AL))


    elif instrucao[0] == 'ADD':
        quebrainst = instrucao[1].split(',')
        MAR = int(quebrainst[0])
        MAR1 = int(quebrainst[0]) #buffer para poder salvar o valor inicial de MAR
        for i in range(len(codigo)+1):
            if MAR == i:
                ula = int(codigo[i - 1])
                oper1 = ula
        MAR = int(quebrainst[1])
        for i in range(len(codigo)+1):
            if MAR == i:
                oper2 = int(codigo[i - 1])
                ula += oper2

        acc = ula
        print("""
                   \nINSTRUÇÃO ADD:
                       MAR(REGISTRADOR DE ENDEREÇO DE MEMORIA) = do 1º operando: {} | do 2º operando: {}
                       ULA(UNIDADE LOGICA ARITMETICA) = {} + {}  
                       ACC (REGISTRADOR QUE ARMAZENA DADOS DA OPERAÇÃO DA ULA) = {}
           """.format(MAR1, MAR, oper1,oper2, acc))


    else:
        x=1
    ir = pc
    pc += 1

x=0
y=0
while x != 1:
    instruction = Busca_Instrucao(ir)
    Decodifica_Instrucao(instruction)
