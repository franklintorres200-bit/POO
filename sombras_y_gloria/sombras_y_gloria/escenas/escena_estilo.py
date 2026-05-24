import pygame
from constantes import *
from ui.widgets import Boton
from ui.render import _osc


class EscenaEstilo:
    def __init__(self, j):
        self.j = j; cx = ANCHO//2
        self.b1 = Boton(cx-260, 280, 240, 240, "", C_NARANJA)
        self.b2 = Boton(cx+20, 280, 240, 240, "", C_CYAN)
        self.bv = Boton(20, 20, 110, 38, "< Volver", C_GRIS, font_size=16)

    def manejar(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.b1.verificar_click(e.pos): self.j.estilo = "agresivo"; self.j.cambiar("enemigo")
            elif self.b2.verificar_click(e.pos): self.j.estilo = "defensivo"; self.j.cambiar("enemigo")
            elif self.bv.verificar_click(e.pos): self.j.cambiar("clase")

    def actualizar(self):
        pos = pygame.mouse.get_pos(); self.b1.verificar_hover(pos); self.b2.verificar_hover(pos); self.bv.verificar_hover(pos)

    def dibujar(self, p):
        self.bv.dibujar(p, self.j.f1)
        t = self.j.f3.render(f"Estilo de Combate - {self.j.clase.upper()}", True, C_BLANCO); p.blit(t, (ANCHO//2 - t.get_width()//2, 100))
        if self.j.clase == "heroe":
            i1 = ["Saitama", "Maximo dano", "Poca defensa", "Golpe devastador"]
            i2 = ["Capitan America", "Buena defensa", "Dano moderado", "Equilibrado"]
        else:
            i1 = ["El Guason", "Dano impredecible", "Defensa baja", "Caotico"]
            i2 = ["Magneto", "Gran defensa", "Recupera vida", "Controlador"]
        self._panel(p, self.b1.rect, "AGRESIVO", C_NARANJA, i1)
        self._panel(p, self.b2.rect, "DEFENSIVO", C_CYAN, i2)

    def _panel(self, p, r, t, c, info):
        pygame.draw.rect(p, C_PANEL, r, border_radius=14); pygame.draw.rect(p, c, r, 3, border_radius=14)
        cx = r.centerx
        pygame.draw.circle(p, _osc(c,0.3), (cx, r.y+50), 28); pygame.draw.circle(p, c, (cx, r.y+50), 28, 3)
        i = self.j.f3.render(t[0], True, C_BLANCO); p.blit(i, (cx - i.get_width()//2, r.y+30))
        tt = self.j.f2.render(t, True, c); p.blit(tt, (cx - tt.get_width()//2, r.y+90))
        y = r.y + 125
        for l in info:
            s = self.j.f1.render(f"- {l}", True, C_BLANCO); p.blit(s, (r.x+25, y)); y += 26
