def executarExpressao(tokens, memoria, historico):
    def parse_item(pos):
        if pos >= len(tokens):
            raise Exception("Fim inesperado dos tokens")

        tipo, valor = tokens[pos]

        if tipo == "NUMERO":
            return float(valor), pos + 1

        if tipo == "LPAREN":
            return parse_expressao(pos)

        if tipo == "VAR":
            # VAR sozinho só faz sentido dentro de estruturas como:
            # (MEM)  -> leitura
            # (V MEM) -> escrita
            return ("VAR", valor), pos + 1

        if tipo == "RES":
            return ("RES", valor), pos + 1

        if tipo == "OPERADOR":
            return ("OPERADOR", valor), pos + 1

        raise Exception(f"Token inesperado: {tokens[pos]}")

    def parse_expressao(pos):
        if pos >= len(tokens) or tokens[pos][0] != "LPAREN":
            raise Exception("Esperado '(' no início da expressão")

        pos += 1
        itens = []

        while pos < len(tokens) and tokens[pos][0] != "RPAREN":
            item, pos = parse_item(pos)
            itens.append(item)

        if pos >= len(tokens) or tokens[pos][0] != "RPAREN":
            raise Exception("Parêntese de fechamento ausente")

        pos += 1

        valor = avaliar_itens(itens)
        return valor, pos

    def avaliar_itens(itens):
        # Caso 1: (MEM)
        if len(itens) == 1:
            item = itens[0]

            if isinstance(item, tuple) and item[0] == "VAR":
                nome_memoria = item[1]
                return memoria.get(nome_memoria, 0.0)

            raise Exception(f"Estrutura inválida com 1 item: {itens}")

        # Caso 2: (N RES) ou (V MEM)
        if len(itens) == 2:
            primeiro, segundo = itens

            # (N RES)
            if isinstance(segundo, tuple) and segundo[0] == "RES":
                if not isinstance(primeiro, (int, float)):
                    raise Exception("(N RES) exige número na primeira posição")

                if int(primeiro) != primeiro or primeiro < 0:
                    raise Exception("(N RES) exige inteiro não negativo")

                n = int(primeiro)

                if n == 0:
                    if historico:
                        return historico[-1]
                    return 0.0

                if n > len(historico):
                    return 0.0

                return historico[-n]

            # (V MEM)
            if isinstance(segundo, tuple) and segundo[0] == "VAR":
                nome_memoria = segundo[1]

                if not isinstance(primeiro, (int, float)):
                    raise Exception("(V MEM) exige valor numérico ou expressão válida")

                memoria[nome_memoria] = float(primeiro)
                return float(primeiro)

            raise Exception(f"Estrutura inválida com 2 itens: {itens}")

        # Caso 3: (A B op)
        if len(itens) == 3:
            a, b, op = itens

            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                raise Exception("Operação aritmética exige dois operandos numéricos")

            if not (isinstance(op, tuple) and op[0] == "OPERADOR"):
                raise Exception("Operação aritmética exige operador na terceira posição")

            operador = op[1]

            if operador == "+":
                return a + b
            elif operador == "-":
                return a - b
            elif operador == "*":
                return a * b
            elif operador == "/":
                if b == 0:
                    raise Exception("Divisão por zero")
                return a / b
            elif operador == "//":
                if b == 0:
                    raise Exception("Divisão inteira por zero")
                return int(a) // int(b)
            elif operador == "%":
                if b == 0:
                    raise Exception("Resto por zero")
                return int(a) % int(b)
            elif operador == "^":
                if int(b) != b or b < 0:
                    raise Exception("Potenciação exige expoente inteiro não negativo")
                return a ** int(b)

            raise Exception(f"Operador inválido: {operador}")

        raise Exception(f"Estrutura inválida: {itens}")

    resultado, pos_final = parse_expressao(0)

    if pos_final != len(tokens):
        raise Exception("Sobraram tokens após o fim da expressão")

    return resultado