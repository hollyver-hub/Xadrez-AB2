def check_cavalo(posicao, cor, brancas_posicao, pretas_posicao):
    movimentos_lista = []

    # Aqui é checado de qual time o cavalo é:

    if cor == 'brancos':
        lista_amigos = brancas_posicao
    else:
        lista_amigos = pretas_posicao

    movimentos_do_cavalo = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

    for i in range(8):
        movimento_cavalo = (posicao[0] + movimentos_do_cavalo[i][0], posicao[1] + movimentos_do_cavalo[i][1])
        if movimento_cavalo not in lista_amigos and 0 <= movimento_cavalo[0] <= 7 and 0 <= movimento_cavalo[1] <= 7:
            movimentos_lista.append(movimento_cavalo)

    return movimentos_lista