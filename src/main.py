import sys
from lerArquivo import lerArquivo
from parseExpressao import parseExpressao
from salvarTokens import salvarTokens
from gerarAssembly import gerarAssembly
from executarExpressao import executarExpressao
from exibirResultados import exibirResultados

MODO_TESTE = True

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        sys.exit(1)

    nomeArquivo = sys.argv[1]
    linhas = lerArquivo(nomeArquivo)

    if not linhas:
        print("Nenhuma linha foi lida do arquivo.")
        sys.exit(1)

    linhas_tokenizadas = []
    resultados = []
    memoria = {}
    historico = []

    for numero_linha, linha in enumerate(linhas, start=1):
        tokens = []
        valido = parseExpressao(linha, tokens)

        if not valido:
            print(f"Erro léxico na linha {numero_linha}: {linha}")
            print()
            continue

        linhas_tokenizadas.append((linha, tokens))

        print(f"Linha {numero_linha}: {linha}")
        print(f"Tokens: {tokens}")

        if MODO_TESTE: # Testa a execução da expressão
            try:
                resultado = executarExpressao(tokens, memoria, historico)
                historico.append(resultado)
                resultados.append(resultado)
            except Exception as e:
                print(f"Erro no teste de execução: {e}")

        print()

    if MODO_TESTE:
        exibirResultados(resultados)

    salvarTokens("output/tokens.txt", linhas_tokenizadas)
    gerarAssembly(linhas_tokenizadas, "output/programa.s")
    print("Assembly gerado em output/programa.s")

if __name__ == "__main__":
    main()