import pygame
import time
import json

from pygame import mixer

mixer.init()
pygame.init()

pygame.display.set_caption('RADIO GAGA')

#Colegio WIDTH 854, HEIGHT 700
SCREEN = WIDTH, HEIGHT = 864, 700 
TILE_WIDTH = WIDTH // 12
TILE_HEIGHT = 100 
TILE_HEIGHT_HANDLER = TILE_HEIGHT/2
W_TILE_HEIGHT_HANDLER = (TILE_HEIGHT_HANDLER-TILE_HEIGHT*2)

WRONG_TILE_WIDTH = TILE_WIDTH
WRONG_TILE_HEIGHT = TILE_HEIGHT/2

screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()
FPS = 60

points = 0
color_timer = 0
TIMERTIME = 20
speed = 4.5

# COLORES *********************************************************************

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
DARKBLUE = (0,10,80)
DARKGREEN = (0,80,10)

# *****************************************************************************


class Key():
    def __init__(self, x,y,color1,color2,key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x,self.y,TILE_WIDTH,TILE_HEIGHT)
        self.handled = False

keys = [
    Key(4,HEIGHT-TILE_HEIGHT_HANDLER,BLUE,DARKBLUE,pygame.K_TAB),
    Key(4+(TILE_WIDTH),HEIGHT-TILE_HEIGHT_HANDLER,GREEN,DARKGREEN,pygame.K_q),
    Key(4+(TILE_WIDTH*2),HEIGHT-TILE_HEIGHT_HANDLER,BLUE,DARKBLUE,pygame.K_w),
    Key(4+(TILE_WIDTH*3),HEIGHT-TILE_HEIGHT_HANDLER,GREEN,DARKGREEN,pygame.K_e),
    Key(4+(TILE_WIDTH*4),HEIGHT-TILE_HEIGHT_HANDLER,BLUE,DARKBLUE,pygame.K_r),
    Key(4+(TILE_WIDTH*5),HEIGHT-TILE_HEIGHT_HANDLER,GREEN,DARKGREEN,pygame.K_t),
    Key(4+(TILE_WIDTH*6),HEIGHT-TILE_HEIGHT_HANDLER,BLUE,DARKBLUE,pygame.K_y),
    Key(4+(TILE_WIDTH*7),HEIGHT-TILE_HEIGHT_HANDLER,GREEN,DARKGREEN,pygame.K_u),
    Key(4+(TILE_WIDTH*8),HEIGHT-TILE_HEIGHT_HANDLER,BLUE,DARKBLUE,pygame.K_i),
    Key(4+(TILE_WIDTH*9),HEIGHT-TILE_HEIGHT_HANDLER,GREEN,DARKGREEN,pygame.K_o),
    Key(4+(TILE_WIDTH*10),HEIGHT-TILE_HEIGHT_HANDLER,BLUE,DARKBLUE,pygame.K_p),
    Key(4+(TILE_WIDTH*11),HEIGHT-TILE_HEIGHT_HANDLER,GREEN,DARKGREEN,pygame.K_BACKSPACE),
]

wrongKeys = [
    Key(4,HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_TAB),
    Key(4+(TILE_WIDTH),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_q),
    Key(4+(TILE_WIDTH*2),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_w),
    Key(4+(TILE_WIDTH*3),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_e),
    Key(4+(TILE_WIDTH*4),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_r),
    Key(4+(TILE_WIDTH*5),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_t),
    Key(4+(TILE_WIDTH*6),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_y),
    Key(4+(TILE_WIDTH*7),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_u),
    Key(4+(TILE_WIDTH*8),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_i),
    Key(4+(TILE_WIDTH*9),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_o),
    Key(4+(TILE_WIDTH*10),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_p),
    Key(4+(TILE_WIDTH*11),HEIGHT-W_TILE_HEIGHT_HANDLER,GRAY,WHITE,pygame.K_0),
]

# Herramienta de texto #####################
text_font = pygame.font.SysFont(None, 50)
text_font2 = pygame.font.SysFont(None, 32)
text_color = WHITE


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
############################################


# Función para cargar la canción y el archivo de notas
def load_song(selection):
    if selection == 0:  # Para Elisa
        piano = pygame.mixer.Sound('forElise.mp3')
        # voice = pygame.mixer.Sound('forEliseVoice.mp3')  # Ejemplo de voz si existe
        map_rect = load("forEliseNotes")  # Asegúrate de que el archivo exista
    elif selection == 1:  # The long and winding road
        piano = pygame.mixer.Sound('windingRoadPiano.mp3')
        voice = pygame.mixer.Sound('windingRoadVoice.mp3')
        map_rect = load("windingRoadNotes")
    elif selection == 2:  # Flying
        piano = pygame.mixer.Sound('flying.mp3')
        # voice = pygame.mixer.Sound('flyingVoice.mp3')  # Ejemplo de voz si existe
        map_rect = load("flyingNotes")  # Asegúrate de que el archivo exista
    # Agregar más canciones aquí
    # elif selection == 3:  # Nueva canción
    #     piano = pygame.mixer.Sound('nuevaCancion.mp3')
    #     voice = pygame.mixer.Sound('nuevaCancionVoice.mp3')  # Si tiene voz
    #     map_rect = load("nuevaCancionNotes")
    
    return piano, voice if 'voice' in locals() else None, map_rect

def load(map):
    rects = []
    f = open(map + ".txt",'r')
    data = f.readlines()

    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '0':
                rects.append(pygame.Rect(keys[x].rect.centerx -25,y*-100,50,65))
    return rects            

# Menú para seleccionar canción
def song_selector():
    selected_song = 0
    songs = ["Para Elisa", "The long and winding road", "Flying"]
    song_count = len(songs)
    
    while True:
        screen.fill(BLACK)
        
        draw_text("RADIO GAGÁ", text_font, YELLOW, 320, HEIGHT-(HEIGHT-30))  # Título del juego
        draw_text("Selecciona una canción", text_font2, text_color, 10, (HEIGHT-(HEIGHT-120)))
        draw_text("(Utiliza las dos primeras teclas blancas para navegar", text_font2, text_color, 10, (HEIGHT-(HEIGHT-150)))
        draw_text("y la tercera para seleccionar)", text_font2, text_color, 10, (HEIGHT-(HEIGHT-180)))

        # Dibuja las opciones de canciones
        for i, song in enumerate(songs):
            color = GREEN if i == selected_song else WHITE
            draw_text(song, text_font, color,210, (HEIGHT-200) // 2 + i*60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    selected_song = (selected_song + 1) % song_count
                elif event.key == pygame.K_w:  # Cambiar hacia el otro lado
                    selected_song = (selected_song - 1) % song_count
                elif event.key == pygame.K_r:  # Elegir
                    piano, voice, map_rect = load_song(selected_song)
                    return piano, voice, map_rect

        pygame.display.update()
        clock.tick(FPS)

# Llama al menú para seleccionar canción
piano, voice, map_rect = song_selector()
if voice:  # Reproduce la voz si existe
    voice.play()
piano.play()

while True:

    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()


    
    if event.type == pygame.KEYUP:
        piano.set_volume(1)

    k = pygame.key.get_pressed()

    for key in keys:
        # Si la tecla se presiona
        if k[key.key]:
            pygame.draw.rect(screen, key.color1, key.rect)
            
            # Si ya está procesada (handled), ignoramos el resto
            if key.pressed:
                continue
            
            # Verificar si hay colisión con alguna nota
            collision = False
            for rect in map_rect:
                if key.rect.colliderect(rect):
                    map_rect.remove(rect)  # Se elimina la nota si hay colisión
                    key.handled = True

                    points += 10  # Aumenta 10 puntos si la tecla es correcta
                    color_timer = TIMERTIME
                    text_color = GREEN

                    collision = True
                    break
            
            # Si no hubo colisión, se presionó una tecla incorrecta
            if not collision:

                points -= 1  # Se reducen los puntos
                color_timer = TIMERTIME
                text_color = RED
                piano.set_volume(0)

            key.pressed = True  # Se marca la tecla como presionada para no aplicar la penalización continuamente

        else:
            pygame.draw.rect(screen, key.color2, key.rect)
            key.handled = True
            key.pressed = False  # Se restablece cuando se suelta la tecla

    # Dibujo de los rectángulos de wrongKeys
    for key in wrongKeys:
        if k[key.key]:
            pygame.draw.rect(screen, key.color1, key.rect)
            key.handled = False
        if not k[key.key]:
            pygame.draw.rect(screen, key.color2, key.rect)
            key.handled = True

    for rect in map_rect:
        pygame.draw.rect(screen, (200, 0, 0), rect)
        rect.y += speed
        
        for key in wrongKeys:
            if key.rect.colliderect(rect):
                # Se toca un rectángulo blanco

                points -= 10  # Resta 1 punto
                color_timer = TIMERTIME
                text_color = RED
                piano.set_volume(0)

                # Se elimina la nota
                map_rect.remove(rect)
                break

        for key in keys:
            if key.rect.colliderect(rect) and not key.handled:
                map_rect.remove(rect)
                key.handled = True

                points += 10  # Aumenta 10 puntos si la tecla es correcta
                color_timer = TIMERTIME
                text_color = GREEN

                break

    draw_text("Puntos "+str(points),text_font,text_color,350,450)

    if color_timer > 0:
        color_timer -= 1
    else:
        text_color = WHITE


    pygame.display.update()
    clock.tick(FPS)