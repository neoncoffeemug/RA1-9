def parseExpressao(linha, tokens):
    i = 0
    tamanho = len(linha)
    parenteses = 0

    while i < tamanho:
        c = linha[i]

        # estado inicial (ignora espaço)
        if c == " ":
            i += 1
            continue

        # estado parênteses
        if c == "(":
            tokens.append(("LPAREN", "("))
            parenteses += 1
            i += 1
            continue

        if c == ")":
            parenteses -= 1
            if parenteses < 0:
                print("Erro: parêntese fechado sem abrir")
                tokens.clear()
                return False

            tokens.append(("RPAREN", ")"))
            i += 1
            continue

        # estado número
        if c.isdigit() or c == ".":
            i = estadoNumero(linha, i, tokens)
            if i == -1:
                tokens.clear()
                return False
            continue

        # estado operador
        if c in "+-*%^":
            tokens.append(("OPERADOR", c))
            i += 1
            continue

        # estado divisão
        if c == "/":
            if i + 1 < tamanho and linha[i+1] == "/":
                tokens.append(("OPERADOR", "//"))
                i += 2
            else:
                tokens.append(("OPERADOR", "/"))
                i += 1
            continue

        # estado identificador
        if c.isalpha():
            i = estadoIdentificador(linha, i, tokens)
            if i == -1:
                tokens.clear()
                return False
            continue

        # erro léxico
        print(f"Erro: caractere inválido '{c}'")
        tokens.clear()
        return False

    if parenteses != 0:
        tokens.clear()
        print("Erro: parênteses não balanceados")
        return False

    return True

def estadoIdentificador(linha, i, tokens):
    palavra = ""
    tamanho = len(linha)

    while i < tamanho and linha[i].isalpha():
        palavra += linha[i]
        i += 1

    if palavra == "RES":
        tokens.append(("RES", palavra))
    else:
        tokens.append(("VAR", palavra))

    return i

def estadoNumero(linha, i, tokens):
    numero = ""
    pontos = 0
    tamanho = len(linha)

    if linha[i] == ".":
        if i + 1 >= tamanho or not linha[i+1].isdigit():
            print("Erro: número malformado")
            return -1

    while i < tamanho and (linha[i].isdigit() or linha[i] == "."):
        if linha[i] == ".":
            pontos += 1
            if pontos > 1:
                print("Erro: número com múltiplos pontos")
                return -1

        numero += linha[i]
        i += 1

    tokens.append(("NUMERO", numero))
    return i