# Importando bibliotecas necessárias para o menu inicial
import main
import pygame
import sys

# Iniciando o PyGame
pygame.init()

# Criando Tela do Game
pygame.display.set_caption("Snake Game")
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Definindo as cores que irei utilizar no projeto
preto = (0, 0, 0)
branca = (255, 255,255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)

# Função condicional para o usuário escolher a dificuldade do jogo
def menu_inicial(recorde_pessoal):
    # Chama a tela preta inicial
    tela.fill(preto)

    # Define a fonte das letras do jogo
    fonte = pygame.font.SysFont("Helvetica", 50)
    fonte_recorde = pygame.font.SysFont("Helvetica", 20)
    texto_titulo = fonte.render("Snake Game", True, vermelho)
    texto_recorde = fonte_recorde.render(f"Recorde pessoal: {recorde_pessoal}", True, branca)
    texto_opcoes = fonte.render("Selecione um modo:", True, branca)
    texto_ilimitado = fonte.render("1 - Modo Ilimitado", True, branca)
    texto_limitado = fonte.render("2 - Modo Limitado", True, branca)
    
    # Define a Largura do texto
    largura_texto = max(texto_titulo.get_width(), texto_opcoes.get_width(), texto_ilimitado.get_width(), texto_limitado.get_width())
    pos_x = largura // 2 - largura_texto // 2

    # Abaixo só é usado na variavel de recorde
    pos_xy = largura - texto_recorde.get_width() - 10
    pos_y = 10

    # Define a posição das palavras
    tela.blit(texto_titulo, [pos_x, 30])
    tela.blit(texto_recorde, [pos_xy, pos_y])
    tela.blit(texto_opcoes, [pos_x, altura // 2 - 30])
    tela.blit(texto_ilimitado, [pos_x, altura // 2 + 30])
    tela.blit(texto_limitado, [pos_x, altura // 2 + 70])
    pygame.display.update()
    
    opcao_selecionada = None
    while opcao_selecionada not in ('1', '2'):
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.unicode in ('1', '2'):
                    opcao_selecionada = evento.unicode
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
    return opcao_selecionada

recorde_pessoal = 0  # Inicialize o recorde pessoal como 0
modo_selecionado = menu_inicial(recorde_pessoal)
while True:
    if modo_selecionado == '1':
        recorde_pessoal = main.rodar_jogo(recorde_pessoal, True)
    elif modo_selecionado == '2':
        recorde_pessoal = main.rodar_jogo(recorde_pessoal, False)
    modo_selecionado = menu_inicial(recorde_pessoal)

if __name__ == __main__:
    menu_inicial()