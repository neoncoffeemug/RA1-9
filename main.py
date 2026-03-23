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

    if valido:
        resultados.append((linha, tokens))  # ← ISSO É IMPORTANTE

salvarTokens("output/tokens.txt", resultados)