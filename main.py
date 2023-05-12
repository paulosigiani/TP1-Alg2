#!/usr/bin/env python
import argparse
import Compression

# Criando o objeto parser e adicionando os argumentos
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--compress', action='store_true',
                    help='Realiza a compressão do arquivo.')
parser.add_argument('-x', '--extract', action='store_true',
                    help='Realiza a descompressão do arquivo.')
parser.add_argument('input_file', type=str,
                    help='Caminho para o arquivo de entrada.')
parser.add_argument("-o", "--output_file",
                    help="Caminho para o arquivo de saída")

# Analisando a linha de comando
args = parser.parse_args()

# Acessando os valores dos argumentos
input_file = args.input_file
output_file = args.output_file

# Caso peça para Comprimir: (se a extensão de entrada é txt):
if args.compress:
    # Transformando para Binário
    with open(input_file, 'rb') as inFile:
        binary = inFile.read()
        inFile.close
        text = ''.join(format(byte, '08b') for byte in binary)
    # Comprimindo
    compressedFile = Compression.encoding(text)
    # Salvando a compressão em Arquivo:
    if output_file == None:
        output_file = input_file[:-3] + 'z78'
    with open(output_file, 'wb') as outFile:
        # Processo de Bit Packing
        num_bytes = len(compressedFile) // 8

        currentByte = 0
        bitPosition = 0

        # Itera sobre cada caractere do código comprimido:
        for char in compressedFile:
            # Converte o caracter para um inteiro (0 ou 1)
            bit = int(char)
            # Coloca o bit no byte
            currentByte = currentByte | (bit << (7 - bitPosition))

            # Incrementa a posição do bit no nyte
            bitPosition += 1
            # Se o byte está cheio, grava ele em arquivo binário
            if bitPosition == 8:
                outFile.write(currentByte.to_bytes(1, byteorder='big'))
                # Reseta a contagem
                currentByte = 0
                bitPosition = 0

# Opção de Descomprimir (caso a extensão seja z78)
if args.extract:
    # Abrindo arquivo
    with open(input_file, 'rb') as inFile:
        binary = inFile.read()
        inFile.close
        codeZ78 = ''.join(format(byte, '08b') for byte in binary)
    # Descompressão
    decompressedFile = Compression.decoding(codeZ78)
    # Salvando texto em arquivo de texto
    if output_file == None:
        output_file = input_file[:-3] + 'txt'
    with open(output_file, 'w') as outFile:
        outFile.write(decompressedFile)
