import pygame
import random
import sys

# Iniciando o pygame e criando a tela do jogo
pygame.init()

pygame.display.set_caption("Snake Game")
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Definindo as cores
preto = (0, 0, 0)
branca = (255, 255,255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)

# Parâmetros da cobra
tamanho_quadrado = 20
velocidade_jogo = 15

# Variável de recorde pessoal
recorde_pessoal = 0

# Funções para rodar o jogo
def gerar_comida(pixels, ilimitado):
    if ilimitado:
        comida_x = round(random.randrange(0, largura - tamanho_quadrado) // tamanho_quadrado) * tamanho_quadrado
        comida_y = round(random.randrange(0, altura - tamanho_quadrado) // tamanho_quadrado) * tamanho_quadrado
    else:
        comida_x = round(random.randrange(1, (largura - tamanho_quadrado - 1) // tamanho_quadrado)) * tamanho_quadrado
        comida_y = round(random.randrange(1, (altura - tamanho_quadrado - 1) // tamanho_quadrado)) * tamanho_quadrado
    if [comida_x, comida_y] not in pixels:
        return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao, recorde):
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, vermelho)
    tela.blit(texto_pontuacao, [1, 1])

def selecionar_velocidade(tecla, velocidade_x, velocidade_y, direcao_atual):
    if tecla == pygame.K_DOWN and direcao_atual != 'up':
        return 0, tamanho_quadrado, 'down'
    elif tecla == pygame.K_UP and direcao_atual != 'down':
        return 0, -tamanho_quadrado, 'up'
    elif tecla == pygame.K_RIGHT and direcao_atual != 'left':
        return tamanho_quadrado, 0, 'right'
    elif tecla == pygame.K_LEFT and direcao_atual != 'right':
        return -tamanho_quadrado, 0, 'left'
    return velocidade_x, velocidade_y, direcao_atual

def colisao_corpo(x, y, pixels):
    for pixel in pixels[:-1]:
        if pixel == [x, y]:
            return True
    return False

def tela_perdeu(pontuacao, recorde):
    tela.fill(preto)
    fonte = pygame.font.SysFont("Helvetica", 50)
    texto_perdeu = fonte.render("Você Perdeu!", True, vermelho)
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, branca)
    texto_recorde = fonte.render(f"Recorde Pessoal: {recorde}", True, branca)
    texto_instrucao = fonte.render("Pressione 'M' para voltar ao Menu Inicial ou 'Esc' para sair", True, branca)

    largura_texto = max(texto_perdeu.get_width(), texto_pontuacao.get_width(), texto_recorde.get_width(), texto_instrucao.get_width())
    pos_x = (largura - largura_texto) // 2
    pos_y_perdeu = (altura // 2) - 50
    pos_y_pontuacao = (altura // 2)
    pos_y_recorde = (altura // 2) + 50
    pos_y_instrucao = (altura // 2) + 100

    tela.blit(texto_perdeu, [pos_x, pos_y_perdeu])
    tela.blit(texto_pontuacao, [pos_x, pos_y_pontuacao])
    tela.blit(texto_recorde, [pos_x, pos_y_recorde])
    tela.blit(texto_instrucao, [pos_x, pos_y_instrucao])
    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m:
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    

def rodar_jogo(recorde_pessoal, ilimitado):
    fim_jogo = False
    x = largura // 2
    y = altura // 2
    velocidade_x = 0
    velocidade_y = 0
    direcao_atual = 'right'
    tamanho_cobra = 1
    pixels = []
    comida_x, comida_y = gerar_comida(pixels, ilimitado)
    
    while not fim_jogo:
        tela.fill(preto)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y, direcao_atual = selecionar_velocidade(evento.key, velocidade_x, velocidade_y, direcao_atual)

        # Desenhar comida
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)

        # Atualizar a posição da cobra
        x += velocidade_x
        y += velocidade_y

        # Verificar colisão com a parede
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True

        # Verificar colisão com o corpo da cobra
        if colisao_corpo(x, y, pixels):
            fim_jogo = True

        # Desenhar a cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            pixels.pop(0)

        desenhar_cobra(tamanho_quadrado, pixels)

        # Desenhar pontos
        desenhar_pontuacao(tamanho_cobra - 1, recorde_pessoal)

        # Atualização da tela
        pygame.display.update()

        # Verificar se a cobra comeu a comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida(pixels, ilimitado)

        relogio.tick(velocidade_jogo)

    if tamanho_cobra - 1 > recorde_pessoal:
        recorde_pessoal = tamanho_cobra - 1

    tela_perdeu(tamanho_cobra - 1, recorde_pessoal)

def menu_inicial(recorde_pessoal):
    tela.fill(preto)
    fonte = pygame.font.SysFont("Helvetica", 50)
    texto_titulo = fonte.render("Snake Game", True, vermelho)
    texto_opcoes = fonte.render("Selecione uma opção:", True, branca)
    texto_ilimitado = fonte.render("1 - Modo Ilimitado", True, branca)
    texto_limitado = fonte.render("2 - Modo Limitado", True, branca)
    
    largura_texto = max(texto_titulo.get_width(), texto_opcoes.get_width(), texto_ilimitado.get_width(), texto_limitado.get_width())
    pos_x = largura // 2 - largura_texto // 2

    tela.blit(texto_titulo, [pos_x, altura // 2 - 100])
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

modo_selecionado = menu_inicial(recorde_pessoal)
while True:
    if modo_selecionado == '1':
        recorde_pessoal = rodar_jogo(recorde_pessoal, True)
    elif modo_selecionado == '2':
        recorde_pessoal = rodar_jogo(recorde_pessoal, False)
    modo_selecionado = menu_inicial(recorde_pessoal)
