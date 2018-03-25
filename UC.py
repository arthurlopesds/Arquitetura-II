"""
bicho, ta muito seboso kkkk, mas é só pra ver se agt consegue pensar melhor pra fazer o completo, ta lgdo?
foi a partir desse video: https://www.youtube.com/watch?v=69svptJTE9Y&t=122s
ele explica o funcionamento,eu fui vendo e fazendo, é muito simples esse código, mas eu acho que da pra ajudar na ideia.
Se tiver alguma coisa errada, tu vê, ou tu diz que agt vê.
"""
with open("assembly.txt","r") as arquivo:
    codigo = arquivo.readlines()

ula = 0
ir=0 #começo do arquivo (1ª instrução)
pc = ir + 1
x = True
print('IR = {}'.format(ir)) #print só pra saber se o valor ta certo mesmo
while x == True:
    instrucao = codigo[ir] #linhas do codigo em assembly, cada linha é um indice do array codigo
    instrucao = instrucao.split() #quebrando uma linha pelo espaço em branco(Ex: MOV R1,5 = instrução[0]='MOV' | instrução[1]='R1,5'
    if instrucao[0] == 'MOV': #se a primeira parte da instrução for MOV
        quebrainst = instrucao[1].split(',') #quebrando a segunda parte da instrução(o "lado direito") pela vírgula para saber qual o registrador armazenar e o valor do endereço
        MAR = int(quebrainst[1])  #Movendo o endereço para o registrador de endereço da Memoria e convertendo para inteiro
        for i in range(len(codigo)+1):#percorrer o arquivo para achar o valor no endereço , o range vai de 0 até 8
            if(MAR ==  i): #Buscando o valor correspondente ao valor do endereço do MAR da instrução
                MBR = codigo[i-1] #Depois que achou o resultado, o valor do endereço vai para o Registrador de Bloco de memoria
        if quebrainst[0] == 'AL': #dependendo de qual registrador o valor vai ser movido, o valor de MBR vai ser colocado nele
            AL = MBR
        print("""
                \nINSTRUÇÃO MOV:
                    MAR(REGISTRADOR DE ENDEREÇO DE MEMORIA) = {}
                    MBR(REGISTRADOR DE BLOCO DE MEMORIA) = {}
                    AL (REGISTRADOR) = {}
        """.format(MAR,MBR,AL))
        ir = pc #Registrador de Instruções recebendo o valor para a proxima instrução
        pc += 1 #PC apontando para a proxima instrução
        print('IR = {} e PC = {}'.format(ir, pc)) #print só pra saber se o valor ta certo mesmo

    elif instrucao[0] == 'ADD': #se a primeira parte da instrução for MOV
        quebrainst = instrucao[1].split(',') #quebrando a segunda parte da instrução(o "lado direito") pela vírgula para saber qual o registrador armazenar e o valor do endereço
        MAR = int(quebrainst[0]) #pegando a primeira parte de quebrainst, o endereço de onde está o operando
        MAR1 = int(quebrainst[0]) #só pra printar no fim o 1º valor de MAR
        for i in range(len(codigo)+1): #buscar o primeiro operando de acordo com o seu endereço, vai de 0 até 8
            if MAR == i:
                ula = int(codigo[i-1]) #armazenando na ula
                oper1 = ula
        MAR = int(quebrainst[1]) #pegando a segunda parte de quebrainst , no caso o endereço de onde está o outro operando
        for i in range(len(codigo)+1):  #buscar o segundo operando de acordo com o seu endereço
            if MAR == i:
                ula += int(codigo[i-1]) #depois que achou o outro operando, efetuou a Soma
                oper2 = int(codigo[i-1])
        acc = ula #armazenando o resultado no registrador ACC
        print("""
                \nINSTRUÇÃO ADD:
                    MAR(REGISTRADOR DE ENDEREÇO DE MEMORIA) = do 1º operando: {} | do 2º operando: {}
                    ULA(UNIDADE LOGICA ARITMETICA) = {} + {} 
                    ACC (REGISTRADOR QUE ARMAZENA DADOS DA OPERAÇÃO DA ULA) = {}
        """.format(MAR1,MAR,oper1,oper2,acc))
        ir = pc #Registrador de Instruções recebendo o valor para a proxima instrução
        pc += 1 #PC apontando para a proxima instrução
        print('IR = {} e PC = {}'.format(ir, pc)) #print só pra saber se o valor ta certo mesmo

    else: #condição de parada do while, se as instruções nao forem MOV nem ADD, entra no else
         x = False
