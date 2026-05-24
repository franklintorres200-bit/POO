import pygame
import math
from constantes import *
from ui.widgets import Boton



class EscenaMenu:
    def __init__(self, j):
        self.j = j; cx = ANCHO//2
        self.bs = [Boton(cx-130, 340, 260, 55, "JUGAR", C_AZUL, font_size=24),
                   Boton(cx-130, 410, 260, 55, "SALON DE LA FAMA", C_MORADO, font_size=20),
                   Boton(cx-130, 480, 260, 55, "CREDITOS", C_VERDE_OSC, font_size=22),
                   Boton(cx-130, 550, 260, 55, "SALIR", C_ROJO, font_size=22)]
        self.t = 0

    def manejar(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.bs[0].verificar_click(e.pos): self.j.cambiar("nombre")
            elif self.bs[1].verificar_click(e.pos): self.j.cambiar("ranking")
            elif self.bs[2].verificar_click(e.pos): self.j.cambiar("creditos")
            elif self.bs[3].verificar_click(e.pos): self.j.corriendo = False

    def actualizar(self):
        pos = pygame.mouse.get_pos()
        for b in self.bs: b.verificar_hover(pos)
        self.t += 0.05

    def dibujar(self, p):
        t = self.j.f4.render("SOMBRAS Y GLORIA", True, C_DORADO)
        s = self.j.f4.render("SOMBRAS Y GLORIA", True, (80,60,0))
        tx = ANCHO//2 - t.get_width()//2; ty = 140 + int(math.sin(self.t)*4)
        p.blit(s, (tx+3, ty+3)); p.blit(t, (tx, ty))
        sub = self.j.f2.render("Combate Epico por Turnos", True, C_GRIS_CLARO)
        p.blit(sub, (ANCHO//2 - sub.get_width()//2, 220))
        pygame.draw.line(p, C_DORADO, (250, 270), (ANCHO-250, 270), 2)
        for b in self.bs: b.dibujar(p, self.j.f2)
