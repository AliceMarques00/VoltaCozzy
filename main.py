import pygame 
import random 
 
pygame.init()  

#janela
x = 1280  # Largura 
y = 720   # Altura 

screen = pygame.display.set_mode((x, y))  # Cria a janela com o tamanho definido
pygame.display.set_caption("Volta cozzi!")  # Define o título da janela do jogo

# Fundo
bg = pygame.image.load('ima/rural.png').convert_alpha()  # Carrega a imagem de fundo com transparência
bg = pygame.transform.scale(bg, (x, y))  # Redimensiona a imagem para caber na janela

# Carregando imagens dos personagens (com erro nos caminhos que precisam ser preenchidos corretamente)
cuscuz = pygame.image.load('ima/cuscuz.png').convert_alpha() 
cuscuz = pygame.transform.scale(cuscuz,(50, 50))  

playerImg = pygame.image.load('ima/hely.png').convert_alpha()  
playerImg = pygame.transform.scale(playerImg, (150, 150))  # Redimensiona o player para 50x50
playerImg = pygame.transform.rotate(playerImg, 360)  # Rotaciona o player 


bala= pygame.image.load('ima/bala.png').convert_alpha()
bala =pygame.transform.scale(bala,( 50, 50))
bala= pygame.transform.rotate(bala,360)

game_over_img = pygame.image.load('ima/gameover.png').convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (x, y))  # Ajusta ao tamanho da janela

# Posições iniciais dos personagens
pos_cuscuz_x = 500  # horizontal
pos_cuscuz_y = 360  # vertical

pos_player_x = 200  # ''''
pos_player_y = 300  # ''''

vel_x_bala=0
pos_bala_x= 200   #
pos_bala_y= 300  #


triggered= False
pontos= 1
rodando = True  # Controle do loop

font = pygame.font.SysFont('fonts/PixelGameFont.ttf', 50)

player_rect = playerImg.get_rect()
cuscuz_rect = cuscuz.get_rect()
bala_rect = bala.get_rect()

#funções
    
def respawn():
     x= 1350
     y= random.randint(1,640)
     return[x,y]
 
def respawn_bala():
    triggered = False
    respawn_bala_x = pos_player_x
    respawn_bala_y = pos_player_y
    vel_x_bala = 0
    return[respawn_bala_x, respawn_bala_y, triggered, vel_x_bala]

def colisions():
    global pontos
    if player_rect.colliderect(cuscuz_rect) or cuscuz_rect.x ==60:
       pontos -=1
       return True

    elif bala_rect.colliderect(cuscuz_rect):
       pontos +=1
       return True
    else:
       return False

 

while rodando:  # Enquanto o jogo estiver rodando
    for event in pygame.event.get():  # Verifica eventos (teclado, mouse, fechar janela)
        if event.type == pygame.QUIT:  
            rodando = False  
            
    screen.blit(bg, (0, 0))  # Desenha o fundo na tela, posição inicial

    # Carrossel infitiro
    rel_x = x % bg.get_rect().width  # Calcula a posição relativa do fundo para mover ele
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))  # Desenha segunda parte do fundo para efeito de continuidade
    if rel_x < 1280:  # Se ainda há espaço, desenha o fundo novamente
        screen.blit(bg, (rel_x, 0))
        
        
    #teclas
    
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_player_y > 0:

       pos_player_y -=2
       if not triggered:
          pos_bala_y -=1 
#velocidade q sobe
    if tecla[pygame.K_DOWN] and pos_player_y < (y - playerImg.get_height()):
        pos_player_y +=2#velocidade q desce
            
        if not triggered:
            pos_bala_y +=1 
            
 
            
    #atirar
    if tecla[pygame.K_SPACE] and not triggered:
        triggered = True
        vel_x_bala = 2
        pos_bala_x = pos_player_x + playerImg.get_width() - 20  # sair da frente do helicóptero
        pos_bala_y = pos_player_y + (playerImg.get_height() // 2) - (bala.get_height() // 2)  # centro vertical
    
    if pontos <= -1:
        rodando = False

#regras- respawn

    
    if pos_cuscuz_x == 50  :
        pos_cuscuz_x= respawn()[0]
        pos_cuscuz_y= respawn()[1]
        
    if pos_bala_x == 1300:
        pos_bala_x, pos_bala_y, triggered, vel_x_bala = respawn_bala()
        #principal respsv pelo respawn
    
    if pos_cuscuz_x == 50 or colisions():
        pos_cuscuz_x = respawn()[0]
        pos_cuscuz_y = respawn()[1]
    
    if pontos <= -1:
        game_over = True
        screen.blit(game_over_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)
        rodando = False

        
    # posição do rect

    player_rect.y= pos_player_y
    player_rect.x= pos_player_x

    bala_rect.x= pos_bala_x
    bala_rect.y= pos_bala_y

    cuscuz_rect.x= pos_cuscuz_x
    cuscuz_rect.y = pos_cuscuz_y
     
     

    #movimento
    x -= 6 #vel
    pos_cuscuz_x -=1
    
    pos_bala_x += vel_x_bala
    
    '''pygame.draw.rect(screen, (255, 0, 0), player_rect, 4)
    pygame.draw.rect(screen, (255, 0, 0), bala_rect, 4)
    pygame.draw.rect(screen, (255, 0, 0), cuscuz_rect, 4)'''
    
    score = font.render(f' Pontos:{ int(pontos)}', True, (0,0,0))
    screen.blit(score, (50,50))

    # Desenha os personagens na tela
   
    screen.blit(cuscuz, (pos_cuscuz_x, pos_cuscuz_y)) 
    screen.blit(playerImg, (pos_player_x, pos_player_y))  # Desenha o player na posição correta
    if triggered:
        screen.blit(bala, (pos_bala_x, pos_bala_y))

    print(pontos)
    pygame.display.update() 
