import pygame
from pygame import MOUSEBUTTONDOWN
import random
import time

# Inicialização

pygame.init()
pygame.mixer.init()
pygame.font.init()
from assets import *


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

    if 'rei' in pecas_brancas:
        rei_index = pecas_brancas.index('rei')
        rei_posicao = brancas_posicao[rei_index]
        for i in range(len(pretas_posicao)):
            movimentos_inimigo = check_opcoes_movimento([pecas_pretas[i]], [pretas_posicao[i]], 'pretos', brancas_posicao, pretas_posicao)[0]
            if rei_posicao in movimentos_inimigo:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [rei_posicao[0] * 60, rei_posicao[1] * 60, 60, 60], 5)

    if 'rei' in pecas_pretas:
        rei_index = pecas_pretas.index('rei')
        rei_posicao = pretas_posicao[rei_index]
        for i in range(len(brancas_posicao)):
            movimentos_inimigo = check_opcoes_movimento([pecas_brancas[i]], [brancas_posicao[i]], 'brancos', brancas_posicao, pretas_posicao)[0]
            if rei_posicao in movimentos_inimigo:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [rei_posicao[0] * 60, rei_posicao[1] * 60, 60, 60], 5)

def desenha_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 50])

def check_movimentos_validos_ia(peca, posicao):
    movimentos_validos = check_opcoes_movimento([peca], [posicao], 'pretos', brancas_posicao, pretas_posicao)
    return movimentos_validos

#Movimentação

def check_opcoes_movimento(pecas, posicao, turno, brancas_posicao, pretas_posicao):
    lista_movimentos = []
    todos_os_movimentos = []

    for i in range(len(pecas)):
        localizacao = posicao[i]
        peca = pecas[i]
        if peca == 'peao':
            lista_movimentos = check_peao(localizacao, turno, brancas_posicao, pretas_posicao)

        if peca == 'torre':
            lista_movimentos = check_torre(localizacao, turno, brancas_posicao, pretas_posicao)

        if peca == 'cavalo':
            lista_movimentos = check_cavalo(localizacao, turno, brancas_posicao, pretas_posicao)

        if peca == 'bispo':
            lista_movimentos = check_bispo(localizacao, turno, brancas_posicao, pretas_posicao)

        if peca == 'rainha':
            lista_movimentos = check_bispo(localizacao, turno, brancas_posicao, pretas_posicao) + check_torre(localizacao, turno, brancas_posicao, pretas_posicao)

        if peca == 'rei':
            lista_movimentos = check_rei(localizacao, turno, brancas_posicao, pretas_posicao)

        todos_os_movimentos.append(lista_movimentos)

    return todos_os_movimentos

def check_bispo(posicao, cor, brancas_posicao, pretas_posicao):
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

def check_peao(posicao, cor, brancas_posicao, pretas_posicao):
    movimentos_lista = []
    if cor == 'brancos':

        # Movimento normal do peao:

        if ((posicao[0], posicao[1] - 1) not in brancas_posicao and
                (posicao[0], posicao[1] - 1) not in pretas_posicao and posicao[1] > 0):
            movimentos_lista.append((posicao[0], posicao[1] - 1))

        # Movimento de duas casas somente quando estiver na posição inicial:

        if ((posicao[0], posicao[1] - 2) not in brancas_posicao and
                (posicao[0], posicao[1] - 2) not in pretas_posicao and posicao[1] == 6):
            movimentos_lista.append((posicao[0], posicao[1] - 2))

        # Movimento de captura de peça para a diagonal esquerda:

        if (posicao[0] - 1, posicao[1] - 1) in pretas_posicao:
            movimentos_lista.append((posicao[0] - 1, posicao[1] - 1))

        # Movimento de captura de peça para a diagonal direita:

        if (posicao[0] + 1, posicao[1] - 1) in pretas_posicao:
            movimentos_lista.append((posicao[0] + 1, posicao[1] - 1))

        # Movimento de captura de peça para a diagonal esquerda(en passant):

        if (posicao[0] - 1, posicao[1] + 1) == pretas_en_passant:
            movimentos_lista.append((posicao[0] - 1, posicao[1] - 1))

        # Movimento de captura de peça para a diagonal direita(en passant):

        if (posicao[0] + 1, posicao[1] + 1) == pretas_en_passant:
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

        # Movimento de captura de peça para a diagonal esquerda(en passant):

        if (posicao[0] - 1, posicao[1] - 1) == brancas_en_passant:
            movimentos_lista.append((posicao[0] - 1, posicao[1] + 1))

        # Movimento de captura de peça para a diagonal direita(en passant):

        if (posicao[0] + 1, posicao[1] - 1) == brancas_en_passant:
            movimentos_lista.append((posicao[0] + 1, posicao[1] + 1))



    return movimentos_lista

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


#en passant
def check_en_passant(coord_antigas, coord_novas):
    if turno <= 1:
        index = brancas_posicao.index(coord_antigas)
        en_passant_coord = (coord_novas[0], coord_novas[1] - 1)
        peca = pecas_brancas[index]
    else:
        index = pretas_posicao.index(coord_antigas)
        en_passant_coord = (coord_novas[0], coord_novas[1] + 1)
        peca = pecas_pretas[index]
    if peca == 'peao' and abs(coord_antigas[1] - coord_novas[1]) > 1:
        pass
    else:
        en_passant_coord = (100, 100)
    return en_passant_coord

# Carregando textos

modo1_text = fonte_negrito.render('Player vs Player', True, (255, 255, 255), (20, 20, 20))
modo1_text_rect = modo1_text.get_rect()
modo1_text_rect.center = (width // 2, height - 300)

modo2_text = fonte_negrito.render('Player vs IA(desenvolvimento)', True, (255, 255, 255), (20, 20, 20))
modo2_text_rect = modo2_text.get_rect()
modo2_text_rect.center = (width // 2, height - 200)


#Função de escolher o modo de jogo

modo = 0
while modo == 0:
    screen.fill((0, 0, 0))

    mouse_pos = pygame.mouse.get_pos()

    if modo1_text_rect.collidepoint(mouse_pos):
        modo1_text = fonte_negrito_grande.render('Player vs Player', True, (255, 255, 255), (20, 20, 20))
        modo1_text_rect = modo1_text.get_rect()
        modo1_text_rect.center = (width // 2, height - 300)
    else:
        modo1_text = fonte_negrito.render('Player vs Player', True, (255, 255, 255), (20, 20, 20))
        modo1_text_rect = modo1_text.get_rect()
        modo1_text_rect.center = (width // 2, height - 300)

    if modo2_text_rect.collidepoint(mouse_pos):
        modo2_text = fonte_negrito_grande.render('Player vs IA(desenvolvimento)', True, (255, 255, 255), (20, 20, 20))
        modo2_text_rect = modo2_text.get_rect()
        modo2_text_rect.center = (width // 2, height - 200)
    else:
        modo2_text = fonte_negrito.render('Player vs IA(desenvolvimento)', True, (255, 255, 255), (20, 20, 20))
        modo2_text_rect = modo2_text.get_rect()
        modo2_text_rect.center = (width // 2, height - 200)

    screen.blit(modo1_text, modo1_text_rect)
    screen.blit(modo2_text, modo2_text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == MOUSEBUTTONDOWN:
            if modo1_text_rect.collidepoint(mouse_pos):
                modo = 1
            if modo2_text_rect.collidepoint(mouse_pos):
                modo = 2

        pygame.display.update()

pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos', brancas_posicao, pretas_posicao)
brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos', brancas_posicao, pretas_posicao)
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
        if turno == 0:
            pygame.display.set_caption('Turno das Peças Brancas')
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
                    brancas_en_passant = check_en_passant(brancas_posicao[selecionado], click_coordenada)
                    brancas_posicao[selecionado] = click_coordenada
                    if click_coordenada not in pretas_posicao:
                        som_movimento.play()

                    #Se o movimento for válido e o click for em cima de uma peça inimiga, "come" ela.
                    if click_coordenada in pretas_posicao:
                        peca_preta = pretas_posicao.index(click_coordenada)
                        pecas_capturadas_branco.append(pecas_pretas[peca_preta])
                        som_eliminado.play()
                        pecas_pretas.pop(peca_preta)
                        pretas_posicao.pop(peca_preta)
                        if 'rei' in pecas_capturadas_branco:
                            pygame.quit()
                            jogando = False
                    if click_coordenada == (pretas_en_passant[0], pretas_en_passant[1]-2):
                        peca_preta = pretas_posicao.index((pretas_en_passant[0], pretas_en_passant[1]-1))
                        pecas_capturadas_branco.append(pecas_pretas[peca_preta])
                        som_eliminado.play()
                        pecas_pretas.pop(peca_preta)
                        pretas_posicao.pop(peca_preta)
                        if 'rei' in pecas_capturadas_branco:
                            pygame.quit()
                            jogando = False
                    # Atualiza as opções de jogadas de ambos os times e inicia o turno do preto.

                    turno = 2
                    selecionado = 50
                    pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos', brancas_posicao,
                                                           pretas_posicao)
                    brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos', brancas_posicao,
                                                            pretas_posicao)
            if modo == 1:
                # Turno do preto.
                if turno > 1:
                    pygame.display.set_caption('Turno das Peças Pretas')

                    # Verifica se o click foi em alguma peça preta, se foi checa os movimentos válidos.
                    if click_coordenada in pretas_posicao:
                        selecionado = pretas_posicao.index(click_coordenada)
                        movimentos_validos = check_movimentos_validos()
                        if turno == 2:
                            turno = 3
                    # Se houver uma peça selecionada, e o click estiver na lista de movimentos válidos, coloca a peça na posição desejada.
                    if click_coordenada in movimentos_validos and selecionado != 50:
                        pretas_en_passant = check_en_passant(pretas_posicao[selecionado], click_coordenada)

                        pretas_posicao[selecionado] = click_coordenada
                        if click_coordenada not in brancas_posicao:
                            som_movimento.play()
                        # Se o movimento for válido e o click for em cima de uma peça inimiga, "come" ela.
                        if click_coordenada in brancas_posicao:
                            peca_branca = brancas_posicao.index(click_coordenada)
                            pecas_capturadas_preto.append(pecas_brancas[peca_branca])
                            som_eliminado.play()
                            pecas_brancas.pop(peca_branca)
                            brancas_posicao.pop(peca_branca)
                            if 'rei' in pecas_capturadas_preto:
                                jogando = False
                                pygame.quit()
                        if click_coordenada == (brancas_en_passant[0], brancas_en_passant[1]+2):
                            peca_branca = brancas_posicao.index((brancas_en_passant[0], brancas_en_passant[1]+1))
                            pecas_capturadas_preto.append(pecas_brancas[peca_branca])
                            som_eliminado.play()
                            pecas_brancas.pop(peca_branca)
                            brancas_posicao.pop(peca_branca)
                            if 'rei' in pecas_capturadas_preto:
                                jogando = False
                                pygame.quit()

                        pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos', brancas_posicao, pretas_posicao)
                        brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos', brancas_posicao, pretas_posicao)
                        turno = 0
                        selecionado = 50
                        movimentos_validos = []
            if modo == 2:
                if turno > 1:
                    pygame.display.set_caption('IA Pensando...')
                    while True:
                        selecionado = random.choice(range(len(pretas_posicao)))
                        movimentos_validos = check_movimentos_validos_ia(pecas_pretas[selecionado],
                                                                         pretas_posicao[selecionado])
                        if movimentos_validos:
                            break

                    try:
                        movimento = random.choice(movimentos_validos[0])
                        pretas_posicao[selecionado] = movimento
                        som_movimento.play()
                        for posicao in brancas_posicao:
                            if movimento == posicao:
                                peca_branca = brancas_posicao.index(posicao)
                                pecas_capturadas_preto.append(pecas_brancas[peca_branca])
                                som_eliminado.play()
                                pecas_brancas.pop(peca_branca)
                                brancas_posicao.pop(peca_branca)
                                if 'rei' in pecas_capturadas_preto:
                                    pygame.quit()
                                    jogando = False

                            turno = 0
                            selecionado = 50
                            movimentos_validos = []

                            pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos',
                                                                   brancas_posicao, pretas_posicao)
                            brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos',
                                                                    brancas_posicao, pretas_posicao)

                    except IndexError:
                        pass;

    pygame.display.update()
    print(pretas_en_passant, brancas_en_passant)
pygame.quit()
quit()
