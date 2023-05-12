import Alg2.Trie as Trie
import math

# Classe para compressão e descompressão dos dados.

# Recebe a string de bits do arquivo de texto e comprime:


def encoding(word: str):
    # Inicializa uma Trie como dicionário e lista com códigos
    dictionary = Trie.BinaryTrie()
    code = []
    wordLenght = len(word)

    # Inicializa o prefixo P
    prefix = ''

    # inicialia a contagem de prefixos:
    prefixCounter = 1

    # Para cada símbolo na palavra:
    for i in range(wordLenght):
        # c é o símbolo analizado
        observedSymbol = word[i]

        # Vemos se P+c está na Trie
        localPrefixPlusChar = dictionary.searchString(prefix + observedSymbol)

        # Se ele está na trie, então definimos P=P+c, e guardamos a posição dele na Trie
        if localPrefixPlusChar >= 0:
            prefix = prefix + observedSymbol
            localPrefixInDictionary = localPrefixPlusChar

        # Se ele não está na Trie, inserimos P+c nela e salvamos uma tupla (local de P na trie, c) na compressão
        # Resetamos P para string vazia
        else:
            dictionary.insertString(prefix + observedSymbol, prefixCounter)
            prefixCounter += 1
            if len(prefix) == 0:
                codeword = 0
            else:
                codeword = localPrefixInDictionary
            code.append((codeword, observedSymbol))
            prefix = ''

    # Se lemos o texto todo mas P não está vazia, adicionamos tupla (local de P na trie, '')
    if (len(prefix) != 0):
        code.append((localPrefixInDictionary, ''))

    # Converte código para binário.
    code = codeToBool(code, prefixCounter)
    return code


# Recebe um código em binário e descomprime para texto


def decoding(code):
    # Pega a sequência binária e transforma na lista de tuplas com código:
    code = boolToCode(code)

    # Incializa um dicionário de prefixos
    dictionary = []

    # Incializa o texto descomprimido:
    originalString = ''
    tempCode = ''

    # Para cada tupla do código:
    for item in code:

        # Pega uma tupla e seu conteúdo
        codeword = item[0]
        symbol = item[1]

        # Segura o conteúdo que a tupla descodificou
        tempCode = ''

        # Se o código for 0 (palavra vazia) adiciona o simbolo no texto original,
        if codeword == 0:
            originalString += symbol
            tempCode += symbol

        # Se não for 0, pega o número do prefixo no dicionario, e adiciona no texto junto com o simbolo da tupla
        else:
            tempCode += dictionary[codeword-1] + symbol
            originalString += tempCode

        # Bota o conteúdo descodificado pela tupla no dicionário
        dictionary.append(tempCode)
        tempCode = ''

    # Converte a string descodificada de binário para texto
    originalString = binToText(originalString)
    return originalString


# Converte uma sequência em binário para Texto Humano


def binToText(binaryString: str):

    # Incializa array de Bytes
    bytesData = bytearray()

    # Transforma cada 8 bits em byte e coloca no array
    for i in range(0, len(binaryString), 8):
        byte = binaryString[i:i+8]
        bytesData.append(int(byte, 2))

    # Converte os bytes para texto humano
    humanText = bytes(bytesData).decode('utf-8')
    return humanText

# Converte a lista de tuplas do código LZ para uma string de binário


def codeToBool(code: list, numberOfPrefixes: int):

    # Definimos o número mínimo de bits necessário para representar a quantidade de prefixos:
    numberBits = math.ceil(math.log2(numberOfPrefixes))

    # Guardamos em 5 bits o número de bits utilizado para codificar o número de prefixos, no início do código
    # Ou seja, podemos guardar valores de 0 até 31, e utilizar essa quantidade de bits para cada inteiro
    # Logo, podemos representar até 2^31 prefixos com esse número de bits
    numberBitsString = '0' + str(numberBits) + 'b'
    codeString = format(numberBits, '05b')

    # Transformamos o número do prefixo na representação de bits e adicionamos no código
    for item in code:
        binRepresentation = format(item[0], numberBitsString)
        codeString += binRepresentation + item[1]

    # Certificamos de que a sequência é um múltiplo de 8, para poder converter para bytes depois
    # Se não for, completamos com uma sequência de 1s necessária.
    # Salvamos em 3 bits o número de bits adicionado para completar (Já que x mod 8 tem valores de 0 a 7)
    missingBits = (8 - (len(codeString) + 3) % 8) % 8
    codeString += '1' * missingBits + format(missingBits, '03b')

    return codeString

# Desconverte uma sequência binária comprimida para Lista de tuplas de código LZ


def boolToCode(code: str):
    # Pega os 5 primeiros dígitos para descobrir o nº de bits usados
    numberOfBits = int(code[:5], 2)

    # Descarta a parte da sequência que conta o número de bits usados e o que foi completado na string
    trashSize = int(code[-3:], 2)
    code = code[5: -(trashSize + 3)]

    codeConverted = []

    # Se o código tem número impar, é pq a última tupla tem a string vazia como simbolo.
    if (len(code) % 2) == 1:
        iteratorString = len(code) + 1
    else:
        iteratorString = len(code)

    # Pega cada sequência de bits correspondete a uma tupla e converte:
    for i in range(0, iteratorString, numberOfBits + 1):

        # Pega número do prefixo
        codeWord = int(code[i: (i + numberOfBits)], 2)

        # Pega o simbolo da tupla. Se for a última interação temos que certificar se é 0, 1, ou ''.
        if (i == (iteratorString - (numberOfBits + 1)) and (len(code) % 2)) == 1:
            symbol = ''
        else:
            symbol = code[i + numberOfBits]

        # Coloca no código
        codeConverted.append((codeWord, symbol))

    return codeConverted
