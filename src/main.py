import sys
from lerArquivo import lerArquivo
from parseExpressao import parseExpressao
from salvarTokens import salvarTokens
from executarExpressao import executarExpressao
from gerarAssembly import gerarAssembly

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

        try:
            resultado = executarExpressao(tokens, memoria, historico)
            historico.append(resultado)

            print(f"Linha {numero_linha}: {linha}")
            print(f"Tokens: {tokens}")
            print(f"Resultado: {resultado}")
            print(f"Memória atual: {memoria}")
            print()

        except Exception as e:
            print(f"Erro na execução da linha {numero_linha}: {linha}")
            print(f"Motivo: {e}")
            print()

    salvarTokens("output/tokens.txt", linhas_tokenizadas)
    gerarAssembly(linhas_tokenizadas, "output/programa.s")
    print("Assembly gerado em output/programa.s")

if __name__ == "__main__":
    main()
