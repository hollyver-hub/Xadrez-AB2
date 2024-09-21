def check_peao(posicao, cor, brancas_posicao, pretas_posicao):
    movimentos_lista = []
    if cor == 'brancos':

        #Movimento normal do peao:

        if ((posicao[0], posicao[1] - 1) not in brancas_posicao and
                (posicao[0], posicao[1] - 1) not in pretas_posicao and posicao[1] > 0):
            movimentos_lista.append((posicao[0], posicao[1] - 1))


        #Movimento de duas casas somente quando estiver na posição inicial:

        if ((posicao[0], posicao[1] - 2) not in brancas_posicao and
                (posicao[0], posicao[1] - 2) not in pretas_posicao and posicao[1] == 6):
            movimentos_lista.append((posicao[0], posicao[1] - 2))

        #Movimento de captura de peça para a diagonal esquerda:

        if (posicao[0] - 1, posicao[1] - 1) in pretas_posicao:
            movimentos_lista.append((posicao[0] - 1, posicao[1] - 1))

        #Movimento de captura de peça para a diagonal direita:

        if (posicao[0] + 1, posicao[1] - 1) in pretas_posicao:
            movimentos_lista.append((posicao[0] + 1, posicao[1] - 1))


    else:

        # Movimento normal do peao:

        if (posicao[0], posicao[1] + 1) not in brancas_posicao and (
                posicao[0], posicao[1] + 1) not in pretas_posicao and posicao[1] < 7:
            movimentos_lista.append((posicao[0], posicao[1] + 1))

        # Movimento de duas casas somente quando estiver na posição inicial:

        if (posicao[0], posicao[1] + 2) not in brancas_posicao and (
                posicao[0], posicao[1] + 2) not in pretas_posicao and posicao[1] == 1:
            movimentos_lista.append((posicao[0], posicao[1] + 2))

        # Movimento de captura de peça para a diagonal esquerda:

        if (posicao[0] - 1, posicao[1] + 1) in brancas_posicao:
            movimentos_lista.append((posicao[0] - 1, posicao[1] + 1))

        # Movimento de captura de peça para a diagonal direita:

        if (posicao[0] + 1, posicao[1] + 1) in brancas_posicao:
            movimentos_lista.append((posicao[0] + 1, posicao[1] + 1))

    return movimentos_lista