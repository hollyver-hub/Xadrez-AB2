import pygame
from pygame import MOUSEBUTTONDOWN
import random
import time

# Inicialização

pygame.init()
pygame.mixer.init()
pygame.font.init()
from assets import *

# Função que desenha o/ou tabuleiro

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

def desenha_validos(movimentos):
    for i in range(len(movimentos)):
        pygame.draw.circle(screen, 'red', (movimentos[i][0] * 60 + 30, movimentos[i][1] * 60 + 30), 5)

def desenha_cheque():
    global cheque
    cheque = False

    if 'rei' in pecas_brancas:
        rei_index = pecas_brancas.index('rei')
        rei_posicao = brancas_posicao[rei_index]
        for i in range(len(pretas_posicao)):
            movimentos_inimigo = check_opcoes_movimento([pecas_pretas[i]], [pretas_posicao[i]], 'pretos', brancas_posicao, pretas_posicao)[0]
            if rei_posicao in movimentos_inimigo:
                cheque = True
                if counter < 15:
                    pygame.draw.rect(screen, 'dark red', [rei_posicao[0] * 60, rei_posicao[1] * 60, 60, 60], 5)

    if 'rei' in pecas_pretas:
        rei_index = pecas_pretas.index('rei')
        rei_posicao = pretas_posicao[rei_index]
        for i in range(len(brancas_posicao)):
            movimentos_inimigo = check_opcoes_movimento([pecas_brancas[i]], [brancas_posicao[i]], 'brancos', brancas_posicao, pretas_posicao)[0]
            if rei_posicao in movimentos_inimigo:
                cheque = True
                if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [rei_posicao[0] * 60, rei_posicao[1] * 60, 60, 60], 5)

def desenha_game_over():
    screen.fill('black')
    screen.blit(game_over_title_text, game_over_title_text_rect)

    if restart_button_rect.collidepoint(mouse_pos):
        screen.blit(restart_button_grande, restart_button_rect_grande)
    else:
        screen.blit(restart_button, restart_button_rect)

def desenha_promocao():
    if brancas_promocao:
        cor = 'branco'
        pygame.draw.rect(screen, 'black', [0, 190, 480, 100])
        pygame.display.set_caption('Branco, faça a promoção desejada')
        for i in range(len(brancas_promocoes)):
            peca = brancas_promocoes[i]
            index = todas_pecas.index(peca)
            screen.blit(imagens_pecas_brancas[index], [60 + 100 * i, 220])
            screen.blit(promocao_text_branco, promocao_text_rect_branco)
    elif pretas_promocao:
        cor = 'preto'
        pygame.draw.rect(screen, 'white', [0, 190, 480, 100])
        pygame.display.set_caption('Preto, faça a promoção desejada')
        for i in range(len(pretas_promocoes)):
            peca = pretas_promocoes[i]
            index = todas_pecas.index(peca)
            screen.blit(imagens_pecas_pretas[index], [60 + 100 * i, 220])
            screen.blit(promocao_text_preto, promocao_text_rect_preto)

def desenha_credits():
    screen.fill('black')


#Movimentação

def check_movimentos_validos():
    if turno < 2:
        opcoes_lista = brancas_opcoes
    else:
        opcoes_lista = pretas_opcoes
    opcoes_validas = opcoes_lista[selecionado]

    return opcoes_validas

def check_opcoes_movimento(pecas, posicao, turno, brancas_posicao, pretas_posicao):
    global movimentos_castling
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
            lista_movimentos, movimentos_castling = check_rei(localizacao, turno, brancas_posicao, pretas_posicao)

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
                (posicao[0], posicao[1] - 2) not in pretas_posicao and posicao[1] == 6) and ((posicao[0], posicao[1] - 1) not in brancas_posicao and ((posicao[0], posicao[1] - 1) not in pretas_posicao)):
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
                posicao[0], posicao[1] + 2) not in pretas_posicao and posicao[1] == 1 and ((posicao[0], posicao[1] + 1) not in brancas_posicao and ((posicao[0], posicao[1] + 1) not in pretas_posicao)):
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
    movimentos_castling = check_castling()
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

    return movimentos_lista, movimentos_castling

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

def check_movimentos_validos_ia(peca, posicao):
    movimentos_validos = check_opcoes_movimento([peca], [posicao], 'pretos', brancas_posicao, pretas_posicao)
    return movimentos_validos

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

#Castling

def check_castling():
    movimentos_castling = []
    indexes_torre = []
    localizacao_torre = []
    index_rei = 0
    localizacao_rei = (0, 0)

    if turno <= 1:
        for i in range(len(pecas_brancas)):
            if pecas_brancas[i] == 'torre':
                indexes_torre.append(pecas_movidas_branco[i])
                localizacao_torre.append(brancas_posicao[i])
            if pecas_brancas[i] == 'rei':
                index_rei = i
                localizacao_rei = brancas_posicao[i]

        if not pecas_movidas_branco[index_rei] and False in indexes_torre and not cheque:
            for i in range(len(indexes_torre)):
                castle = True
                if localizacao_torre[i][0] > localizacao_rei[0]:
                    espacos_vazios = [(localizacao_rei[0] + 1, localizacao_rei[1]),
                                      (localizacao_rei[0] + 2, localizacao_rei[1])]

                else:
                    espacos_vazios = [(localizacao_rei[0] - 1, localizacao_rei[1]),
                                      (localizacao_rei[0] - 2, localizacao_rei[1]),
                                      (localizacao_rei[0] - 3, localizacao_rei[1])]

                for j in range(len(espacos_vazios)):
                    if espacos_vazios[j] in brancas_posicao or espacos_vazios[j] in pretas_posicao or \
                            espacos_vazios[j] in pretas_opcoes or indexes_torre[i]:
                        castle = False
                if castle:
                    movimentos_castling.append((espacos_vazios[1], espacos_vazios[0]))
    else:
        for i in range(len(pecas_pretas)):
            if pecas_pretas[i] == 'torre':
                indexes_torre.append(pecas_movidas_preto[i])
                localizacao_torre.append(pretas_posicao[i])
            if pecas_pretas[i] == 'rei':
                index_rei = i
                localizacao_rei = pretas_posicao[i]

        if not pecas_movidas_preto[index_rei] and False in indexes_torre and not cheque:
            for i in range(len(indexes_torre)):
                castle = True
                if localizacao_torre[i][0] > localizacao_rei[0]:
                    espacos_vazios = [(localizacao_rei[0] + 1, localizacao_rei[1]),
                                      (localizacao_rei[0] + 2, localizacao_rei[1])]
                else:
                    espacos_vazios = [(localizacao_rei[0] - 1, localizacao_rei[1]),
                                      (localizacao_rei[0] - 2, localizacao_rei[1]),
                                      (localizacao_rei[0] - 3, localizacao_rei[1])]
                for j in range(len(espacos_vazios)):
                    if espacos_vazios[j] in brancas_posicao or espacos_vazios[j] in pretas_posicao or \
                            espacos_vazios[j] in brancas_opcoes or indexes_torre[i]:
                        castle = False
                if castle:
                    movimentos_castling.append((espacos_vazios[1], espacos_vazios[0]))
    return movimentos_castling

def desenha_castling(movimentos):
    cor = 'blue'
    for i in range(len(movimentos)):
        pygame.draw.circle(screen, cor, (movimentos[i][0][0] * 60 + 30, movimentos[i][0][1] * 60 + 30), 5)

# Promoções do peão

def check_promocao():
    peao_indexes = []
    brancas_promocao = False
    pretas_promocao = False
    promocao_index = 100
    for i in range(len(pecas_brancas)):
        if pecas_brancas[i] == 'peao':
            peao_indexes.append(i)
    for i in range(len(peao_indexes)):
        if brancas_posicao[peao_indexes[i]][1] == 0:
            brancas_promocao = True
            promocao_index = peao_indexes[i]

    peao_indexes = []

    for i in range(len(pecas_pretas)):
        if pecas_pretas[i] == 'peao':
            peao_indexes.append(i)
    for i in range(len(peao_indexes)):
        if pretas_posicao[peao_indexes[i]][1] == 7:
            pretas_promocao = True
            promocao_index = peao_indexes[i]

    return brancas_promocao, pretas_promocao, promocao_index

def check_selecao_promocao():
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100
    if brancas_promocao and click and 0 <= x_pos <= 6 and y_pos == 2:
        pecas_brancas[promocao_index] = brancas_promocoes[x_pos]
    if pretas_promocao and click and 0 <= x_pos <= 6 and y_pos == 2:
        pecas_pretas[promocao_index] = pretas_promocoes[x_pos]

#Função de escolher o modo de jogo

modo = 0
while modo == 0:
    credits_bool = False
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(title, title_rect)

    #Botões Interativos:

    if modo1_rect.collidepoint(mouse_pos):
        screen.blit(modo1_big, modo1_big_rect)
    else:
        screen.blit(modo1, modo1_rect)


    if modo2_rect.collidepoint(mouse_pos):
        screen.blit(modo2_big, modo2_big_rect)
    else:
        screen.blit(modo2, modo2_rect)

    screen.blit(credits, credits_rect)
    screen.blit(credits_names, credits_names_rect)
    screen.blit(credits_names2, credits_names2_rect)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == MOUSEBUTTONDOWN:
            if modo1_rect.collidepoint(mouse_pos):
                modo = 1
            if modo2_rect.collidepoint(mouse_pos):
                modo = 2




        pygame.display.update()

pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos', brancas_posicao, pretas_posicao)
brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos', brancas_posicao, pretas_posicao)
jogando = True
game_over = False


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
    if not game_over:
        brancas_promocao, pretas_promocao, promocao_index = check_promocao()
        if brancas_promocao or pretas_promocao:
            desenha_promocao()
            check_selecao_promocao()
        if selecionado != 50:
            movimentos_validos = check_movimentos_validos()
            desenha_validos(movimentos_validos)
            if peca_selecionada == 'rei':
                desenha_castling(movimentos_castling)
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

                        # Castling
                        peca_selecionada = pecas_brancas[selecionado]

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
                            pecas_movidas_preto.pop(peca_preta)
                            if 'rei' in pecas_capturadas_branco:
                                game_over = True
                                vencedor = 'Branco'

                        if click_coordenada == (pretas_en_passant[0], pretas_en_passant[1]-2):
                            peca_preta = pretas_posicao.index((pretas_en_passant[0], pretas_en_passant[1]-1))
                            pecas_capturadas_branco.append(pecas_pretas[peca_preta])
                            som_eliminado.play()
                            pecas_pretas.pop(peca_preta)
                            pecas_movidas_preto.pop(peca_preta)
                            pretas_posicao.pop(peca_preta)
                            if 'rei' in pecas_capturadas_branco:
                                game_over = True
                                vencedor = 'Branco'

                        # Atualiza as opções de jogadas de ambos os times e inicia o turno do preto.
                        turno = 2
                        pecas_movidas_branco[selecionado] = True
                        selecionado = 50
                        pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos', brancas_posicao,
                                                               pretas_posicao)
                        brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos', brancas_posicao,
                                                                pretas_posicao)
                    #Castling

                    elif selecionado != 50 and peca_selecionada == 'rei':
                        for z in range(len(movimentos_castling)):
                            if click_coordenada == movimentos_castling[z][0]:
                                brancas_posicao[selecionado] = click_coordenada
                                pecas_movidas_branco[selecionado] = True
                                if click_coordenada == (2, 7):
                                    torre_coordenada = (0, 7)
                                else:
                                    torre_coordenada = (7, 7)
                                torre_index = brancas_posicao.index(torre_coordenada)
                                brancas_posicao[torre_index] = movimentos_castling[z][1]
                                turno = 2
                                pecas_movidas_branco[selecionado] = True
                                selecionado = 50
                                pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos', brancas_posicao,
                                                                       pretas_posicao)
                                brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos', brancas_posicao,
                                                                        pretas_posicao)
                                som_movimento.play()

                if modo == 1:
                    # Turno do preto.
                    if turno > 1:
                        pygame.display.set_caption('Turno das Peças Pretas')

                        # Verifica se o click foi em alguma peça preta, se foi checa os movimentos válidos.
                        if click_coordenada in pretas_posicao:
                            selecionado = pretas_posicao.index(click_coordenada)
                            movimentos_validos = check_movimentos_validos()

                            # Castling
                            peca_selecionada = pecas_pretas[selecionado]
                            if turno == 2:
                                turno = 3
                        # Se houver uma peça selecionada, e o click estiver na lista de movimentos válidos, coloca a peça na posição desejada.
                        if click_coordenada in movimentos_validos and selecionado != 50:
                            pretas_en_passant = check_en_passant(pretas_posicao[selecionado], click_coordenada)

                            if pecas_movidas_branco[selecionado] == False:
                                pecas_movidas_branco[selecionado] = True

                            pretas_posicao[selecionado] = click_coordenada
                            if click_coordenada not in brancas_posicao:
                                som_movimento.play()
                            # Se o movimento for válido e o click for em cima de uma peça inimiga, "come" ela.
                            if click_coordenada in brancas_posicao:
                                peca_branca = brancas_posicao.index(click_coordenada)
                                pecas_capturadas_preto.append(pecas_brancas[peca_branca])
                                som_eliminado.play()
                                pecas_brancas.pop(peca_branca)
                                pecas_movidas_branco.pop(peca_branca)
                                brancas_posicao.pop(peca_branca)
                                if 'rei' in pecas_capturadas_preto:
                                    game_over = True
                                    vencedor = 'Preto'
                            if click_coordenada == (brancas_en_passant[0], brancas_en_passant[1]+2):
                                peca_branca = brancas_posicao.index((brancas_en_passant[0], brancas_en_passant[1]+1))
                                pecas_capturadas_preto.append(pecas_brancas[peca_branca])
                                som_eliminado.play()
                                pecas_brancas.pop(peca_branca)
                                pecas_movidas_branco.pop(peca_branca)
                                brancas_posicao.pop(peca_branca)
                                if 'rei' in pecas_capturadas_preto:
                                    game_over = True
                                    vencedor = 'Preto'
                            pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos', brancas_posicao, pretas_posicao)
                            brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos', brancas_posicao, pretas_posicao)
                            turno = 0
                            selecionado = 50
                            movimentos_validos = []

                            # Castling

                        elif selecionado != 50 and peca_selecionada == 'rei':
                            for z in range(len(movimentos_castling)):
                                if click_coordenada == movimentos_castling[z][0]:
                                    pretas_posicao[selecionado] = click_coordenada
                                    pecas_movidas_preto[selecionado] = True
                                    if click_coordenada == (2, 0):
                                        torre_coordenada = (0, 0)
                                    else:
                                        torre_coordenada = (7, 0)
                                    torre_index = pretas_posicao.index(torre_coordenada)
                                    pretas_posicao[torre_index] = movimentos_castling[z][1]
                                    turno = 0
                                    pecas_movidas_preto[selecionado] = True
                                    selecionado = 50
                                    pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos', brancas_posicao,
                                                                           pretas_posicao)
                                    brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos',
                                                                            brancas_posicao,
                                                                            pretas_posicao)
                                    som_movimento.play()
                if modo == 2:
                    if turno > 1:
                        pygame.display.set_caption('IA Pensando...')
                        movimento_feito = False  # Flag para controlar o loop

                        while not movimento_feito:
                            # Seleciona uma peça preta aleatória
                            selecionado = random.choice(range(len(pretas_posicao)))
                            movimentos_validos = check_movimentos_validos_ia(
                                pecas_pretas[selecionado], pretas_posicao[selecionado]
                            )

                            if movimentos_validos and movimentos_validos[0]:  # Verifica se há movimentos válidos
                                # Verifica se pode capturar uma peça branca
                                captura_feita = False
                                for posicao in movimentos_validos[0]:
                                    if posicao in brancas_posicao:
                                        movimento = posicao
                                        captura_feita = True
                                        break

                                # Se nenhuma peça puder ser capturada, escolhe um movimento aleatório
                                if not captura_feita:
                                    movimento = random.choice(
                                        movimentos_validos[0])  # Escolhe aleatoriamente um movimento válido

                                # Move a peça preta
                                pretas_posicao[selecionado] = movimento
                                som_movimento.play()

                                # Verifica se capturou uma peça branca
                                if movimento in brancas_posicao:
                                    peca_branca = brancas_posicao.index(movimento)
                                    pecas_capturadas_preto.append(pecas_brancas[peca_branca])
                                    som_eliminado.play()

                                    # Remove a peça branca capturada
                                    pecas_brancas.pop(peca_branca)
                                    pecas_movidas_branco.pop(peca_branca)
                                    brancas_posicao.pop(peca_branca)

                                    # Verifica se o rei foi capturado
                                    if 'rei' in pecas_capturadas_preto:
                                        game_over = True
                                        vencedor = 'IA'

                                # Finaliza o turno
                                brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos',
                                                                        brancas_posicao, pretas_posicao)
                                turno = 0
                                selecionado = 50
                                movimentos_validos = []
                                movimento_feito = True


                            else:
                                # Se não houver movimentos válidos, tenta novamente
                                continue
    else:
        desenha_game_over()
        pygame.display.set_caption(f'O {vencedor} ganhou!!')
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogando = False
            if event.type == MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(mouse_pos):

                    pecas_capturadas_branco = []
                    pecas_movidas_branco = [False, False, False, False, False, False, False, False,
                                            False, False, False, False, False, False, False, False, ]
                    pecas_capturadas_preto = []
                    pecas_movidas_preto = [False, False, False, False, False, False, False, False,
                                           False, False, False, False, False, False, False, False, ]
                    pecas_pretas = ['torre', 'cavalo', 'bispo', 'rainha', 'rei', 'bispo', 'cavalo', 'torre',
                                    'peao', 'peao', 'peao', 'peao', 'peao', 'peao', 'peao', 'peao']

                    pretas_posicao = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                      (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

                    pecas_brancas = ['torre', 'cavalo', 'bispo', 'rainha', 'rei', 'bispo', 'cavalo', 'torre',
                                     'peao', 'peao', 'peao', 'peao', 'peao', 'peao', 'peao', 'peao']

                    brancas_posicao = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                       (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                    pretas_en_passant = (100, 100)
                    brancas_en_passant = (100, 100)
                    brancas_promocao = False
                    pretas_promocao = False
                    promocao_index = 50
                    movimentos_castling = []
                    cheque = False
                    vencedor = 'null'
                    turno = 0
                    counter = 0
                    selecionado = 50
                    movimentos_validos = []
                    game_over = False
                    pygame.display.set_caption('Xadrez - AB1')
                    pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos',
                                                           brancas_posicao, pretas_posicao)
                    brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos',
                                                            brancas_posicao, pretas_posicao)

        pygame.display.update()

    pygame.display.update()
pygame.quit()
quit()
