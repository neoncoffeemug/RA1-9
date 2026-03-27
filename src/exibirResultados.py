def exibirResultados(resultados):
    if not resultados:
        print("Nenhum resultado para exibir.")
        return

    print("Resultados das expressões:")
    for i, resultado in enumerate(resultados, start=1):
        print(f"Linha {i}: {resultado:.1f}")