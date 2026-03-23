def parseExpressao(linha, tokens):
    i = 0
    tamanho = len(linha)
    parenteses = 0

    while i < tamanho:
        c = linha[i]

        # ignora espaço
        if c == " ":
            i += 1
            continue

        # parênteses
        if c == "(":
            tokens.append(("LPAREN", "("))
            parenteses += 1
            i += 1
            continue

        if c == ")":
            parenteses -= 1
            if parenteses < 0:
                return False
            tokens.append(("RPAREN", ")"))
            i += 1
            continue

        # números (inteiro ou decimal)
        if c.isdigit() or c == ".":
            numero = ""
            pontos = 0
            
            if c == ".":
                if i + 1 >= tamanho or not linha [i + 1].isdigit():
                    print("Erro léxico '{c}'")
                    return False

            while i < tamanho and (linha[i].isdigit() or linha[i] == "."):
                if linha[i] ==".":
                    pontos += 1
                    if pontos > 1:
                        return False
                numero += linha[i]
                i += 1

            tokens.append(("NUMERO", numero))
            continue

        # operadores simples
        if c in "+-*%^":
            tokens.append(("OPERADOR", c))
            i += 1
            continue

        # divisão inteira //
        if c == "/":
            if i + 1 < tamanho and linha[i+1] == "/":
                tokens.append(("OPERADOR", "//"))
                i += 2
            else:
                tokens.append(("OPERADOR", "/"))
                i += 1
            continue

        # identificadores (MEM, X, RES)
        if c.isalpha():
            palavra = ""

            while i < tamanho and linha[i].isalpha():
                palavra += linha[i]
                i += 1

            if palavra == "RES":
                tokens.append(("RES", palavra))
            else:
                tokens.append(("VAR", palavra))

            continue

        # erro
        return False
    
    if parenteses != 0:
        return False

    return True