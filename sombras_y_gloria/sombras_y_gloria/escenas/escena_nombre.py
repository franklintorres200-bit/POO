import pygame
from constantes import *
from ui.widgets import Boton, CampoTexto


class EscenaNombre:
    def __init__(self, j):
        self.j = j; cx = ANCHO//2
        self.c = CampoTexto(cx-160, 340, 320, 48, "Escribe tu nombre...")
        self.b1 = Boton(cx-110, 420, 220, 50, "CONTINUAR", C_VERDE, font_size=22)
        self.b2 = Boton(20, 20, 110, 38, "< Volver", C_GRIS, font_size=16)

    def manejar(self, e):
        r = self.c.manejar(e)
        if r is not None and r.strip(): self.j.nombre = r.strip(); self.j.cambiar("clase")
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.b1.verificar_click(e.pos): self.j.nombre = self.c.texto.strip() or "Jugador"; self.j.cambiar("clase")
            elif self.b2.verificar_click(e.pos): self.j.cambiar("menu")

    def actualizar(self):
        pos = pygame.mouse.get_pos(); self.b1.verificar_hover(pos); self.b2.verificar_hover(pos)

    def dibujar(self, p):
        self.b2.dibujar(p, self.j.f1)
        t = self.j.f3.render("Cual es tu nombre, guerrero?", True, C_BLANCO)
        p.blit(t, (ANCHO//2 - t.get_width()//2, 180))
        self.c.dibujar(p, self.j.f2); self.b1.dibujar(p, self.j.f2)
        h = self.j.f1.render("Presiona Enter para continuar", True, C_GRIS)
        p.blit(h, (ANCHO//2 - h.get_width()//2, 490))
