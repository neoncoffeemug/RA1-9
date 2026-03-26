import os


class GeradorAssembly:
    def __init__(self):
        self.texto = []
        self.dados = []
        self.constantes = {}
        self.memorias = set()
        self.resultados = []
        self.contador_const = 0
        self.const_zero = None
        self.const_um = None

    def emitir(self, linha):
        self.texto.append(linha)

    def adicionarConstante(self, valor):
        if valor not in self.constantes:
            rotulo = f"const_{self.contador_const}"
            self.constantes[valor] = rotulo
            self.dados.append(f"{rotulo}: .double {valor}")
            self.contador_const += 1
        return self.constantes[valor]

    def carregarConstante(self, valor):
        rotulo = self.adicionarConstante(valor)
        self.emitir(f"    LDR r0, ={rotulo}")
        self.emitir(f"    VLDR.F64 d0, [r0]")

    def carregarMemoria(self, nome):
        self.memorias.add(nome)
        self.emitir(f"    LDR r0, =mem_{nome}")
        self.emitir(f"    VLDR.F64 d0, [r0]")

    def salvarMemoria(self, nome):
        self.memorias.add(nome)
        self.emitir(f"    LDR r0, =mem_{nome}")
        self.emitir(f"    VSTR.F64 d0, [r0]")

    def salvarResultado(self, indice):
        self.emitir(f"    LDR r0, ={self.resultados[indice]}")
        self.emitir("    VSTR.F64 d0, [r0]")


def construirAST(tokens):
    def parseItem(pos):
        if pos >= len(tokens):
            raise Exception("Fim inesperado dos tokens")

        tipo, valor = tokens[pos]

        if tipo == "NUMERO":
            return {"tipo": "numero", "valor": valor}, pos + 1

        if tipo == "VAR":
            return {"tipo": "identificador", "nome": valor}, pos + 1

        if tipo == "RES":
            return {"tipo": "res_kw"}, pos + 1

        if tipo == "OPERADOR":
            return {"tipo": "operador", "valor": valor}, pos + 1

        if tipo == "LPAREN":
            pos += 1
            itens = []

            while pos < len(tokens) and tokens[pos][0] != "RPAREN":
                item, pos = parseItem(pos)
                itens.append(item)

            if pos >= len(tokens):
                raise Exception("Parênteses desbalanceados")

            pos += 1
            return montarNo(itens), pos

        raise Exception(f"Token inesperado: {tokens[pos]}")

    def montarNo(itens):
        if len(itens) == 1 and itens[0]["tipo"] == "identificador":
            return {"tipo": "mem_get", "nome": itens[0]["nome"]}

        if len(itens) == 2:
            if itens[0]["tipo"] == "numero" and itens[1]["tipo"] == "res_kw":
                numero = itens[0]["valor"]
                if "." in numero:
                    raise Exception("(N RES) exige inteiro")
                return {"tipo": "res", "n": int(numero)}

            if itens[1]["tipo"] == "identificador":
                return {
                    "tipo": "mem_set",
                    "valor": itens[0],
                    "nome": itens[1]["nome"]
                }

        if len(itens) == 3 and itens[2]["tipo"] == "operador":
            return {
                "tipo": "binop",
                "esq": itens[0],
                "dir": itens[1],
                "op": itens[2]["valor"]
            }

        raise Exception(f"Estrutura inválida: {itens}")

    ast, pos = parseItem(0)

    if pos != len(tokens):
        raise Exception("Sobraram tokens após a AST")

    return ast


def gerarExpressao(gerador, no, indiceLinha):
    tipo = no["tipo"]

    if tipo == "numero":
        gerador.carregarConstante(no["valor"])
        return

    if tipo == "mem_get":
        gerador.carregarMemoria(no["nome"])
        return

    if tipo == "mem_set":
        gerarExpressao(gerador, no["valor"], indiceLinha)
        gerador.salvarMemoria(no["nome"])
        return

    if tipo == "res":
        alvo = indiceLinha - no["n"]
        if alvo < 0:
            raise Exception(f"(N RES) inválido na linha {indiceLinha + 1}")
        gerador.emitir(f"    LDR r0, ={gerador.resultados[alvo]}")
        gerador.emitir("    VLDR.F64 d0, [r0]")
        return

    if tipo == "binop":
        gerarExpressao(gerador, no["esq"], indiceLinha)
        gerador.emitir("    SUB sp, sp, #8")
        gerador.emitir("    VSTR.F64 d0, [sp]")

        gerarExpressao(gerador, no["dir"], indiceLinha)

        gerador.emitir("    VLDR.F64 d1, [sp]")
        gerador.emitir("    ADD sp, sp, #8")

        operacoes = {
            "+": "VADD.F64 d0, d1, d0",
            "-": "VSUB.F64 d0, d1, d0",
            "*": "VMUL.F64 d0, d1, d0",
            "/": "VDIV.F64 d0, d1, d0",
            "//": "BL inteiro_div",
            "%": "BL inteiro_mod",
            "^": "BL potencia_int"
        }

        if no["op"] not in operacoes:
            raise Exception(f"Operador não suportado: {no['op']}")

        gerador.emitir(f"    {operacoes[no['op']]}")
        return

    raise Exception(f"Tipo inválido: {tipo}")


def gerarRotinas(gerador):
    gerador.emitir("")
    gerador.emitir("inteiro_div:")
    gerador.emitir("    VCVT.S32.F64 s2, d1")
    gerador.emitir("    VMOV r4, s2")
    gerador.emitir("    VCVT.S32.F64 s3, d0")
    gerador.emitir("    VMOV r5, s3")
    gerador.emitir("    CMP r5, #0")
    gerador.emitir("    BEQ erro_div_zero")
    gerador.emitir("    MOV r8, #0")
    gerador.emitir("    MOV r9, #0")
    gerador.emitir("    CMP r4, #0")
    gerador.emitir("    RSBLT r6, r4, #0")
    gerador.emitir("    MOVGE r6, r4")
    gerador.emitir("    CMP r5, #0")
    gerador.emitir("    RSBLT r7, r5, #0")
    gerador.emitir("    MOVGE r7, r5")
    gerador.emitir("    CMP r4, #0")
    gerador.emitir("    EORLT r9, r9, #1")
    gerador.emitir("    CMP r5, #0")
    gerador.emitir("    EORLT r9, r9, #1")
    gerador.emitir("div_loop:")
    gerador.emitir("    CMP r6, r7")
    gerador.emitir("    BLT div_fim")
    gerador.emitir("    SUB r6, r6, r7")
    gerador.emitir("    ADD r8, r8, #1")
    gerador.emitir("    B div_loop")
    gerador.emitir("div_fim:")
    gerador.emitir("    CMP r9, #0")
    gerador.emitir("    RSBNE r8, r8, #0")
    gerador.emitir("    VMOV s0, r8")
    gerador.emitir("    VCVT.F64.S32 d0, s0")
    gerador.emitir("    BX lr")

    gerador.emitir("")
    gerador.emitir("inteiro_mod:")
    gerador.emitir("    VCVT.S32.F64 s2, d1")
    gerador.emitir("    VMOV r4, s2")
    gerador.emitir("    VCVT.S32.F64 s3, d0")
    gerador.emitir("    VMOV r5, s3")
    gerador.emitir("    CMP r5, #0")
    gerador.emitir("    BEQ erro_div_zero")
    gerador.emitir("    CMP r4, #0")
    gerador.emitir("    RSBLT r6, r4, #0")
    gerador.emitir("    MOVGE r6, r4")
    gerador.emitir("    CMP r5, #0")
    gerador.emitir("    RSBLT r7, r5, #0")
    gerador.emitir("    MOVGE r7, r5")
    gerador.emitir("mod_loop:")
    gerador.emitir("    CMP r6, r7")
    gerador.emitir("    BLT mod_fim")
    gerador.emitir("    SUB r6, r6, r7")
    gerador.emitir("    B mod_loop")
    gerador.emitir("mod_fim:")
    gerador.emitir("    CMP r4, #0")
    gerador.emitir("    RSBMI r6, r6, #0")
    gerador.emitir("    VMOV s0, r6")
    gerador.emitir("    VCVT.F64.S32 d0, s0")
    gerador.emitir("    BX lr")

    gerador.emitir("")
    gerador.emitir("potencia_int:")
    gerador.emitir("    VCVT.S32.F64 s3, d0")
    gerador.emitir("    VMOV r5, s3")
    gerador.emitir(f"    LDR r0, ={gerador.const_um}")
    gerador.emitir("    VLDR.F64 d0, [r0]")
    gerador.emitir("pot_loop:")
    gerador.emitir("    CMP r5, #0")
    gerador.emitir("    BEQ pot_fim")
    gerador.emitir("    VMUL.F64 d0, d0, d1")
    gerador.emitir("    SUB r5, r5, #1")
    gerador.emitir("    B pot_loop")
    gerador.emitir("pot_fim:")
    gerador.emitir("    BX lr")

    gerador.emitir("")
    gerador.emitir("erro_div_zero:")
    gerador.emitir("    B erro_div_zero")


def gerarAssembly(resultadosTokens, nomeArquivoSaida="output/programa.s"):
    pasta = os.path.dirname(nomeArquivoSaida)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)

    gerador = GeradorAssembly()
    gerador.const_zero = gerador.adicionarConstante("0.0")
    gerador.const_um = gerador.adicionarConstante("1.0")
    gerador.resultados = [f"resultado_{i}" for i in range(len(resultadosTokens))]

    gerador.emitir(".global _start")
    gerador.emitir(".text")
    gerador.emitir("_start:")

    for indice, (_, tokens) in enumerate(resultadosTokens):
        ast = construirAST(tokens)
        gerarExpressao(gerador, ast, indice)
        gerador.salvarResultado(indice)

    gerador.emitir("")
    gerador.emitir("fim:")
    gerador.emitir("    B fim")

    gerarRotinas(gerador)

    secaoDados = ["", ".data"]

    for nome in sorted(gerador.memorias):
        secaoDados.append(f"mem_{nome}: .double 0.0")

    for rotulo in gerador.resultados:
        secaoDados.append(f"{rotulo}: .double 0.0")

    secaoDados.extend(gerador.dados)

    codigo = "\n".join(gerador.texto + secaoDados)

    with open(nomeArquivoSaida, "w", encoding="utf-8") as arquivo:
        arquivo.write(codigo)

    return codigo