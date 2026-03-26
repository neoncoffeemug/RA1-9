def gerar_assembly(tokens):
    codigo = []

    for tipo, valor in tokens:

        if tipo == "NUMERO":
            codigo.append(f"MOV R0, #{valor}")
            codigo.append("PUSH {R0}")

        elif tipo == "OPERADOR":
            codigo.append("POP {R1}")
            codigo.append("POP {R0}")

            if valor == "+":
                codigo.append("ADD R0, R0, R1")

            elif valor == "-":
                codigo.append("SUB R0, R0, R1")

            elif valor == "*":
                codigo.append("MUL R0, R0, R1")

            elif valor == "/":
                codigo.append("SDIV R0, R0, R1")

            elif valor == "//":
                codigo.append("SDIV R0, R0, R1")

            elif valor == "%":
                codigo.append("SDIV R2, R0, R1")
                codigo.append("MUL R2, R2, R1")
                codigo.append("SUB R0, R0, R2")

            elif valor == "^":
                codigo.append("; potência (implementar loop)")

            codigo.append("PUSH {R0}")

    return codigo