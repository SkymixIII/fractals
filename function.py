import pygame
import re 

def zoom(zoom_factor, signe):
    from graphique import _W,_H
    centerX = (_W[0] + _W[1]) / 2
    centerY = (_H[0] + _H[1]) / 2
    if signe == -1:
        width = (_W[1] - _W[0]) * zoom_factor
        height = (_H[1] - _H[0]) * zoom_factor
    else :
        width = (_W[1] - _W[0]) / zoom_factor
        height = (_H[1] - _H[0]) / zoom_factor
    return (centerX - width / 2, centerX + width / 2), (centerY - height / 2, centerY + height / 2)
                


def drawButtonsZF(surface, downUP, hover, regular, textColor, basicText, f_or_z, zoom_factor = 0):
    from graphique import width,height
    title = pygame.font.Font(None, 20)

    if f_or_z == 1:
        text_surface = basicText.render("Zoomer", True, regular)
        text_rect = text_surface.get_rect(left=int((5/4)*height)+10, top=height-150)
        tmp1 = draw_button(surface, int((5/4)*height)+10, height-120, int((width-int((5/4)*height))/2)-10, 50, "+", hover, regular, textColor, downUP, basicText)
        tmp2 = draw_button(surface, int((5/4)*height)+int((width-int((5/4)*height))/2)+10, height-120, int((width-int((5/4)*height))/2)-20, 50, "-", hover, regular, textColor, downUP, basicText)
    elif f_or_z == 2:
        text_surface = basicText.render(f"Accélerer le zoom : {zoom_factor}", True, regular)
        text_rect = text_surface.get_rect(left=int((5/4)*height)+10, top=height-300)
        tmp1 = draw_button(surface, int((5/4)*height)+10, height-270, int((width-int((5/4)*height))/2)-10, 50, "+", hover, regular, textColor, downUP, basicText)
        tmp2 = draw_button(surface, int((5/4)*height)+int((width-int((5/4)*height))/2)+10, height-270, int((width-int((5/4)*height))/2)-20, 50, "-", hover, regular, textColor, downUP, basicText)
    
    surface.blit(text_surface, text_rect)
    return tmp1,tmp2

def drawMultipleFix(surface, downUP, hover, regular, textColor, basicText):
    from graphique import width,height
    tmp1 = draw_button(surface, int((5/4)*height)+10, height-210, int((width-int((5/4)*height))/4)-10, 50, "x1.2", hover, regular, textColor, downUP, basicText)
    tmp2 = draw_button(surface, int((5/4)*height)+int((width-int((5/4)*height))/4)+10, height-210, int((width-int((5/4)*height))/4)-10, 50, "x10", hover, regular, textColor, downUP, basicText)
    tmp3 = draw_button(surface, int((5/4)*height)+2*int((width-int((5/4)*height))/4)+10, height-210, int((width-int((5/4)*height))/4)-10, 50, "x50", hover, regular, textColor, downUP, basicText)
    tmp4 = draw_button(surface, int((5/4)*height)+3*int((width-int((5/4)*height))/4)+10, height-210, int((width-int((5/4)*height))/4)-20, 50, "x100", hover, regular, textColor, downUP, basicText)
    
    return tmp1,tmp2,tmp3,tmp4

def drawSelecFrac(surface, downUP, hover, regular, textColor, basicText):
    from graphique import width,height
    tmp1 = draw_button(surface, int((5/4)*height)+10, 10, int((width-int((5/4)*height)))-20, 50, "Mandelbrot", hover, regular, textColor, downUP, basicText)
    tmp2 = draw_button(surface, int((5/4)*height)+10, 70, int((width-int((5/4)*height)))-20, 50, "Julia", hover, regular, textColor, downUP, basicText)
    return tmp1,tmp2     
    

def draw_button(surface, x, y, width, height, text, active_color, normal_color, text_color, downUP, basicText):
    mouse_pos = pygame.mouse.get_pos()
    
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        pygame.draw.rect(surface, active_color, (x, y, width, height))
        if downUP and mouse_pos[0]>(5/4)*height:  
            return True
    else:
        pygame.draw.rect(surface, normal_color, (x, y, width, height))
    
    text_surface = basicText.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)
    return False

def matchTextComplex(input_str):
    pattern = r"^\s*([\+\-]?\d+(\.\d+)?)(?:\s*([\+\-])\s*(\d+(\.\d+)?)i)\s*$"
    match = re.match(pattern, input_str)
    
    if not match:
        return (0.285, 0.01)  
    
    real_part = float(match.group(1))
    sign = match.group(3)  
    imag_part = float(match.group(4)) if match.group(4) else 0.0

    if sign == '-':
        imag_part = -imag_part

    return real_part, imag_part

def drawResetZoom(surface, downUP, hover, regular, textColor, basicText):
    from graphique import width,height
    return draw_button(surface, int((5/4)*height)+10, height-60, int(width-int((5/4)*height))-20, 50, "RESET", hover, regular, textColor, downUP, basicText)
    
    