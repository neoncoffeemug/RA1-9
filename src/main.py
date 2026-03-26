import sys
from lerArquivo import lerArquivo
from parseExpressao import parseExpressao
from salvarTokens import salvarTokens
from executarExpressao import executarExpressao
from gerarAssembly import gerar_assembly

if len(sys.argv) < 2:
    print("Uso: python main.py <arquivo>")
    sys.exit(1)

nomeArquivo = sys.argv[1]
linhas = lerArquivo(nomeArquivo)

resultados_tokens = []
codigo_assembly = []

memoria = {}
historico = []

for linha in linhas:
    tokens = []
    valido = parseExpressao(linha, tokens)

    if not valido:
        print(f"Erro léxico: {linha}")
        continue


    resultados_tokens.append((linha, tokens))

    try:
        resultado = executarExpressao(tokens, memoria, historico)
        historico.append(resultado)

        print("Linha:", linha)
        print("Resultado:", resultado)
        print()

    
        asm_linha = gerar_assembly(tokens)

        codigo_assembly.append(f"; {linha}")
        codigo_assembly.extend(asm_linha)
        codigo_assembly.append("") 

    except Exception as e:
        print(f"Erro na execução: {linha}")
        print("Motivo:", e)
        print()

salvarTokens("output/tokens.txt", resultados_tokens)


with open("output/programa.s", "w") as f:
    f.write(".text\n.global _start\n_start:\n\n")

    for linha in codigo_assembly:
        f.write(linha + "\n")

    f.write("\n; fim\n")