def check_torre(posicao, cor, brancas_posicao, pretas_posicao):
    movimentos_lista = []

    # Aqui é checado de qual time a torre é:

    if cor == 'brancos':
        lista_inimigos = pretas_posicao
        lista_amigos = brancas_posicao
    else:
        lista_inimigos = brancas_posicao
        lista_amigos = pretas_posicao

    #Range de 4, por causa que a torre anda em quatro direções
    for i in range(4):
        caminho_percorrer = True
        chain = 1
        #Descendo:
        if i == 0:
            x = 0
            y = 1
        #Subindo
        elif i == 1:
            x = 0
            y = -1
        #Direita
        elif i == 2:
            x = 1
            y = 0
        #Esquerda
        elif i == 3:
            x = -1
            y = 0
        while caminho_percorrer:
            if ((posicao[0] + (chain * x), posicao[1] + (chain * y)) not in lista_amigos and 0 <= posicao[0] +
                    (chain * x) <= 7 and 0 <= posicao[1] + (chain * y) <= 7):
                movimentos_lista.append((posicao[0] + (chain * x), posicao[1] + (chain * y)))
                if (posicao[0] + (chain * x), posicao[1] + (chain * y)) in lista_inimigos:
                    caminho_percorrer = False
                chain += 1
            else:
                caminho_percorrer = False

    return movimentos_lista