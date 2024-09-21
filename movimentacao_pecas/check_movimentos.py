from movimentacao_pecas.rei_movimentos import check_rei
from movimentacao_pecas.torre_movimentos import check_torre
from movimentacao_pecas.cavalo_movimentos import check_cavalo
from movimentacao_pecas.bispo_movimentos import check_bispo
from movimentacao_pecas.peao_movimentos import check_peao

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