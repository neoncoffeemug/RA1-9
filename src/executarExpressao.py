def executarExpressao(tokens, memoria, historico):
    
    def avaliar(pos):
        stack = []

        while pos < len(tokens):
            tipo, valor = tokens[pos]

            if tipo == "LPAREN":
                resultado, pos = avaliar(pos + 1)
                stack.append(resultado)
                continue

            elif tipo == "RPAREN":
                break

            elif tipo == "NUMERO":
                stack.append(float(valor))

            elif tipo == "VAR":
                if valor in memoria:
                    stack.append(memoria[valor])
                else:
                    raise Exception(f"Variável '{valor}' não definida")

            elif tipo == "RES":
                if historico:
                    stack.append(historico[-1])
                else:
                    stack.append(0.0)

            elif tipo == "OPERADOR":
                b = stack.pop()
                a = stack.pop()

                if valor == "+":
                    stack.append(a + b)
                elif valor == "-":
                    stack.append(a - b)
                elif valor == "*":
                    stack.append(a * b)
                elif valor == "/":
                    stack.append(a / b)
                elif valor == "//":
                    stack.append(int(a) // int(b))
                elif valor == "%":
                    stack.append(int(a) % int(b))
                elif valor == "^":
                    stack.append(a ** b)

            pos += 1

        if len(stack) == 1:
            return stack[0], pos

        if len(stack) == 1 and pos > 0:
            ultimo = tokens[pos - 1]
            if ultimo[0] == "VAR":
                memoria[ultimo[1]] = stack[0]
                return stack[0], pos

        return stack[-1] if stack else 0.0, pos

    resultado, _ = avaliar(0)
    return resultado