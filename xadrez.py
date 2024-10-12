import pygame
from movimentacao_pecas.check_movimentos import check_opcoes_movimento

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
                        if pecas_pretas[peca_preta] == 'rei':
                            desenha_game_over()
                    # Atualiza as opções de jogadas de ambos os times e inicia o turno do preto.
                    pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos', brancas_posicao, pretas_posicao)
                    brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos', brancas_posicao, pretas_posicao)
                    turno = 2
                    selecionado = 50
                    movimentos_validos = []

            if turno > 1:
                pygame.display.set_caption('Turno das Peças Pretas')

                if click_coordenada in pretas_posicao:
                    selecionado = pretas_posicao.index(click_coordenada)
                    movimentos_validos = check_movimentos_validos()
                    if turno == 2:
                        turno = 3
                if click_coordenada in movimentos_validos and selecionado != 50:
                    pretas_posicao[selecionado] = click_coordenada
                    if click_coordenada not in brancas_posicao:
                        som_movimento.play()
                    if click_coordenada in brancas_posicao:
                        peca_branca = brancas_posicao.index(click_coordenada)
                        pecas_capturadas_preto.append(pecas_brancas[peca_branca])
                        som_eliminado.play()
                        if pecas_brancas[peca_branca] == 'rei':
                            pygame.quit()
                        pecas_brancas.pop(peca_branca)
                        brancas_posicao.pop(peca_branca)

                    pretas_opcoes = check_opcoes_movimento(pecas_pretas, pretas_posicao, 'pretos', brancas_posicao, pretas_posicao)
                    brancas_opcoes = check_opcoes_movimento(pecas_brancas, brancas_posicao, 'brancos', brancas_posicao, pretas_posicao)
                    turno = 0

                    selecionado = 50
                    movimentos_validos = []
    pygame.display.update()

pygame.quit()
