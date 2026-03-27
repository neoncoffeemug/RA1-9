def lerArquivo(nomeArquivo):
    linhas = []

    try:
        with open(nomeArquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    linhas.append(linha)

        return linhas

    except FileNotFoundError:
        print(f"Erro: arquivo '{nomeArquivo}' não encontrado.")
        return []

    except Exception as erro:
        print(f"Erro ao ler o arquivo: {erro}")
        return []