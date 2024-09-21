import pygame

# Inicialização

pygame.init()
screen = pygame.display.set_mode((480, 480))
timer = pygame.time.Clock()
turno = 0
counter = 0
selecionado = 50
movimentos_validos = []
game_over = False
pygame.display.set_caption('Xadrez - AB1')

# Importando as imagens para o pygame e altera o tamanho;

width_pecas = 55
height_pecas = 55

# Peças brancas:

torre_branca = pygame.image.load('images_refeito/rook-w.svg')
torre_branca = pygame.transform.scale(torre_branca, (width_pecas, height_pecas))

cavalo_branco = pygame.image.load('images_refeito/knight-w.svg')
cavalo_branco = pygame.transform.scale(cavalo_branco, (width_pecas, height_pecas))

bispo_branco = pygame.image.load('images_refeito/bishop-w.svg')
bispo_branco = pygame.transform.scale(bispo_branco, (width_pecas, height_pecas))

rainha_branca = pygame.image.load('images_refeito/queen-w.svg')
rainha_branca = pygame.transform.scale(rainha_branca, (width_pecas, height_pecas))

rei_branco = pygame.image.load('images_refeito/king-w.svg')
rei_branco = pygame.transform.scale(rei_branco, (width_pecas, height_pecas))

peao_branco = pygame.image.load('images_refeito/pawn-w.svg')
peao_branco = pygame.transform.scale(peao_branco, (width_pecas, height_pecas))

imagens_pecas_brancas = [torre_branca, cavalo_branco, bispo_branco, rainha_branca, rei_branco, peao_branco]

pecas_capturadas_branco = []

# Peças pretas:

torre_preta = pygame.image.load('images_refeito/rook-b.svg')
torre_preta = pygame.transform.scale(torre_preta, (width_pecas, height_pecas))

cavalo_preto = pygame.image.load('images_refeito/knight-b.svg')
cavalo_preto = pygame.transform.scale(cavalo_preto, (width_pecas, height_pecas))

bispo_preto = pygame.image.load('images_refeito/bishop-b.svg')
bispo_preto = pygame.transform.scale(bispo_preto, (width_pecas, height_pecas))

rainha_preto = pygame.image.load('images_refeito/queen-b.svg')
rainha_preto = pygame.transform.scale(rainha_preto, (width_pecas, height_pecas))

rei_preto = pygame.image.load('images_refeito/king-b.svg')
rei_preto = pygame.transform.scale(rei_preto, (width_pecas, height_pecas))

peao_preto = pygame.image.load('images_refeito/pawn-b.svg')
peao_preto = pygame.transform.scale(peao_preto, (width_pecas, height_pecas))

imagens_pecas_pretas = [torre_preta, cavalo_preto, bispo_preto, rainha_preto, rei_preto, peao_preto]

pecas_capturadas_preto = []

# Posicionamento das peças no tabuleiro

pecas_pretas = ['torre', 'cavalo', 'bispo', 'rainha', 'rei', 'bispo', 'cavalo', 'torre',
                'peao', 'peao', 'peao', 'peao', 'peao', 'peao', 'peao', 'peao']

pretas_posicao = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

pecas_brancas = ['torre', 'cavalo', 'bispo', 'rainha', 'rei', 'bispo', 'cavalo', 'torre',
                 'peao', 'peao', 'peao', 'peao', 'peao', 'peao', 'peao', 'peao']

brancas_posicao = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

todas_pecas = ['torre', 'cavalo', 'bispo', 'rainha', 'rei', 'peao']


# Função que desenha o tabuleiro

def desenha_tabuleiro():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [
                360 - (column * 120), row * 60, 60, 60])

        else:
            pygame.draw.rect(screen, 'light gray', [
                420 - (column * 120), row * 60, 60, 60])


def coloca_pecas():

    #Coloca as peças brancas:
    for i in range(len(pecas_pretas)):
        index = todas_pecas.index(pecas_pretas[i])
        screen.blit(imagens_pecas_pretas[index], (pretas_posicao[i][0] * 60, pretas_posicao[i][1] * 60 + 2))
        if turno < 2:
            if selecionado == i:
                pygame.draw.rect(screen, 'red', [brancas_posicao[i][0] * 60, brancas_posicao[i][1] * 60, 60, 60], 2)

    #Coloca peças pretas.
    for i in range(len(pecas_brancas)):
        index = todas_pecas.index(pecas_brancas[i])
        screen.blit(imagens_pecas_brancas[index], (brancas_posicao[i][0] * 60, brancas_posicao[i][1] * 60 + 2))

        if turno >= 2:
            if selecionado == i:
                pygame.draw.rect(screen, 'red', [pretas_posicao[i][0] * 60, pretas_posicao[i][1] * 60, 60, 60], 2)


def check_rei(posicao, cor):
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


def check_rainha(posicao, cor):
    # A rainha nada mais é do que a torre e o bispo juntos:

    movimentos_bispo = check_bispo(posicao, cor)
    movimentos_torre = check_torre(posicao, cor)

    for i in range(len(movimentos_bispo)):
        movimentos_torre.append(movimentos_bispo[i])

    return movimentos_torre


def check_bispo(posicao, cor):
    movimentos_lista = []
    # Aqui é checado de qual time o bispo é:

    if cor == 'brancos':
        lista_inimigos = pretas_posicao
        lista_amigos = brancas_posicao
    else:
        lista_inimigos = brancas_posicao
        lista_amigos = pretas_posicao

    # Range de 4, por causa que o bispo anda em quatro direções:
    for i in range(4):
        caminho_percorrer = True
        chain = 1
        # Descendo para direita:
        if i == 0:
            x = 1
            y = 1
        # Descendo para esquerda
        elif i == 1:
            x = -1
            y = 1
        # Subindo para direita
        elif i == 2:
            x = 1
            y = -1
        # Subindo para esquerda
        elif i == 3:
            x = -1
            y = -1
        while caminho_percorrer:
            if (posicao[0] + (chain * x), posicao[1] + (chain * y)) not in lista_amigos and 0 <= posicao[0] + (
                    chain * x) <= 7 and 0 <= posicao[1] + (chain * y) <= 7:
                movimentos_lista.append((posicao[0] + (chain * x), posicao[1] + (chain * y)))
                if (posicao[0] + (chain * x), posicao[1] + (chain * y)) in lista_inimigos:
                    caminho_percorrer = False
                chain += 1
            else:
                caminho_percorrer = False

    return movimentos_lista


def check_cavalo(posicao, cor):
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

def check_torre(posicao, cor):
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


def check_peao(posicao, cor):
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


def check_opcoes(pecas, posicao, turno):
    lista_movimentos = []
    todos_os_movimentos = []

    for i in range(len(pecas)):
        localizacao = posicao[i]
        peca = pecas[i]
        if peca == 'peao':
            lista_movimentos = check_peao(localizacao, turno)

        if peca == 'torre':
            lista_movimentos = check_torre(localizacao, turno)

        if peca == 'cavalo':
            lista_movimentos = check_cavalo(localizacao, turno)

        if peca == 'bispo':
            lista_movimentos = check_bispo(localizacao, turno)

        if peca == 'rainha':
            lista_movimentos = check_rainha(localizacao, turno)

        if peca == 'rei':
            lista_movimentos = check_rei(localizacao, turno)

        todos_os_movimentos.append(lista_movimentos)

    return todos_os_movimentos


def check_movimentos_validos():
    if turno < 2:
        opcoes_lista = brancas_opcoes
    else:
        opcoes_lista = pretas_opcoes
    opcoes_validas = opcoes_lista[selecionado]

    return opcoes_validas


def desenha_validos(movimentos):
    for i in range(len(movimentos)):
        pygame.draw.circle(screen, 'red', (movimentos[i][0] * 60 + 30, movimentos[i][1] * 60 + 30), 5)


def desenha_cheque():
    if turno < 2:
        if 'rei' in pecas_brancas:

            rei_index = pecas_brancas.index('rei')
            rei_posicao = brancas_posicao[rei_index]
            for i in range(len(pretas_posicao)):
                movimentos_inimigo = check_opcoes([pecas_pretas[i]], [pretas_posicao[i]], 'pretos')[0]
                if rei_posicao in movimentos_inimigo:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [rei_posicao[0] * 60, rei_posicao[1] * 60, 60, 60], 5)
    else:
        if 'rei' in pecas_pretas:
            rei_index = pecas_pretas.index('rei')
            rei_posicao = pretas_posicao[rei_index]
            for i in range(len(brancas_posicao)):
                movimentos_inimigo = check_opcoes([pecas_brancas[i]], [brancas_posicao[i]], 'brancos')[0]
                if rei_posicao in movimentos_inimigo:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [rei_posicao[0] * 60, rei_posicao[1] * 60, 60, 60], 5)


def desenha_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 50])


pretas_opcoes = check_opcoes(pecas_pretas, pretas_posicao, 'pretos')
brancas_opcoes = check_opcoes(pecas_brancas, brancas_posicao, 'brancos')
jogando = True
while jogando:
    timer.tick(60)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    desenha_tabuleiro()
    coloca_pecas()
    desenha_cheque()
    if selecionado != 50:
        movimentos_validos = check_movimentos_validos()
        desenha_validos(movimentos_validos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False
        # Pega as coordenadas do click.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coordenada = event.pos[0] // 60
            y_coordenada = event.pos[1] // 60
            click_coordenada = (x_coordenada, y_coordenada)
            # Turno do branco.
            if turno <= 1:
                # Verifica se o click foi em alguma peça branca, se foi checa os movimentos válidos.
                if click_coordenada in brancas_posicao:
                    selecionado = brancas_posicao.index(click_coordenada)
                    movimentos_validos = check_movimentos_validos()
                    if turno == 0:
                        turno = 1
                # Se houver uma peça selecionada, e o click estiver na lista de movimentos válidos, coloca a peça na posição desejada.
                if click_coordenada in movimentos_validos and selecionado != 50:
                    brancas_posicao[selecionado] = click_coordenada
                    #Se o movimento for válido e o click for em cima de uma peça inimiga, "come" ela.
                    if click_coordenada in pretas_posicao:
                        peca_preta = pretas_posicao.index(click_coordenada)
                        pecas_capturadas_branco.append(pecas_pretas[peca_preta])
                        if pecas_pretas[peca_preta] == 'rei':
                            pygame.quit()
                        pecas_pretas.pop(peca_preta)
                        pretas_posicao.pop(peca_preta)
                    # Atualiza as opções de jogadas de ambos os times e inicia o turno do preto.
                    pretas_opcoes = check_opcoes(pecas_pretas, pretas_posicao, 'pretos')
                    brancas_opcoes = check_opcoes(pecas_brancas, brancas_posicao, 'brancos')
                    turno = 2
                    selecionado = 50
                    movimentos_validos = []

            if turno > 1:

                if click_coordenada in pretas_posicao:
                    selecionado = pretas_posicao.index(click_coordenada)
                    movimentos_validos = check_movimentos_validos()
                    if turno == 2:
                        turno = 3
                if click_coordenada in movimentos_validos and selecionado != 50:
                    pretas_posicao[selecionado] = click_coordenada
                    if click_coordenada in brancas_posicao:
                        peca_branca = brancas_posicao.index(click_coordenada)
                        pecas_capturadas_preto.append(pecas_brancas[peca_branca])
                        if pecas_brancas[peca_branca] == 'rei':
                            pygame.quit()
                        pecas_brancas.pop(peca_branca)
                        brancas_posicao.pop(peca_branca)

                    pretas_opcoes = check_opcoes(pecas_pretas, pretas_posicao, 'pretos')
                    brancas_opcoes = check_opcoes(pecas_brancas, brancas_posicao, 'brancos')
                    turno = 0

                    selecionado = 50
                    movimentos_validos = []
    pygame.display.update()

pygame.quit()
