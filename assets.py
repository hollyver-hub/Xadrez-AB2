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

pecas_capturadas_branco = []

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


#Sons

som_movimento = pygame.mixer.Sound("./audios/moviment_sound.mp3")
som_eliminado = pygame.mixer.Sound("./audios/moviment_eliminate.mp3")

#Fontes

fonte_normal = pygame.font.Font("./fonts/Ubuntu-Regular.ttf", 20)
fonte_negrito = pygame.font.Font("./fonts/Ubuntu-Regular.ttf", 20)
