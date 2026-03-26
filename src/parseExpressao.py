def parseExpressao(linha, tokens):
    i = 0
    parenteses = 0

    while i < len(linha):
        i, parenteses, valido = estadoInicial(linha, i, tokens, parenteses)

        if not valido:
            tokens.clear()
            return False

    if parenteses != 0:
        print("Erro: parênteses não balanceados")
        tokens.clear()
        return False

    return True


def estadoInicial(linha, i, tokens, parenteses):
    c = linha[i]

    if c == " ":
        return i + 1, parenteses, True

    if c == "(":
        tokens.append(("LPAREN", "("))
        return i + 1, parenteses + 1, True

    if c == ")":
        parenteses -= 1
        if parenteses < 0:
            print("Erro: parêntese fechado sem abertura")
            return i, parenteses, False

        tokens.append(("RPAREN", ")"))
        return i + 1, parenteses, True

    if c.isdigit() or c == ".":
        novo_i, valido = estadoNumero(linha, i, tokens)
        return novo_i, parenteses, valido

    if c in "+-*%^":
        tokens.append(("OPERADOR", c))
        return i + 1, parenteses, True

    if c == "/":
        novo_i = estadoDivisao(linha, i, tokens)
        return novo_i, parenteses, True

    if c.isalpha():
        novo_i, valido = estadoIdentificador(linha, i, tokens)
        return novo_i, parenteses, valido

    print(f"Erro: caractere inválido '{c}'")
    return i, parenteses, False


def estadoNumero(linha, i, tokens):
    numero = ""
    pontos = 0
    tamanho = len(linha)

    if linha[i] == ".":
        if i + 1 >= tamanho or not linha[i + 1].isdigit():
            print("Erro: número malformado")
            return i, False

    while i < tamanho and (linha[i].isdigit() or linha[i] == "."):
        if linha[i] == ".":
            pontos += 1
            if pontos > 1:
                print("Erro: número com múltiplos pontos")
                return i, False

        numero += linha[i]
        i += 1

    if i < tamanho and linha[i].isalpha():
        print("Erro: número malformado com letras")
        return i, False

    tokens.append(("NUMERO", numero))
    return i, True


def estadoDivisao(linha, i, tokens):
    if i + 1 < len(linha) and linha[i + 1] == "/":
        tokens.append(("OPERADOR", "//"))
        return i + 2

    tokens.append(("OPERADOR", "/"))
    return i + 1


def estadoIdentificador(linha, i, tokens):
    palavra = ""
    tamanho = len(linha)

    while i < tamanho and linha[i].isalpha():
        palavra += linha[i]
        i += 1

    if not palavra.isupper():
        print(f"Erro: identificador inválido '{palavra}'. Use apenas letras maiúsculas.")
        return i, False

    if palavra == "RES":
        tokens.append(("RES", palavra))
    else:
        tokens.append(("VAR", palavra))

    return i, True