import pygame
from numpy import zeros, uint8, float128
from sys import exit
from function import *
from stable import * 




pygame.init()
width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fractals")
clock = pygame.time.Clock()



#VARIABLE
basicText = pygame.font.Font(None, 36)
update = False


#BASE -> MANDELBROT
k = 1
_W = (-2.2,0.8)
_H = (1.5,-1.5)

#JULIA 
j=(0.285, 0.01)


input_text = ""
zoom_factor = 1.2
current_zoom = float128(abs(_W[0]-_W[1])/((5/4)*height))

#COLORS
black = (0, 0, 0)
white = (255, 255, 255)
purple = (202, 194, 235)
pink = (224, 209, 240)
light_blue = (163, 219, 224)
light_green = (140, 217, 176)


#WINDOW
surface = pygame.Surface((int((5/4)*height), height), depth=24)
matrix = zeros((int((5/4)*height), height, 3), dtype=uint8)






rectangle_surface = pygame.Surface((1000, 3000))
rectangle_surface.fill(black)

text_back = pygame.Surface((width - int((5/4)*height) -20,36))
text_back.fill(pink)
window.blit(text_back, (int((5/4)*height)+10, 130))



compute_fractal(matrix,int((5/4)*height),height,_W,_H,k,j)
pygame.surfarray.blit_array(surface, matrix)

    



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: 
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                j = matchTextComplex(input_text)
                k = 2
                _W = (-1.5,1.5)
                _H = (1.5,-1.5)
                compute_fractal(matrix, int((5/4) * height), height, _W, _H,k,j)
                pygame.surfarray.blit_array(surface, matrix)
                input_text = ""
            else: 
                input_text += event.unicode
            text_surface = basicText.render(input_text, True, black)
            text_rect = text_surface.get_rect(left=int((5/4)*height)+10, top=130)
            window.blit(text_back, (int((5/4)*height)+10, 130))
            window.blit(text_surface, text_rect)
        if event.type == pygame.MOUSEBUTTONUP:
            update = True
            pos = event.pos
            if pos[0] < (5/4) * height: 
                if event.button == 1: 
                    tmpX = _W[0] + (pos[0] / int((5/4)*height)) * (_W[1] - _W[0])
                    tmpY = _H[0] + (pos[1] / height) * (_H[1] - _H[0])

                    dx = (_W[1] - _W[0]) / zoom_factor
                    dy = (_H[1] - _H[0]) / zoom_factor
                    _W = (tmpX - dx / 2, tmpX + dx / 2)
                    _H = (tmpY - dy / 2, tmpY + dy / 2)

                    current_zoom = float128(abs(_W[0]-_W[1])/((5/4)*height))

                compute_fractal(matrix, int((5/4) * height), height, _W, _H,k,j)
                pygame.surfarray.blit_array(surface, matrix)
                update = False



                
            

    if (width,height) != window.get_size():
        width,height = window.get_size()
        matrix = zeros((int((5/4)*height), height, 3), dtype=uint8)
        surface = pygame.Surface((int((5/4)*height), height), depth=24)
        compute_fractal(matrix,int((5/4)*height),height,_W,_H,k,j)
        pygame.surfarray.blit_array(surface, matrix)
        text_back = pygame.Surface((width - int((5/4)*height) -20,36))
        text_back.fill(pink)
        window.blit(text_back, (int((5/4)*height)+10, 130))
        text_surface = basicText.render(input_text, True, black)
        text_rect = text_surface.get_rect(left=int((5/4)*height)+10, top=130)
        window.blit(text_surface, text_rect)
        


    reset,dix,cinquante,cent = drawMultipleFix(window, update, purple, pink, black, basicText)
    zoomIn,zoomOut = drawButtonsZF(window, update, purple, pink, black, basicText,1)
    fastIn,fastOut = drawButtonsZF(window, update, purple, pink, black, basicText,2,zoom_factor)
    mandel,julia = drawSelecFrac(window, update, purple, pink, black, basicText)
    resetZoom = drawResetZoom(window, update, purple, pink, black, basicText)
    

    if resetZoom:
        update = False
        if k == 1:
            _W = (-2.2,0.8)
            _H = (1.5,-1.5)
        if k == 2:
            _W = (-1.5,1.5)
            _H = (1.5,-1.5)
        compute_fractal(matrix,int((5/4)*height),height,_W,_H,k,j)
        pygame.surfarray.blit_array(surface, matrix)
        current_zoom = float128(abs(_W[0]-_W[1])/((5/4)*height))

    if zoomIn or zoomOut:
        update = False
        if zoomIn: 
            _W,_H = zoom(zoom_factor, 1)
            current_zoom = float128(abs(_W[0]-_W[1])/((5/4)*height))
            compute_fractal(matrix,int((5/4)*height),height,_W,_H,k,j)
        else: 
            _W,_H = zoom(zoom_factor+0.5, -1)
            current_zoom = float128(abs(_W[0]-_W[1])/((5/4)*height))
            compute_fractal(matrix,int((5/4)*height),height,_W,_H,k,j) 
        pygame.surfarray.blit_array(surface, matrix)

    if fastIn or fastOut or reset or dix or cinquante or cent:
        update = False
        if fastIn:
            zoom_factor+=.2
        if fastOut:
            zoom_factor-=.2

        if reset:
            zoom_factor = 1.2
        if dix:
            zoom_factor = 10
        if cinquante:
            zoom_factor = 50
        if cent:
            zoom_factor = 100
        window.blit(rectangle_surface, (int((5/4)*height), 0))
        text_surface = basicText.render(input_text, True, black)
        text_rect = text_surface.get_rect(left=int((5/4)*height)+10, top=130)
        window.blit(text_back, (int((5/4)*height)+10, 130))
        window.blit(text_surface, text_rect)


    if julia or mandel:
        if mandel:
            update = False
            k = 1
            _W = (-2.2,0.8)
            _H = (1.5,-1.5)
            compute_fractal(matrix,int((5/4)*height),height,_W,_H,k,j) 


        if julia:
            update = False
            k = 2
            _W = (-1.5,1.5)
            _H = (1.5,-1.5)
            compute_fractal(matrix,int((5/4)*height),height,_W,_H,k,j) 
        pygame.surfarray.blit_array(surface, matrix)


        


    

    

    

    
    

    fps = clock.get_fps()
    text_fps = basicText.render(f"FPS: {fps:.1f}", True, light_blue)
    text_zoom = basicText.render(f"1px <-> {current_zoom}", True, light_blue)


    window.blit(surface, (0, 0))
    window.blit(text_fps, (10, 10))
    window.blit(text_zoom, (10, height-46))
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
exit(1)
