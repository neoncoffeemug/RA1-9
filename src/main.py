import sys
from lerArquivo import lerArquivo
from parseExpressao import parseExpressao
from salvarTokens import salvarTokens

if len(sys.argv) < 2:
    print("Uso: python main.py <arquivo>")
    sys.exit(1)

nomeArquivo = sys.argv[1]
linhas = lerArquivo(nomeArquivo)

resultados = []

for linha in linhas:
    tokens = []

    valido = parseExpressao(linha, tokens)

    if not valido:
        print(f"Erro léxico na linha: {linha}")
        continue  # ignora linha inválida

    resultados.append((linha, tokens))

salvarTokens("../output/tokens.txt", resultados)