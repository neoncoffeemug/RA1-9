import sys
from lerArquivo import lerArquivo
from parseExpressao import parseExpressao
from salvarTokens import salvarTokens
from executarExpressao import executarExpressao

if len(sys.argv) < 2:
    print("Uso: python main.py <arquivo>")
    sys.exit(1)

nomeArquivo = sys.argv[1]
linhas = lerArquivo(nomeArquivo)

resultados = []

memoria = {}
historico = []

for linha in linhas:
    tokens = []
    valido = parseExpressao(linha, tokens)

    if not valido:
        print(f"Erro léxico: {linha}")
        continue

    resultados.append((linha, tokens))

    try:
        resultado = executarExpressao(tokens, memoria, historico)

        historico.append(resultado)

        print("Linha:", linha)
        print("Resultado:", resultado)
        print("Memória:", memoria)
        print()

    except Exception as e:
        print(f"Erro na execução: {linha}")
        print("Motivo:", e)
        print()

salvarTokens("output/tokens.txt", resultados)