import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()


width = 480
height = 480
screen = pygame.display.set_mode((width, height))
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

torre_branca = pygame.image.load('images/rook-w.svg')
torre_branca = pygame.transform.scale(torre_branca, (width_pecas, height_pecas))

cavalo_branco = pygame.image.load('images/knight-w.svg')
cavalo_branco = pygame.transform.scale(cavalo_branco, (width_pecas, height_pecas))

bispo_branco = pygame.image.load('images/bishop-w.svg')
bispo_branco = pygame.transform.scale(bispo_branco, (width_pecas, height_pecas))

rainha_branca = pygame.image.load('images/queen-w.svg')
rainha_branca = pygame.transform.scale(rainha_branca, (width_pecas, height_pecas))

rei_branco = pygame.image.load('images/king-w.svg')
rei_branco = pygame.transform.scale(rei_branco, (width_pecas, height_pecas))

peao_branco = pygame.image.load('images/pawn-w.svg')
peao_branco = pygame.transform.scale(peao_branco, (width_pecas, height_pecas))

imagens_pecas_brancas = [torre_branca, cavalo_branco, bispo_branco, rainha_branca, rei_branco, peao_branco]

brancas_promocoes = ['bispo', 'cavalo', 'torre', 'rainha']

pecas_capturadas_branco = []
pecas_movidas_branco = [False, False, False, False, False, False, False, False,
                        False, False, False, False, False, False, False, False,]

# Peças pretas:

torre_preta = pygame.image.load('images/rook-b.svg')
torre_preta = pygame.transform.scale(torre_preta, (width_pecas, height_pecas))

cavalo_preto = pygame.image.load('images/knight-b.svg')
cavalo_preto = pygame.transform.scale(cavalo_preto, (width_pecas, height_pecas))

bispo_preto = pygame.image.load('images/bishop-b.svg')
bispo_preto = pygame.transform.scale(bispo_preto, (width_pecas, height_pecas))

rainha_preto = pygame.image.load('images/queen-b.svg')
rainha_preto = pygame.transform.scale(rainha_preto, (width_pecas, height_pecas))

rei_preto = pygame.image.load('images/king-b.svg')
rei_preto = pygame.transform.scale(rei_preto, (width_pecas, height_pecas))

peao_preto = pygame.image.load('images/pawn-b.svg')
peao_preto = pygame.transform.scale(peao_preto, (width_pecas, height_pecas))

imagens_pecas_pretas = [torre_preta, cavalo_preto, bispo_preto, rainha_preto, rei_preto, peao_preto]
pretas_promocoes = ['bispo', 'cavalo', 'torre', 'rainha']

pecas_capturadas_preto = []
pecas_movidas_preto = [False, False, False, False, False, False, False, False,
                        False, False, False, False, False, False, False, False,]

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


#Sons

som_movimento = pygame.mixer.Sound("./audios/moviment_sound.mp3")
som_eliminado = pygame.mixer.Sound("./audios/moviment_eliminate.mp3")

#Fontes

fonte_normal = pygame.font.Font("./fonts/Ubuntu-Regular.ttf", 20)
fonte_negrito = pygame.font.Font("./fonts/Ubuntu-Regular.ttf", 20)
fonte_negrito_grande = pygame.font.Font("./fonts/Ubuntu-Regular.ttf", 23)

doto_extra_bold = pygame.font.Font("./fonts/Doto/Doto-ExtraBold.ttf", 50)
doto_regular = pygame.font.Font("./fonts/Doto/Doto-Regular.ttf", 25)
doto_regular_big = pygame.font.Font("./fonts/Doto/Doto-Regular.ttf", 30)

#Textos

title = doto_extra_bold.render('Chess Game AB2', True, (255, 255, 255), (0, 0, 0))
title_rect = title.get_rect()
title_rect.center = (width // 2, 100)

#Player vs Player

modo1 = doto_regular.render("Player vs Player", True, (255, 255, 255), (0, 0, 0))
modo1_rect = modo1.get_rect()
modo1_rect.center = (width // 2, 250)

modo1_big = doto_regular_big.render("Player vs Player", True, (255, 255, 255), (0, 0, 0))
modo1_big_rect = modo1_big.get_rect()
modo1_big_rect.center = (width // 2, 250)

#IA

modo2 = doto_regular.render("Player vs IA", True, (255, 255, 255), (0, 0, 0))
modo2_rect = modo2.get_rect()
modo2_rect.center = (width // 2, 300)

modo2_big = doto_regular_big.render("Player vs IA", True, (255, 255, 255), (0, 0, 0))
modo2_big_rect = modo2_big.get_rect()
modo2_big_rect.center = (width // 2, 300)

#Creditos

credits = doto_regular.render("Créditos", True, (255, 255, 255), (0, 0, 0))
credits_rect = credits.get_rect()
credits_rect.center = (width // 2, 400)

credits_big = doto_regular_big.render("Créditos", True, (255, 255, 255), (0, 0, 0))
credits_big_rect = credits_big.get_rect()
credits_big_rect.center = (width // 2, 400)

#Promoção

promocao_text_branco = fonte_negrito.render('Promoção de Peão', True, (255, 255, 255), (0, 0, 0))
promocao_text_rect_branco = promocao_text_branco.get_rect()
promocao_text_rect_branco.center = (width // 2, 205)

promocao_text_preto = fonte_negrito.render('Promoção de Peão', True, (0, 0, 0), (255, 255, 255))
promocao_text_rect_preto = promocao_text_preto.get_rect()
promocao_text_rect_preto.center = (width // 2, 205)

game_over_title_text = fonte_negrito_grande.render('Deseja jogar novamente?', True, (255, 255, 255), (0, 0, 0))
game_over_title_text_rect = game_over_title_text.get_rect()
game_over_title_text_rect.center = (width // 2, height - 400)

restart_button = fonte_negrito.render("Restart", True, (255, 255, 255), (0, 0, 0))
restart_button_rect = restart_button.get_rect()
restart_button_rect.center = (width // 2, height - 205)

restart_button_grande = fonte_negrito_grande.render("Restart", True, (255, 255, 255), (0, 0, 0))
restart_button_rect_grande = restart_button_grande.get_rect()
restart_button_rect_grande.center = (width // 2, height - 205)

#Inicializando

pretas_en_passant = (100, 100)
brancas_en_passant = (100, 100)
brancas_promocao = False
pretas_promocao = False
promocao_index = 50
movimentos_castling = []
cheque = False
credits_bool = False
vencedor = 'null'
