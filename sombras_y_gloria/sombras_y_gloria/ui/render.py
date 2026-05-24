import pygame
import random
import math
from constantes import *

_fondo_cache = None


def dibujar_fondo(pantalla):
    global _fondo_cache
    if _fondo_cache is None:
        surf = pygame.Surface((ANCHO, ALTO))
        for y in range(ALTO):
            t = y / ALTO
            r = int(8 + t * 18)
            g = int(5 + t * 8)
            b = int(20 + t * 30)
            pygame.draw.line(surf, (r, g, b), (0, y), (ANCHO, y))
        for _ in range(6):
            cx = random.randint(0, ANCHO)
            cy = random.randint(0, ALTO)
            radio = random.randint(80, 220)
            nebula = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
            col = random.choice([(40, 10, 80, 18), (10, 20, 70, 15), (60, 10, 50, 12)])
            pygame.draw.circle(nebula, col, (radio, radio), radio)
            surf.blit(nebula, (cx - radio, cy - radio))
        _fondo_cache = surf
    pantalla.blit(_fondo_cache, (0, 0))


def _color_p(p):
    return {"Saitama": COLOR_SAITAMA, "Capitan America": COLOR_CAPITAN, "El Guason": COLOR_GUASON, "Magneto": COLOR_MAGNETO}.get(p.personaje, C_AZUL)

def _osc(c, f):
    return tuple(int(x * f) for x in c)


def dibujar_personaje(p, pers, x, y, es_j, anim=0, flash=False, f=None):
    c = _color_p(pers); x += anim
    pygame.draw.ellipse(p, (15,15,15), (x-30, y+65, 60, 12))
    pygame.draw.rect(p, _osc(c,0.7), (x-14, y+38, 11, 28), border_radius=4)
    pygame.draw.rect(p, _osc(c,0.7), (x+3, y+38, 11, 28), border_radius=4)
    pygame.draw.rect(p, c, (x-18, y-8, 36, 48), border_radius=6)
    pygame.draw.rect(p, _osc(c,0.5), (x-18, y+25, 36, 5))
    pygame.draw.rect(p, _osc(c,0.85), (x-28, y-3, 10, 32), border_radius=4)
    pygame.draw.rect(p, _osc(c,0.85), (x+18, y-3, 10, 32), border_radius=4)
    pygame.draw.circle(p, c, (x, y-28), 20)
    pygame.draw.circle(p, C_BLANCO, (x-7, y-31), 5); pygame.draw.circle(p, C_BLANCO, (x+7, y-31), 5)
    pygame.draw.circle(p, C_NEGRO, (x-6, y-31), 3); pygame.draw.circle(p, C_NEGRO, (x+8, y-31), 3)
    if pers.personaje == "Saitama": pygame.draw.circle(p, (255,255,200), (x-5, y-40), 4)
    elif pers.personaje == "Capitan America":
        pts = []
        for i in range(10):
            a = math.pi/2 + i*math.pi/5; r = 8 if i%2==0 else 3.2
            pts.append((x + r*math.cos(a), y+8 - r*math.sin(a)))
        pygame.draw.polygon(p, C_BLANCO, pts)
    elif pers.personaje == "El Guason": pygame.draw.arc(p, C_ROJO, (x-10, y-24, 20, 12), 0, 3.14, 2)
    elif pers.personaje == "Magneto": pygame.draw.arc(p, C_MORADO, (x-22, y-50, 44, 30), 0, 3.14, 3)
    if flash:
        s = pygame.Surface((70, 110), pygame.SRCALPHA); s.fill((255,50,50,120)); p.blit(s, (x-30, y-48))
    if f:
        et = "TU" if es_j else "ENEMIGO"; c_et = C_CYAN if es_j else C_ROJO
        t = f.render(et, True, c_et); p.blit(t, (x - t.get_width()//2, y+78))
