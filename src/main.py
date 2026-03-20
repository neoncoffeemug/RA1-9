import sys
from lerArquivo import lerArquivo
from parseExpressao import parseExpressao

if len(sys.argv) < 2:
    print("Uso: python main.py <arquivo>")
    sys.exit(1)

nomeArquivo = sys.argv[1]

linhas = lerArquivo(nomeArquivo)

for linha in linhas:
    tokens = []
    parseExpressao(linha, tokens)

    print("Linha:", linha)
    print("Tokens:", tokens)
    print()