import os

def salvarTokens(nomeArquivoSaida, resultados):
    pasta = os.path.dirname(nomeArquivoSaida)

    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)

    with open(nomeArquivoSaida, "w", encoding="utf-8") as arquivo:
        for linha_original, tokens in resultados:
            arquivo.write(f"Linha: {linha_original}\n")
            arquivo.write(f"Tokens: {tokens}\n\n")