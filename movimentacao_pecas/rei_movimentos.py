def check_rei(posicao, cor, brancas_posicao, pretas_posicao):
    movimentos_lista = []

    # Aqui é checado de qual time o rei é:

    if cor == 'brancos':
        lista_amigos = brancas_posicao
    else:
        lista_amigos = pretas_posicao

    movimentos_do_rei = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    for i in range(8):
        movimento_rei = (posicao[0] + movimentos_do_rei[i][0], posicao[1] + movimentos_do_rei[i][1])
        if movimento_rei not in lista_amigos and 0 <= movimento_rei[0] <= 7 and 0 <= movimento_rei[1] <= 7:
            movimentos_lista.append(movimento_rei)

    return movimentos_lista

